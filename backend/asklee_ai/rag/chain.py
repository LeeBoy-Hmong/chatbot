'''The brain of AskLee AI. Takes the users question, retrieves relevant context from our Qdrant Collection, formats it
into a prompt, and passes to Ollama for generation. We will run a test on local computer prior to setting up the configurations
for the Jetson Nano Orin.'''
from retriever import get_retriever
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate as cpt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Initialize Ollama with ChatOllama
chat_llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0.3,  # Increase for creativity, but we need it to be more grounded - keep parameter lower (e.g. 0.2 - 0.3)
    num_ctx=4096,  # Window size - 4096 is pretty standard.
    num_predict=512,  # Cut off point at 512 token (approxitmately 384 words)
    top_p=0.9  # Nucleus Sampling - higher the percentage = higher the probability of most likely words that match.
)
# Build the prompt template. Use ChatPromptTemplate.from_template().
'''  Read me for further instructions...
    # A clear role definition for AskLee
    # {context} placeholder for retrieved chunks. {question} placeholder for user query.
    # An instruction to only answer from context.
'''
prompt_template = """
    You are an AI chatbot name AskLee, an assistant for customers or potential customers for GolieXeeGardens flea market website...
    Only use the following context to answer...
    If the answer is not in the context, state "I currently do not have that information"...
    
    Context: {context}
    User Questions: {question}
"""

chat_prompt = cpt.from_template(prompt_template)
# Wire the chain with LCEL

# Write a function to ask - takes a question string, invokes the chain, returns the response.