'''The retriever connects to the Qdrant collection and converts it into a LangChain retriever object,
so that the RAG chain can retrieve against. It is the read side of Qdrant, the pipeline was the write side.
We are opening a connection to query them.'''
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the same embedding model. Must be the exact same as the pipeline.
m_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
m_kwargs = {"device":"cpu"}
en_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceEmbeddings(
    model_name=m_name,
    model_kwargs=m_kwargs,
    encode_kwargs=en_kwargs
    )
# Connect the existing Qdrant Collection. Use "QdrantVectorStore" - initialize with 'client=', 'collection_name=', and 'embedding='.
    # Not the same as used with the ".from_documents()" method.
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="GolieXeeGardens_docs",
    url=os.getenv("QDRANT_CLUSTER_EP"),
    api_key=os.getenv("QDRANT_API")
    )
# Write a retriever function. Convert the vector store to a retriever using ".as_retriever()" method.
    # In the method, use search_type="similarity" & search_kwargs={"k":3}.
def get_retriever():
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k":5}  # retrieve the top 5 most similar data chunks.
    )
    return retriever

if __name__ == "__main__":
    print(get_retriever())
