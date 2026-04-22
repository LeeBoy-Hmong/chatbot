''' The pipeline is the ochestrator. It'll call my files and push everything into Qdrant'''
from qdrant_client import QdrantClient, models
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Embedding with HuggingFaceEmbeddings - we are using model "multi-qa-MiniLM-L6-cos-v1"
    # Chosen this model for it's semantic search benchmark.
client = QdrantClient(
    url=os.getenv("QDRANT_CLUSTER_EP"),
    api_key=os.getenv("QDRANT_API")
)

print(client.get_collections())