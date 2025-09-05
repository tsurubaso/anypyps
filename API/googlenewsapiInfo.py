# google_news_api_wrapper.py
import os
from dotenv import load_dotenv
from google_news_api import GoogleNewsApi

# Charger les variables d'environnement
load_dotenv()
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def fetch_google_news_api(query, lang="fr", country="FR", max_results=10):
    # Instancier le client avec la clé API
    client = GoogleNewsApi(api_key=GNEWS_API_KEY)

    # Récupérer les articles
    data = client.get_news(
        query=query,
        language=lang,
        country=country,
        max=max_results
    )

    # Normaliser le format pour coller à ton template
    normalized_articles = []
    for a in data.get("articles", []):
        normalized_articles.append({
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "urlToImage": a.get("image"),
            "publishedAt": a.get("publishedAt"),
            "source": {"name": a.get("source", {}).get("name", "")}
        })

    return {"articles": normalized_articles}
