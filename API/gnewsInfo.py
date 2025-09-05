# gnews.py
from gnews import GNews

def fetch_gnews(query, lang="fr", country="FR", max_results=10):
    google_news = GNews(language=lang, country=country, max_results=max_results)
    articles = google_news.get_news(query)

    # Harmoniser le format pour ressembler à NewsAPI
    normalized_articles = []
    for a in articles:
        normalized_articles.append({
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "urlToImage": a.get("image"),   # ton template utilise urlToImage
            "publishedAt": a.get("published date"),
            "source": {"name": a.get("publisher", {}).get("title", "")}
        })
    return {"articles": normalized_articles}
