from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import FastEmbedEmbeddings
from langchain.vectorstores import Chroma
from langchain.vectorstores.utils import filter_complex_metadata
from langchain_community.document_loaders import UnstructuredFileLoader

class PDFProcessor:
    def __init__(self, pdf_path, embedding_model="BAAI/bge-base-en-v1.5", chunk_size=1000, chunk_overlap=100, persist_directory="db"):
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.persist_directory = persist_directory
        self.embeddings = FastEmbedEmbeddings(model_name=embedding_model)
        self.pages = None
        self.texts = None
        self.vector_db = None

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
        """Generates embeddings and stores them in a vector database."""
        filtered_documents = filter_complex_metadata(self.texts)
        self.vector_db = Chroma.from_documents(
            documents=filtered_documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        return self.vector_db

    def prepare_pdf(self):
        """Complete PDF preparation pipeline."""
        self.read_pdf()
        print("Reading PDF is done")
        self.split_document()
        print("Splitting and storing PDF is done")
        self.perform_embedding()
        print("Embedding is done")