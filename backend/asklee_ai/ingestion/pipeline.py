''' The pipeline is the ochestrator. It'll call my files and push everything into Qdrant'''
# from chunker import chunk_doc
from qdrant_client.models import VectorParams, Distance, PointStruct as PS
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from chunker import chunk_doc
from loader import get_content_wp
import os
from dotenv import load_dotenv
load_dotenv()

q_client = QdrantClient(
    url=os.getenv("QDRANT_CLUSTER_EP"),
    api_key=os.getenv("QDRANT_API")
)

# Initialize Embedding with HuggingFaceEmbeddings - we are using model "multi-qa-MiniLM-L6-cos-v1"
    # Chosen this model for it's semantic search benchmark.
m_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
m_kwargs = {"device": "cpu"}
en_kwargs = {"normalize_embeddings": True}  # True, ensures cosine similarity works correctly. Giving more consistent search results especially for semantic RAG systems.
embeddings = HuggingFaceEmbeddings(  # Pass this object to your upsert.
    model_name=m_name,
    model_kwargs=m_kwargs,
    encode_kwargs=en_kwargs
)

dimension = len(embeddings.embed_query("testing"))  # Retrieve the dimension without having to guess the size. Pass it through the collection, size parameter.
print(dimension)
# Create a collection for the Qdrant vector database.
collection_doc = "GolieXeeGardens_docs"
if not q_client.collection_exists(collection_doc):
    q_client.create_collection(
        collection_name=collection_doc,
        vectors_config=VectorParams(size=dimension, distance=Distance.COSINE))
# Insert the vector into a collection. Utilizing QdrantVectorStore.from_documents()
# Do not use PointStruct if we are using LangChain.
lang_doc = chunk_doc(get_content_wp())
QdrantVectorStore.from_documents(
    documents=lang_doc,
    embedding=embeddings,  # Pass the initialized 'embeddings' object created.
    url=os.getenv("QDRANT_CLUSTER_EP"),
    api_key=os.getenv("QDRANT_API"),
    collection_name=collection_doc
)



