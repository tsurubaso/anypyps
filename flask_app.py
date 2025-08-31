import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
project_folder = os.path.expanduser('/home/tsurubaso/mysite')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))# Load variables from .env
#load_dotenv() This is not working on AnywherePy
NEWS_API_KEY = os.getenv('NEWS_API_KEY')  # Load from environment
if NEWS_API_KEY:
    print(f"Using NEWS_API_KEY: {NEWS_API_KEY[0:2]}...")
else:
    print("NEWS_API_KEY is not set!")

####################### Variables###################
NEWS_API_URL = 'https://newsapi.org/v2/everything'
cached_news = None
last_fetched_time = 0

#######################Functions####################
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
        'language': 'en',  # tu peux adapter selon ton public
        'pageSize': 10,
        'sortBy': 'publishedAt'  # optional: sorts news by newest first
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
##
app = Flask(__name__)

#######################Routes####################
@app.route("/", methods=["GET"])
def home():
    query = request.args.get("query", "").strip()

    data = fetch_news(query=query)
    articles = []

    if query:
        data = fetch_news(query=query)
        articles = data["articles"] if data and "articles" in data else []


    return render_template("home.html", articles=articles, query=query,current_page='home')

@app.route('/about')
def about():
    return render_template('about.html', current_page='about')

##
if __name__ == '__main__':
    app.run(debug=True)