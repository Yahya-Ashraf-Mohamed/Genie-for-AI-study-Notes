import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_groq import ChatGroq
from langchain_pinecone import Pinecone
import uuid
from pathlib import Path
import uuid
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


rag_instances = {}
##########      Files Embedding     ##########
os.environ["PINECONE_API_KEY"] = "pcsk_7a6x6_Mq2MQntZVjiiXLLpdPWXfKdgKatSLRn3FHrETqvixgyR6TEJoZBbw7CtBYAaWnk" 
os.environ["GROQ_API_KEY"] = "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"
embeddings=FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")



class PDFProcessor:
    def __init__(self, pdf_path, index_name="gradproject", chunk_size=1000, chunk_overlap=100, batch_size=64):
        self.pdf_path = Path(pdf_path)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.batch_size = batch_size  # New: Batch size for embeddings
        self.embeddings = embeddings
        self.index_name = index_name
        # Initialize Pinecone vector store
        self.vector_db = Pinecone.from_existing_index(
            index_name=self.index_name,
            embedding=self.embeddings,
            text_key="text"
        )

    def read_pdf(self):
        """Reads the PDF document."""
        loader = UnstructuredFileLoader(self.pdf_path)
        self.pages = loader.load()
        return self.pages

    def split_document(self):
        """Splits the document into smaller chunks."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        self.texts = text_splitter.split_documents(self.pages)
        return self.texts

    def perform_embedding(self):
        """Generates embeddings in batches and stores them in Pinecone with metadata."""
        # Create metadata for each chunk (e.g., including the PDF file name)
        metadatas = [{"source": str(self.pdf_path.name), "id": str(uuid.uuid4())} for _ in self.texts]
        texts = [doc.page_content for doc in self.texts]  # Extract text content from Document objects

        # Batch processing for embeddings
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            batch_metadatas = metadatas[i:i + self.batch_size]
            self.vector_db.add_texts(texts=batch_texts, metadatas=batch_metadatas)

        return self.vector_db

    def prepare_pdf(self):
        self.read_pdf()
        print("Reading PDF is done")
        self.split_document()
        print("Splitting and storing PDF is done")
        self.perform_embedding()
        print("Embedding is done")


##########      RAG     ##########


class RagChain:
    def __init__(self, source_name, index_name="gradproject", model_name="llama-3.1-8b-instant", temperature=0):
        self.model_name = model_name
        self.llm = ChatGroq(temperature=temperature, model_name=model_name)
        self.source_name = source_name
        self.index_name = index_name
        # Generate a unique session ID
        self.session_id = str(uuid.uuid4())

        # Initialize vector database
        self.vector_db = Pinecone.from_existing_index(
            index_name=self.index_name,
            embedding=embeddings,
            text_key="text"
        )
        self.retriever = self.vector_db.as_retriever( search_kwargs={
            "filter": {"source": self.source_name}, 
        })

        # Create history-aware retriever
        self.contextualize_q_prompt = self.create_contextualize_q_prompt()
        self.history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, self.contextualize_q_prompt
        )

        # Create retrieval QA chain
        self.qa_prompt = self.create_qa_prompt()
        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.qa_prompt)
        self.rag_chain = create_retrieval_chain(self.history_aware_retriever, self.question_answer_chain)

        # Single chat history for all interactions
        self.chat_history = ChatMessageHistory()

        # Initialize conversational chain with message history
        self.conversational_rag_chain = self.create_conversational_rag_chain()

    def create_contextualize_q_prompt(self):
        """Creates the prompt for contextualizing questions."""
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        return ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

    def create_qa_prompt(self):
        """Creates the system prompt for question answering."""
        system_prompt = (
            """
        Use the following pieces of information to answer the user's question.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            Answer the question and provide additional helpful information,
            based on the pieces of information, if applicable. Be succinct.
            Responses should be properly formatted to be easily read.


            Context: {context}


        """
        )
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

    def create_conversational_rag_chain(self):
        """Creates a conversational chain with history management."""
        return RunnableWithMessageHistory(
            self.rag_chain,
            lambda _: self.chat_history,  # Always use the single default chat history
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def trim_memory_to_window(self, max_messages: int = 10):
        """
        Ensures chat history contains only the most recent `max_messages`.
        """
        if len(self.chat_history.messages) > max_messages:
            # Trim messages to retain only the most recent `max_messages`
            self.chat_history.messages = self.chat_history.messages[-max_messages:]

    def ask_question(self, question: str):
        """Queries the conversational chain and returns the response."""
        try:
    
            # Trim memory to keep only the most recent 10 messages
            self.trim_memory_to_window(max_messages=10)


            # Invoke the conversational chain
            response = self.conversational_rag_chain.invoke(
                {"input": question},
                config={"configurable": {"session_id": self.session_id}}  # Pass the session ID explicitly
            )

            return response.get("answer", "No answer returned.")
        except Exception as e:
            print(f"Error while querying the chain: {e}")
            return "An error occurred while processing your question."


# obj=RagChain(source_name=r"..\Storage\6- Permutation test.pdf")
# obj.ask_question("What is the permutation test?")
# obj.ask_question("explain more")