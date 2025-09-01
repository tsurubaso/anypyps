import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request ,redirect, url_for #, session
project_folder = os.path.expanduser('/home/tsurubaso/mysite')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))# Load variables from .env

NEWS_API_KEY = os.getenv('NEWS_API_KEY')  # Load from environment
if NEWS_API_KEY:
    print(f"Using NEWS_API_KEY: {NEWS_API_KEY[0:2]}...")
else:
    print("NEWS_API_KEY is not set!")

####################### Variables###################
NEWS_API_URL = 'https://newsapi.org/v2/everything'
cached_news = None
last_fetched_time = 0

# Temporary store for articles — you may use session or a database
ARTICLES = []

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

#######################processor for routes######
@app.context_processor
def inject_current_page():
    return dict(current_page=request.endpoint or "")

#######################Routes####################
@app.route("/", methods=["GET"])
def home():
    query = request.args.get("query", "").strip()
    articles = []

    if query:
        data = fetch_news(query=query)
        articles = data["articles"] if data and "articles" in data else []
        global ARTICLES
        ARTICLES = articles # Store fetched articles temporarily


    return render_template("home.html", articles=articles, query=query)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit_article(index):
    if index >= len(ARTICLES):
        return "Article not found", 404

    article = ARTICLES[index]

    if request.method == "POST":
        article['title'] = request.form.get("title", "")
        article['description'] = request.form.get("description", "")
        article['urlToImage'] = request.form.get("urlToImage", "")
        if 'source' not in article:
            article['source'] = {}
        article['source']['name'] = request.form.get("source", "")

        # After saving, redirect somewhere (e.g., back to edit or home)
        return redirect(url_for('edit_article', index=index))

    return render_template("edit_article.html", article=article, index=index)




##
if __name__ == '__main__':
    app.run(debug=True)