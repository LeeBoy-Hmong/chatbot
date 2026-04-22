from loader import get_content_wp
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Create an instance of RecursiveTextSplitter with basic params to research.
txt_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50,
    length_function=len
)
# Write out a function with the data content that was obtained from loader.py
def chunk_doc(data_content):
    data_t = [{"Title": dat["Title"]} for dat in data_content]  # Loop through the iteraction of the content - list dictionary (metadata)
    data_c = [dat["Content"] for dat in data_content]  # Loop through the iteraction of the content
    # Pass the content string through the splitter user .create_documents(). This method takes raw string data and turn it into documents.
    doc = txt_splitter.create_documents(texts=data_c,
                                        metadatas=data_t)  # Metas need to be a list dictionary. Second argument of .create_documents() accepts as list of metadata dicts. Pass the Title here.
    # Extend the results with returned chunks
    return doc

# Return the chunks (full list of Document objects). Langchain documents - .page_content & .metadata

if __name__ == "__main__":
    print(chunk_doc(get_content_wp()))