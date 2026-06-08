'''The brain of AskLee AI. Takes the users question, retrieves relevant context from our Qdrant Collection, formats it
into a prompt, and passes to Ollama for generation. We will run a test on local computer prior to setting up the configurations
for the Jetson Nano Orin.'''
from asklee_ai.rag.retriever import get_retriever
from langchain_ollama import ChatOllama
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate as cpt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_postgres import PostgresChatMessageHistory
from operator import itemgetter
import psycopg
import uuid
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Ollama with ChatOllama
chat_llm = ChatOllama(
    model="llama3.2:3b",
    base_url="http://10.0.0.242:11434",
    temperature=0.4,  # Increase for creativity, but we need it to be more grounded - keep parameter lower (e.g. 0.2 - 0.3)
    num_ctx=5120,  # Window size - 4096 is pretty standard.
    num_predict=512,  # Cut off point at 512 token (approxitmately 384 words)
    top_p=0.9,  # Nucleus Sampling - higher the percentage = higher the probability of most likely words that match.
    repeat_penalty= 1.1  # Added to see if this can assist with preventing the looping from happening. 
)
# Build the prompt template. Use ChatPromptTemplate.from_template().
'''  Read me for further instructions...
    # A clear role definition for AskLee
    # {context} placeholder for retrieved chunks. {question} placeholder for user query.
    # An instruction to only answer from context.
'''
prompt_template = """
You are 'AskLee AI', an assistant for GolieXee Gardens flea market website. Introduce yourself if prompt to by the customer (user), otherwise continue to the rules below.

Rules:
1. Answer only the user's latest question.
2. Use chat history only to understand references such as "they", "those", "that", or "yes".
3. Do not repeat previous assistant answers.
4. Do not repeat product lists unless the user asks for product lists.
5. Use only the Context to answer.
6. If the answer is not in the Context, say: "I currently do not have that information. Please contact info@goliexeegardens.com."
7. AskLee AI represents GolieXee Gardens. Interpret customer phrases like “you,” “your,” “you guys,” or “your prices” as referring to GolieXee Gardens. Respond in third person using “GolieXee Gardens,” “the business,” or “the team,” rather than speaking as “I” or “we.”

Chat History:
{chat_history}

Context:
{context}

Latest User Question:
{question}

Answer:
"""
chat_prompt = cpt.from_template(prompt_template)
### Was added in to fix LLM issue - need to format the LangChain Docs to string. LLM is only currently reading strings.
def formatter(docs):
    return "\n\n".join(doc.page_content for doc in docs)

token_counter = lambda messages: sum(len(m.content.split()) for m in messages)

'''
# message_trimmer = trim_messages(
#     max_tokens=400,
#     token_counter=token_counter,
#     strategy="last",
#     allow_partial=False,
#     include_system=True
# ) '''

# Created a function to trim down the history that the conversation will hold.
def message_trimmer(message):
    limit = 4
    
    if not message:
        return []
    return message[-limit:]
# Use RunnableLambda so that we may run the custom function.
trimmer = RunnableLambda(message_trimmer)

# Wire the chain with LCEL
rag_chain = {"context": itemgetter("question") | get_retriever() | formatter, 
"question": itemgetter("question"),
"chat_history": itemgetter("chat_history") | trimmer} | chat_prompt | chat_llm | StrOutputParser()

# Wrap the chain in a memory function. Use 'RunnableWithMessageHistory'.
def retrieve_session_hist(session_identification: str):
    supabase_connection = psycopg.connect(os.getenv("SUPABASE_CONNECTION"))
    return PostgresChatMessageHistory(
        "message_history",
        session_identification,
        sync_connection=supabase_connection,
    )

chain_with_hist = RunnableWithMessageHistory(
    rag_chain,
    retrieve_session_hist,
    input_messages_key="question",
    history_messages_key="chat_history"
)

session_id = str(uuid.uuid4())
# Write a function to ask - takes a question string, invokes the chain, returns the response.
def rag_response():
    '''# Generate the session id prior to the loop.
    session_id = str(uuid.uuid4())'''
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            break

        ai_response = chain_with_hist.invoke(
            {"question": query},
            config={"configurable": {"session_id": session_id}})
        
        print(f"Session ID: {session_id}")
        print(f"\nAskLee AI: {ai_response}")

if __name__ == "__main__":
    (rag_response())