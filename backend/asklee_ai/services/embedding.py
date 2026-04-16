from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

chat_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_model(text: str):
    return chat_model.encode(text)

# vector = chat_model.encode("How many carrot grows on trees.")
# print(len(vector))