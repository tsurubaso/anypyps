#threads_api


#import requests deja dans flask.py
#import json deja dans flask.py
import sys
from pathlib import Path


# 👉 Mets ton token ici
ACCESS_TOKEN = ""


def fetch_data(url: str, params: dict, filename: str, check_key: str, message: str):
    """Generic function to call the API, check a key, print, and save to file."""
    response = requests.get(url, params=params)
    data = response.json()

    # Debug si jamais problème
    # print(json.dumps(data, indent=4))

    if isinstance(data, dict) and "error" in data:
        error_message = data.get("error", {}).get("message", "Unknown error occurred")
        print("⚠️ API error:", error_message)
        return None

    try:
        # Vérifie la clé pour savoir si la réponse est valide
        if check_key in json.dumps(data):
            print(f"{message}: {json.dumps(eval(check_key), ensure_ascii=False)}")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))
        else:
            print(f"⚠️ {message} not found in response.")
    except Exception as e:
        print("⚠️ Unexpected error:", e)

    return data


def get_me():
    url = "https://graph.threads.net/v1.0/me"
    params = {
        "fields": "id,username,name,threads_profile_picture_url,threads_biography,is_verified",
        "access_token": ACCESS_TOKEN
    }
    return fetch_data(url, params, "info_on_me.txt", "data['id']", "Your id is")


def get_threads(since="2025-08-20", until="2025-08-26"):
    url = f"https://graph.threads.net/v1.0/me/threads"
    params = {
        "fields": "id,media_product_type,media_type,media_url,permalink,owner,username,text,topic_tag,timestamp,shortcode,thumbnail_url,children,is_quote_post,link_attachment_url,reposted_post",
        "since": since,
        "until": until,
        "limit": 20,
        "access_token": ACCESS_TOKEN
    }
    return fetch_data(url, params, "info_posts.txt", "data['data'][0]['id']", "First post id")


def get_replies(since="2025-07-01", until="2025-08-26"):
    url = "https://graph.threads.net/v1.0/me/replies"
    params = {
        "fields": "id,media_product_type,media_type,media_url,permalink,username,text,topic_tag,timestamp,shortcode,thumbnail_url,children,is_quote_post,has_replies,root_post,replied_to,is_reply,is_reply_owned_by_me,reply_audience",
        "since": since,
        "until": until,
        "limit": 20,
        "access_token": ACCESS_TOKEN
    }
    return fetch_data(url, params, "reponse_aux_posts.txt", "data['data'][0]['id']", "First reply id")


def get_insights(post_id="24335771116092512"):
    url = f"https://graph.threads.net/v1.0/{post_id}/threads_insights"
    params = {
        "metric": "views,likes,reposts",
        "access_token": ACCESS_TOKEN
    }
    return fetch_data(url, params, "insights.txt", "data['data'][0]['name']", "Metric name")


def main():
    if not ACCESS_TOKEN:
        print("⚠️ Please set your ACCESS_TOKEN in the script.")
        sys.exit(1)

    Path(".").mkdir(parents=True, exist_ok=True)

   # print("\n=== Fetching user info ===")
   # get_me()

   # print("\n=== Fetching threads ===")
   # get_threads()

   # print("\n=== Fetching replies ===")
   # get_replies()

   # print("\n=== Fetching insights ===")
   # get_insights()



