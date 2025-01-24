from langchain.embeddings import FastEmbedEmbeddings
from langchain.prompts import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_pinecone import Pinecone
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from pathlib import Path

class DocumentRetriever:
    """
    A class to handle document retrieval and embeddings using a vector database.
    """

    def __init__(self, source_name,index_name="gradproject", embedding_model="BAAI/bge-base-en-v1.5"):
        """
        Initialize the DocumentRetriever with Pinecone vector store and embeddings.

        Args:
            index_name (str): The name of the Pinecone index.
            embedding_model: The embedding model instance (e.g., FastEmbedEmbeddings).
         
        """
        self.source_name= str(Path(source_name).name)
        self.embeddings = FastEmbedEmbeddings(model_name=embedding_model)

        # Initialize the Pinecone vector database
        self.vector_db = Pinecone.from_existing_index(
                    index_name=index_name,
                    embedding=self.embeddings,
                    text_key="text" 
                )
    def retrieve_all_chunks(self):
        """
        Retrieve all the chunks of a document based on its source metadata.

        Args:
            source_name (str): The name or path of the document used as metadata.

        Returns:
            List of documents containing all chunks of the document.
        """
        retrieved_docs = self.vector_db.similarity_search(
            query="",  # Query is not necessary since we're using a filter
            k=10000,  # Large value to ensure all chunks are retrieved
            filter={"source": self.source_name},  # Filter by the source metadata
        )

        print(f"Retrieved {len(retrieved_docs)} chunks from source: {self.source_name}")
        return retrieved_docs
class KnowledgeExtractor:
    """
    A pipeline to extract key knowledge points from educational documents using a Map-Reduce process.
    """

    def __init__(self, map_llm="llama-3.1-8b-instant",reduce_llm="llama-3.1-8b-instant", token_max=5000, max_insights=15):
        """
        Initialize the KnowledgeExtractor pipeline.

        Args:
            llm: The language model to use (e.g., groq_client).
            token_max (int): Maximum token limit for reducing documents. Default is 10000.
            max_insights (int): Maximum number of insights to output in the reduce phase. Default is 15.
        """
        self.token_max = token_max
        self.max_insights = max_insights

        self.map_client=ChatGroq(temperature=0, model_name=map_llm)
        self.reduce_client=ChatGroq(temperature=0, model_name=reduce_llm)
        
        # Initialize Map and Reduce prompts
        self.map_prompt = self._create_map_prompt()
        self.reduce_prompt = self._create_reduce_prompt()

        # Create LLM Chains
        self.map_chain = LLMChain(llm=self.map_client, prompt=self.map_prompt)
        self.reduce_chain = LLMChain(llm=self.reduce_client, prompt=self.reduce_prompt)

        # Create Chains
        self.combine_documents_chain = self._create_combine_documents_chain()
        self.reduce_documents_chain = self._create_reduce_documents_chain()
        self.map_reduce_chain = self._create_map_reduce_chain()

    def _create_map_prompt(self):
        """
        Define the prompt for the map phase.
        """
        template = """  
        You are summarizing multiple summaries from an educational document. 
        Combine the provided summaries into a single, cohesive summary that represents the entire document. 
        Focus on unifying key themes, concepts, and insights while avoiding redundancy.{docs}
        
        Generated Summary:"""
        return PromptTemplate.from_template(template)

    def _create_reduce_prompt(self):
    
        template=    """
                You are summarizing multiple summaries from an educational document. 
                Combine the provided summaries into a single, cohesive summary that represents the entire document. 
                Focus on unifying key themes, concepts, and insights while avoiding redundancy.
                
                The Set of Summaries:
                {docs}
                
                Generated Summary:
                - **Main Idea:** Clearly state the primary purpose or theme of the document.
                - **Key Points:** Highlight the central insights, processes, or concepts from the document.
                - **Conclusion:** Summarize the overall takeaway or purpose of the document..
                        """
        return PromptTemplate.from_template(template)

    def _create_combine_documents_chain(self):
        """
        Create the chain for combining documents in the reduce phase.
        """
        return StuffDocumentsChain(llm_chain=self.reduce_chain, document_variable_name="docs")

    def _create_reduce_documents_chain(self):
        """
        Create the chain for reducing documents iteratively.
        """
        return ReduceDocumentsChain(
            combine_documents_chain=self.combine_documents_chain,
            collapse_documents_chain=self.combine_documents_chain,
            token_max=self.token_max,
        )

    def _create_map_reduce_chain(self):
        """
        Create the full Map-Reduce chain.
        """
        return MapReduceDocumentsChain(
            llm_chain=self.map_chain,
            reduce_documents_chain=self.reduce_documents_chain,
            document_variable_name="docs",
            return_intermediate_steps=False,
        )

    def generate_summary(self, documents):
        """
        Run the Map-Reduce pipeline on the provided documents.

        Args:
            documents (list[Document]): A list of Document objects to process.

        Returns:
            str: The final extracted insights.
        """
        return self.map_reduce_chain.invoke(documents)

class SummaryPipeline:
    """
    A pipeline to manage knowledge extraction and quiz generation from educational documents.
    """

    def __init__(self, source_name, map_llm="llama-3.1-8b-instant", reduce_llm="llama-3.1-8b-instant", token_max=5000):
        """
        Initialize the QuizPipeline.

        Args:
            source_name (str): The source name of the document.
            map_llm (str): The language model for the map phase.
            reduce_llm (str): The language model for the reduce phase.
            token_max (int): Maximum token limit for reducing documents.
            max_insights (int): Maximum number of insights to output.
        """
        self.source_name = source_name
        self.retriever = DocumentRetriever(source_name=source_name)
        self.knowledge_extractor = KnowledgeExtractor(
            map_llm=map_llm,
            reduce_llm=reduce_llm,
            token_max=token_max,
        )

    def process_documents(self):
        """
        Process the given documents to extract knowledge and generate quizzes.

        Returns:
            dict: A dictionary containing extracted insights and the generated quiz.
        """
        # Step 1: Retrieve documents
        print("Retrieving Documents...")
        documents = self.retriever.retrieve_all_chunks()

        # Step 2: Extract knowledge
        print("Extracting knowledge...")
        summary = self.knowledge_extractor.generate_summary(documents)


        # Return the generated quiz
        return summary.get("output_text")
