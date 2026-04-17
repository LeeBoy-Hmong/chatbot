# Chatbot
RAG Chatbot for 'GolieXeeGardens' website.

# Why:
This is one of the projects on for my parents website. Along with augmenting the UI of the site, this will help me develop better skills in AI. A RAG (Retrieval Augmented Generator) is one of my most popular AI Frameworks - embedding it into a chatbot to help my users with FAQ (Frequently Asked Questions) and help the team collect data.

# Stack
## Frontend
Utilize HTML, CSS, and JavaScript to create a chat widget.
## Backend
Python is the main programming language for the backend. FASTAPI framework is utilize for as my API. The vector database will be Qdrant for further scaling purposes if need be. Will be hosted on Render for free usage and overlapped with the website.
## Knowledge Storage
SupaBase is a backend service that utilize PostGresSQL as it's database core. BetterDocs is a documentation/knowledge base solution for Hostinger, it provides a REST API that allow my connection 
## Embeddings & Language Model
Will be run locally on a Jetson Nano Orin (8GB RAM) on a Ollama model. Will Utilize the Open-Source Framework *Setence Transformers* for embedding.
