# pinecone_handler.py
import pinecone

# Initialize Pinecone with your API key and environment
pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENVIRONMENT")

# Create a Pinecone index (or use an existing one)
index = pinecone.Index("ai-study-assistant")

# Function to insert vector data into Pinecone
def insert_vector_data(id: str, embeddings: list):
    """Insert the generated vector into Pinecone"""
    index.upsert([(id, embeddings)])

# Function to query Pinecone for similar vectors
def query_vector_data(query_vector: list, top_k: int = 5):
    """Query Pinecone for top K similar vectors"""
    results = index.query(query_vector, top_k=top_k, include_metadata=True)
    return results
