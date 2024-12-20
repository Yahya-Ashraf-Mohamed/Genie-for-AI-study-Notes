import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import FastEmbedEmbeddings
from langchain.vectorstores import Chroma
from langchain.vectorstores.utils import filter_complex_metadata
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_groq import ChatGroq
from langchain.memory import ConversationSummaryMemory
from langchain_pinecone import Pinecone
import uuid


##########      Files Embedding     ##########
os.environ["PINECONE_API_KEY"] = "pcsk_7a6x6_Mq2MQntZVjiiXLLpdPWXfKdgKatSLRn3FHrETqvixgyR6TEJoZBbw7CtBYAaWnk" 
class PDFProcessor:
    def __init__(self,pdf_path, index_name="gradproject", embedding_model="BAAI/bge-base-en-v1.5", chunk_size=1000, chunk_overlap=100):
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings = FastEmbedEmbeddings(model_name=embedding_model)
    
        # Initialize Pinecone vector store
        self.vector_db =  Pinecone.from_existing_index(
            index_name=index_name,
            embedding=self.embeddings,
            text_key="text" 
        )

    
    def read_pdf(self):
        """Reads the PDF document."""
        # loader = PyPDFLoader(self.pdf_path, extract_images=True)
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
        """Generates embeddings and stores them in Pinecone with the PDF file name as metadata."""
        # Create metadata for each chunk (e.g., including the PDF file name)
        metadatas = [{"source": self.pdf_path, "id": str(uuid.uuid4())} for _ in self.texts]

        # Add text chunks and their metadata to the Pinecone index
        texts = [doc.page_content for doc in self.texts]  # Extract text content from Document objects
        self.vector_db.add_texts(texts=texts, metadatas=metadatas)
        return self.vector_db


    def prepare_pdf(self):
        self.read_pdf()
        print("reading pdf is done")
        self.split_document()
        print("spliting and storing pdf is done")
        self.perform_embedding()
        print("embedding is done")


##########      RAG     ##########
class RagChain:
    def __init__(self,  source_name,index_name="gradproject", embedding_model="BAAI/bge-base-en-v1.5", model_name="llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.groq_client = ChatGroq(temperature=0, model_name=model_name)
        self.memory = ConversationSummaryMemory(memory_key="chat_history", return_messages=True, llm=self.groq_client)
        self.embeddings = FastEmbedEmbeddings(model_name=embedding_model)
        self.souce_name=source_name
        # Initialize Pinecone vector store
        self.vector_db = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=self.embeddings,
            text_key="text" 
        )
        self.conversational_chain = self.create_qa_chain()

    def create_qa_chain(self):
        """Creates a RetrievalQA chain."""

        # ChatGPT-style template using ChatPromptTemplate
        system_template = """
        Use the following pieces of information to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Answer the question and provide additional helpful information,
        based on the pieces of information, if applicable. Be succinct.
        Responses should be properly formatted to be easily read.

        Context: {context}
        """

        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = "{question}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        # Create the conversational chain with the template
        conversational_chain = RetrievalQA.from_chain_type(
            llm=self.groq_client,
            retriever=self.vector_db.as_retriever(search_kwargs={
            "filter": {"source": self.souce_name}  # Filter results by the source metadata
        }),
            memory=self.memory,
            chain_type="stuff",
            chain_type_kwargs={"prompt": chat_prompt}
        )
        return conversational_chain

    def ask_question(self, question):
        """Queries the chain and returns the response."""
        try:
            # Run the chain and return the result
            return self.conversational_chain.invoke({"query": question})
        except Exception as e:
            print(f"Error while querying the chain: {e}")
            return "An error occurred while processing your question."
        
        

    def load_memory(self, chat_history):
        """Reconstructs memory from saved chat history."""
        for msg in chat_history:
            sender = "user" if msg["sender"] == "user" else "system"
            self.memory.add_message(sender, msg["message"])
