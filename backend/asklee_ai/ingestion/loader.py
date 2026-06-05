from bs4 import BeautifulSoup as bs
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_content_wp():
# Use requests to hit the BetterDocs REST endpoint. The API is paginated, look into 'per_page' and page query 'params' on WP REST.
    username = os.getenv("BETTERDOCS_USERNAME")
    password = os.getenv("APP_PASSWORD")
    betterdocs = os.getenv("BETTERDOCS_REST")
    data_content = []
    current_pg = 1
# Loop through pages until no results return.
    while True:
    # Set up and authentication header - Define the parameters to include the private post.
        params = {
            "page": current_pg,
            "status": "private, publish",
            "per_page": 100
        }
        response = requests.get(betterdocs,
                                auth=(username, password),
                                params=params)
        print(f"Retrieving: {current_pg}")  # Ensure I see the page that is getting cycled.
        # Retrieve 404 error/redirect if page does not exist.
        if response.status_code != 200 or len(response.text) < 500:
            break
# Collect and extract data from the JSON. If there is no data, then stop.
        data = response.json()
        if not data:
            break
        
        for doc in data:
            title = doc["title"]["rendered"]
            content = doc["content"]["rendered"]
# Parse and strip HTML from 'content.rendered' before returning.
            souped_title = bs(title, 'html.parser').get_text(separator=" ", strip=True)
            souped_content = bs(content, 'html.parser').get_text(separator=" ", strip=True)
# Return a list of clean dictionaries.
            data_content.append({
                "title" : souped_title,
                "content": souped_content
            })
        current_pg += 1  # Continue to increment through the pages.
    return data_content

if __name__ == "__main__":   
    print(get_content_wp())
