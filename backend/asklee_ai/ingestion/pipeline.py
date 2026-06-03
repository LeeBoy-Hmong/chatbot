''' The pipeline is the orchestrator. It'll call my files and push everything into Qdrant'''
# from chunker import chunk_doc
from qdrant_client.models import VectorParams, Distance, PointStruct as PS
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from chunker import chunk_doc
from loader import get_content_wp
import os
from dotenv import load_dotenv

load_dotenv()

def qdrant_pipeline():
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
    # print(dimension)
    # Create a collection for the Qdrant vector database.
    collection_doc = "GolieXeeGardens_docs"  # Created this varidable be the collection was used multiple times.

    if not q_client.collection_exists(collection_doc):
        q_client.create_collection(
            collection_name=collection_doc,
            vectors_config=VectorParams(size=dimension, distance=Distance.COSINE))

    lang_doc = chunk_doc(get_content_wp())
    # Get existing titles from Qdrant - collect all Title values, if already stored in our payload.
    points, _ = q_client.scroll(collection_name=collection_doc,
                                    with_payload=True,
                                    limit=150)
    # Create a filter variable for new documents - return the docs, filter out any whose Title already existing in Qdrant.
    all_docs: list[Document] = lang_doc   # Applied Type Hints: avoid pylance errors
    existent_titles: set[str] = {point.payload["metadata"]["title"] for point in points}  # Qdrant stores metadata (payload) in lowercase. So pull with lowercase.
    new_docs = [docs for docs in all_docs if docs.metadata["title"] not in existent_titles]
    # Only chunk and upsert new docs - Pass the new documents into chunk_doc() instead of docs. If new documents are empty, skip it entirely.
    if not new_docs:
        print("There were no new documents ingested.")
        return
    # Insert the vector into a collection. Utilizing QdrantVectorStore.from_documents() - Do not use PointStruct if we are using LangChain.
    QdrantVectorStore.from_documents(
        documents=new_docs,  #  Previously lang_doc
        embedding=embeddings,  # Pass the initialized 'embeddings' object created.
        url=os.getenv("QDRANT_CLUSTER_EP"),
        api_key=os.getenv("QDRANT_API"),
        collection_name=collection_doc
    )

    return "Qdrant pipeline completed successfully"

if __name__ == "__main__":
    print(qdrant_pipeline())