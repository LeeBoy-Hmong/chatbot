import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_documents():
    user = os.getenv("BETTERDOCS_USERNAME")
    password = os.getenv("APP_PASSWORD")
    website =  os.getenv("BETTERDOCS_REST")

    params = {
        "status": "private, publish",  # Do not pass as a list - just pass it with a comma - REST API can't read list in betterdocs.
        "per_page": 100
    }

    # headers = {
    #     "User-Agent": "Mozilla/5.0",
    #     "Accept": "application/json"
    # }

    response = requests.get(website,
                            auth=(user, password),
                            params=params)

    if response.status_code == 200:
        documents = response.json()
        print(f"Here are your private your documents\n{(documents)}.")
    else:
        print(f"Failed to connect {response.status_code} error, try again later.")
        print(response.text)

test_documents()