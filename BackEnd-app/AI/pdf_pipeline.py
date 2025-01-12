from dotenv import load_dotenv
import fitz  #
import base64
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
import nest_asyncio
from pathlib import Path
from langchain_pinecone import Pinecone
import os
from langchain_community.embeddings import FastEmbedEmbeddings
import uuid
from concurrent.futures import ThreadPoolExecutor
from langchain.text_splitter import RecursiveCharacterTextSplitter
import asyncio


# Enable nested event loops
nest_asyncio.apply()



class PDFImageExtractor:
    """
    Handles PDF operations such as extracting images from pages and converting them to base64 format.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def get_image_pages(self):
        """
        Extract images from all pages of the PDF and return them as a dictionary.
        
        Returns:
            dict: A dictionary with page numbers as keys and base64-encoded images as values.
        """

        # Open the PDF file
        pdf_file = fitz.open(self.file_path)
        
        # Dictionary to store base64-encoded images (key: page number, value: base64 image)
        base64_images = {}
        
        # STEP 3: Iterate over PDF pages
        for page_index in range(len(pdf_file)):
            # Get the page itself
            page = pdf_file.load_page(page_index)  # Load the page
            image_list = page.get_images(full=True)  # Get images on the page
            # Print the number of images found on this page
            if image_list:
                # Render the page as an image (PNG format)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # High resolution
                image_bytes = pix.tobytes("png")  # Convert to PNG bytes
        
                # Convert the image to base64
                base64_image = base64.b64encode(image_bytes).decode("utf-8")
        
                # Add the base64 image to the dictionary with the page number as the key
                base64_images[page_index] = base64_image

        return base64_images

class VisualizationSummarizer:
    """
    Summarizes visualizations in images using the ChatGroq model.
    """
    def __init__(self):
        self.chat_model = ChatGroq(
            model="llama-3.2-90b-vision-preview",
            temperature=0
        )

    def get_visualization_summary(self, pages):
        """
        Generate summaries for visualizations in a set of images.

        Args:
            pages (dict): A dictionary of base64-encoded images with page numbers as keys.

        Returns:
            dict: A dictionary with page numbers as keys and visualization summaries as values.
        """
        pages_numbers = list(pages.keys())
        images = [pages[i] for i in pages_numbers]

        prompt_template = """
        You will be provided with an image of a page from an educational document.

        If the image contains a visualization:
            return the following details:
            1. The title of the visualization.
            2. The axes labels or other relevant axis information (e.g., "X-axis: Time, Y-axis: Value").
            3. Any numbers present in the visualization, including specific data points, percentages, or values.
            4. A clear and standalone summary of the insights taken from the visualization. Ensure the summary is written in one paragraph format, and it must begin with: 'The Page Contains'.


        If the image does not contain an educational visualization (e.g., graph, chart, or diagram):
            only return: "The Page Has No Visualization".  
        """

        messages = [
            (
                "user",
                [
                    {"type": "text", "text": prompt_template},
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:image/jpeg;base64,{image}"},
                    },
                ],
            )
        ]

        chain = ChatPromptTemplate.from_messages(messages) | self.chat_model | StrOutputParser()
        image_summaries = chain.batch(images, config={"max_concurrency": 5})

        return {pages_numbers[i]: summary for i, summary in enumerate(image_summaries)}

class TextSplitter:
    """
    Processes text by splitting it into manageable chunks with optional overlap.
    """
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def process_single_page(self, entry):
        """
        Process a single page's text and split it into chunks with page references.

        Args:
            entry (dict): A dictionary containing page number and page content.

        Returns:
            list: A list of text chunks with page references.
        """
        page_number = entry['page']
        page_text = entry['page_content']['Text'] + "\n" + entry['page_content']['Visualization']
        chunks = self.text_splitter.split_text(page_text)
        return [f"Page {page_number}: {chunk}" for chunk in chunks]

    def process_all_pages_concurrently(self, pages_with_summaries):
        """
        Process all pages concurrently to split text into chunks.

        Args:
            pages_with_summaries (list): A list of dictionaries containing page content and summaries.

        Returns:
            list: A list of text chunks with page references.
        """
        chunks_with_page_reference = []
        with ThreadPoolExecutor() as executor:
            results = executor.map(self.process_single_page, pages_with_summaries)
            for result in results:
                chunks_with_page_reference.extend(result)
        return chunks_with_page_reference

class PineconeManager:
    """
    Manages interactions with the Pinecone vector database, including adding text embeddings.
    """
    def __init__(self, index_name):
        self.pc = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5"),
            text_key="text"
        )

    def add_to_index(self, source_file_name,chunks_with_page_reference):
        """
        Add text chunks to the Pinecone index with associated metadata.

        Args:
            chunks_with_page_reference (list): A list of text chunks with page references.
        """
        metadatas = [{"source": str(Path(source_file_name).name), "id": str(uuid.uuid4())} for _ in chunks_with_page_reference]
        for i in range(0, len(chunks_with_page_reference), 100):
            batch_texts = chunks_with_page_reference[i:i + 100]
            batch_metadatas = metadatas[i:i + 100]
            self.pc.add_texts(texts=batch_texts, metadatas=batch_metadatas)

class PDFPipeline:
    """
    Orchestrates the entire PDF processing pipeline, including image extraction, summarization,
    text processing, and indexing into Pinecone.
    """
    def __init__(self, file_path,  pinecone_index="gradproject"):
        self.pdf_handler = PDFImageExtractor(file_path)
        self.visualization_summarizer = VisualizationSummarizer()
        self.text_processor = TextSplitter()
        self.pinecone_handler = PineconeManager(pinecone_index)
        self.pages_with_summaries = []

    async def load_pages_with_summaries(self, loader, summary):
        async for page in loader.alazy_load():
            page_number = page.metadata['page']
            if page_number in summary:
                self.pages_with_summaries.append({
                    "page": page_number + 1,
                    "page_content": {
                        "Text": page.page_content,
                        "Visualization": summary[page_number],
                    },
                })
            else:
                self.pages_with_summaries.append({
                    "page": page_number + 1,
                    "page_content": {
                        "Text": page.page_content,
                        "Visualization": "The Page Has No Visualization.",
                    },
                })

    async def run(self):
        pages = self.pdf_handler.get_image_pages()
        print("images extraction is done")
        summary = self.visualization_summarizer.get_visualization_summary(pages)
        print("images Summarization is done")
        loader = PyPDFLoader(self.pdf_handler.file_path)

        # Load pages asynchronously
        await self.load_pages_with_summaries(loader, summary)
        print("Loading pages with summaries is done")    
        # Process and split text
        chunks_with_page_reference = self.text_processor.process_all_pages_concurrently(self.pages_with_summaries)
        print("Text processing is done")
        # Add to Pinecone
        self.pinecone_handler.add_to_index(self.pdf_handler.file_path,chunks_with_page_reference)
        print("Pipeline completed successfully.")




