import uuid
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.vectorstores import Pinecone
from langchain_groq import ChatGroq
from langchain.embeddings import FastEmbedEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
import uuid
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
rag_instances = {}  

class VectorDatabase:
    def __init__(self, index_name, source_name, embedding_model="BAAI/bge-base-en-v1.5"):
        self.index_name = index_name
        self.source_name = source_name
        self.embeddings = FastEmbedEmbeddings(model_name=embedding_model)

        # Initialize Pinecone vector store
        self.vector_db = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=self.embeddings,
            text_key="text"
        )


    def get_retriever(self):
        return self.vector_db.as_retriever( search_kwargs={
            "filter": {"source": self.source_name}
        },k=4)




class QAPrompt:
    def __init__(self, llm):
        self.llm = llm

    def create(self):
        system_prompt = (
            """
           You are a helpful educational assistant. Your goal is to assist users in understanding educational documents and answering their questions.

            You will be provided with:
            1. A user's question.
            2. Context from an educational document that may or may not address the question.
            
            Your task is to:
            - Use the provided context to answer the user's question as clearly and thoroughly as possible.
            - Explain your answer in a way that enhances the user's understanding of the subject.
            - If the context does not provide enough information, honestly say, "The document probably does not provide an answer," and use your intelligence to provide a simple and accurate answer.
           
        
            Be honest,concise,summarized, and avoid making up answers when neither the document nor your knowledge provides enough information.

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

class ContextualizePrompt:
    def __init__(self, llm):
        self.llm = llm

    def create(self):
        system_prompt = (
            """You will be provided with a chat history and the latest user question,\n"
            "which might reference context in the chat history.\n"
            "Your task is to formulate a standalone question which can be understood without the chat history. \n"
            "Note: Do NOT answer the question, just reformulate it if needed and otherwise return it as is.
            """
        )
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )


class ConversationalChain:
    def __init__(self, retriever, memory_llm, contextualize_llm):
        self.memory_llm = memory_llm
        self.contextualize_llm = contextualize_llm
        self.memory = ConversationSummaryBufferMemory(
            llm=memory_llm,
            max_token_limit=20000,  # Adjust this as needed
            memory_key="chat_history"
        )

        self.contextualize_q_prompt = ContextualizePrompt(self.contextualize_llm).create()
        self.history_aware_retriever = create_history_aware_retriever(
            self.contextualize_llm, retriever, self.contextualize_q_prompt
        )

        self.qa_prompt = QAPrompt(self.memory_llm).create()
        self.question_answer_chain = create_stuff_documents_chain(self.memory_llm, self.qa_prompt)

        self.rag_chain = create_retrieval_chain(self.history_aware_retriever, self.question_answer_chain)

    def create_conversational_rag_chain(self):
        return RunnableWithMessageHistory(
            self.rag_chain,
            lambda _: self.memory.chat_memory,  # Pass memory messages
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )



class RagChain:
    def __init__(self, source_name, index_name="gradproject", memory_model="llama-3.1-8b-instant", contextualize_model="llama-3.3-70b-versatile", temperature=0):
        self.memory_llm = ChatGroq(
            model=memory_model,
            temperature=0,
            timeout=10,
            max_retries=2
        )
        self.contextualize_llm = ChatGroq(temperature=0, model_name=contextualize_model)

        self.source_name = source_name
        self.index_name = index_name

        # Generate a unique session ID
        self.session_id = str(uuid.uuid4())

        # Initialize vector database and retriever
        vector_db = VectorDatabase(index_name, source_name)
        self.retriever = vector_db.get_retriever()

        # Initialize conversational chain
        self.conversational_chain = ConversationalChain(self.retriever, self.memory_llm, self.contextualize_llm)
        self.conversational_rag_chain = self.conversational_chain.create_conversational_rag_chain()

    def ask_question(self, question: str):
        """Queries the conversational chain and returns the response."""
        try:
            # Invoke the conversational chain
            response = self.conversational_rag_chain.invoke(
                {"input": question},
                config={"configurable": {"session_id": self.session_id}}  # Pass the session ID explicitly
            )

            return response.get("answer", "No answer returned.")
        except Exception as e:
            print(f"Error while querying the chain: {e}")
            return "An error occurred while processing your question."
