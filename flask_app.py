import os
from flask import Flask, render_template, request, redirect, url_for #, session
from NEWS_API import fetch_news # Import de ta fonction externalisée

#from threads_api import get_me, get_threads, get_replies, get_insights

####################### Variables###################
project_folder = os.path.expanduser('/home/tsurubaso/mysite')  # adjust as appropriate
ARTICLES = []


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