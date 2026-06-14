# Testing file for my Cloudflared tunnel connection.
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

# Create an instance for the ChatOllama - same as the real pipe.
slm = ChatOllama(
    model="llama3.2:3b",
    base_url=os.getenv("CF_CLIENT_URL"),
    temperature=0.4,  # Increase for creativity, but we need it to be more grounded - keep parameter lower (e.g. 0.2 - 0.3)
    num_ctx=5120,  # Window size - 4096 is pretty standard. 5120
    num_predict=512,  # Cut off point at 512 token (approxitmately 384 words)
    top_p=0.9,  # Nucleus Sampling - higher the percentage = higher the probability of most likely words that match.
    repeat_penalty= 1.1,  # Added to see if this can assist with preventing the looping from happening.
    client_kwargs={
        "headers": {
            "CF-Access-Client-Id": os.getenv("CF_CLIENT_ID"),
            "CF-Access-Client-Secret": os.getenv("CF_CLIENT_SECRET")
        }
    }
)
# invoke a response
model_reponse = slm.invoke("Reply with: 'Tunnel is working on Cloudflare End'")
# print the response
print(model_reponse)