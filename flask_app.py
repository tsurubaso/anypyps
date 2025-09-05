import os
from flask import Flask, render_template, request, redirect, url_for #, session
from NEWS_API import fetch_news # Import de ta fonction externalisée
from gnewsInfo import fetch_gnews
from googlenewsapiInfo import fetch_google_news_api
#from threads_api import get_me, get_threads, get_replies, get_insights

####################### Variables###################
project_folder = os.path.expanduser('/home/tsurubaso/mysite')  # adjust as appropriate
ARTICLES = []
ARTICLES_GNEWS = []
ARTICLES_GNAPI = []


##
app = Flask(__name__)

#######################processor for routes######
@app.context_processor
def inject_current_page():
    return dict(current_page=request.endpoint or "")

#######################Routes####################

##Home
@app.route("/", methods=["GET"])
def  home():
    query = request.args.get("query", "").strip()
    articles = []

    if query:
        data = fetch_news(query=query)
        articles = data["articles"] if data and "articles" in data else []
        global ARTICLES
        ARTICLES = articles # Store fetched articles temporarily

    return render_template("home.html", articles=articles, query=query,source_api="NewsAPI.org")

## about
@app.route('/about')
def about():
    return render_template('about.html')

##Edit page
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

##GN
@app.route("/GN", methods=["GET"])
def  GN():
    query = request.args.get("query", "").strip()
    articles = []

    if query:
        data = fetch_gnews(query=query)
        articles = data["articles"] if data and "articles" in data else []
        global ARTICLES_GNEWS
        ARTICLES_GNEWS = articles# Store fetched articles temporarily

    return render_template("GN.html", articles=articles, query=query, source_api="GNews")

##GNAPI
@app.route("/GNAPI", methods=["GET"])
def  GNAPI():
    query = request.args.get("query", "").strip()
    articles = []

    if query:
        data = fetch_google_news_api(query, lang="fr", country="FR", max_results=10)
        articles = data["articles"] if data and "articles" in data else []
        global ARTICLES_GNAPI
        ARTICLES_GNAPI = articles # Store fetched articles temporarily

    return render_template("GNAPI.html", articles=articles, query=query, source_api="Google News API")


##
if __name__ == '__main__':
    app.run(debug=True)