'''The brain of AskLee AI. Takes the users question, retrieves relevant context from our Qdrant Collection, formats it
into a prompt, and passes to Ollama for generation. We will run a test on local computer prior to setting up the configurations
for the Jetson Nano Orin.'''
from retriever import get_retriever
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate as cpt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Initialize Ollama with ChatOllama

# Build the prompt template. Use ChatPromptTemplate.from_template().
    # A clear role definition for AskLee
    # {context} placeholder for retrieved chunks. {question} placeholder for user query.
    # An instruction to only answer from context.

# Wire the chain with LCEL

# Write a function to ask - takes a question string, invokes the chain, returns the response.