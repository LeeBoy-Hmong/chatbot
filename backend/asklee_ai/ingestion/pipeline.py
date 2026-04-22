''' The pipeline is the ochestrator. It'll call my files and push everything into Qdrant'''
from chunker import chunk_doc
from qdrant_client import QdrantClient, models
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_CLUSTER_EP"),
    api_key=os.getenv("QDRANT_API")
)
print(client.get_collections())

# Initialize Embedding with HuggingFaceEmbeddings - we are using model "multi-qa-MiniLM-L6-cos-v1"
    # Chosen this model for it's semantic search benchmark.
m_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
m_kwargs = {"device": "cpu"}
en_kwargs = {"normalize_embeddings": True}  # True, ensures cosine similarity works correctly. Giving more consistent search results especially for semantic RAG systems.
embeddings = HuggingFaceEmbeddings(
    model_name=m_name,
    model_kwargs=m_kwargs,
    encode_kwargs=en_kwargs
)




