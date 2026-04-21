from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_content_wp():
# Use requests to hit the BetterDocs REST endpoint. The API is paginated, look into 'per_page' and page query 'params' on WP REST.
    betterdocs = requests.get(os.getenv("BETTERDOCS_REST"))
    data_content = []
    current_pg = 1
# Loop through pages until no results return.
    while True:
        parameters = {
            "page" : current_pg,
            "per_page" : 100
        }

        paginated_url = f"{betterdocs}?page={parameters['page']}"
        print(f"Retrieving: {betterdocs}")
        # Retrieve 404 error/redirect if page does not exist.
        if betterdocs.response_status != 200 or len(betterdocs.text) < 500:
            pass
# Collect and extract data from the JSON. If there is no data, then stop.
        data = betterdocs.json()
        if not data:
            break

# Strip HTML from 'content.rendered' before returning.

# Return a list of clean dictionaries.