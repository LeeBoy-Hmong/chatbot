from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
import os
from dotenv import load_dotenv

load_dotenv()

# Create a function to load the following path for 