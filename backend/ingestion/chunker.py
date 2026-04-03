from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunker(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= 500,
        chunk_overlap= 100
    )
    chunked_docs = text_splitter.split_documents(documents)
    return chunked_docs