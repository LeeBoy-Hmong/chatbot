from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from bs4 import BeautifulSoup as bs
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_content_wp():
# Use requests to hit the BetterDocs REST endpoint. The API is paginated, look into 'per_page' and page query 'params' on WP REST.
    betterdocs = os.getenv("BETTERDOCS_REST")
    data_content = []
    current_pg = 1
# Loop through pages until no results return.
    while True:
        response = requests.get(betterdocs, params={"page": current_pg, "per_page": 100})
        print(f"Retrieving: {betterdocs}")
        # Retrieve 404 error/redirect if page does not exist.
        if response.status_code != 200 or len(response.text) < 500:
            break
# Collect and extract data from the JSON. If there is no data, then stop.
        data = response.json()
        
        for doc in data:
            title = doc["title"]["rendered"]
            content = doc["content"]["rendered"]
        
            current_pg += 1  # Continue to increment through the pages.
# Strip HTML from 'content.rendered' before returning.
            souped_title = bs(title, 'html.parser').get_text(separator=" ")
            souped_content = bs(content, 'html.parser').get_text(separator=" ")
# Return a list of clean dictionaries.
            combined_soup = data_content.append({
                "Title" : souped_title,
                "Content": souped_content
            })

            return combined_soup

    
print(get_content_wp())


# import os
# import requests

# test_betterdocs = os.getenv("BETTERDOCS_REST")
# print("Endpoint:", repr(test_betterdocs))

# page = requests.get(test_betterdocs)
# data = page.json()
# print(type(data))
# print(len(data))
# for doc in data:
#     title = doc["title"]
#     content = doc["content"]

# print(content)