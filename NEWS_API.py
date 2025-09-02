# News_api.py
import os
from dotenv import load_dotenv
import requests

####################### Variables ###################
project_folder = os.path.expanduser('/home/tsurubaso/mysite')  # à adapter si besoin
load_dotenv(os.path.join(project_folder, '.env'))  # Charge les variables .env

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = 'https://newsapi.org/v2/everything'

if NEWS_API_KEY:
    print(f"[News_api] Using NEWS_API_KEY: {NEWS_API_KEY[0:2]}...")
else:
    print("[News_api] NEWS_API_KEY is not set!")

####################### Fonction principale ###################
def fetch_news(query=None):
    if not NEWS_API_KEY:
        print("Error: NEWS_API_KEY is not set.")
        return None

    if not query:
        print("No query provided.")
        return None

    params = {
        'apiKey': NEWS_API_KEY,
        'q': query,
        'language': 'en',
        'pageSize': 10,
        'sortBy': 'publishedAt'
    }

    try:
        response = requests.get(NEWS_API_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching news: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"💥 Request failed: {e}")
        return None
