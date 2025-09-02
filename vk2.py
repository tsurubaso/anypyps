import requests
import json


# 👉 Mets ton token ici
ACCESS_TOKEN = ""
API_VERSION = "5.199"


def vk_request(method: str, params: dict, filename: str = None):
    """Generic VK API request + save to file if needed."""
    url = f"https://api.vk.com/method/{method}"
    params["access_token"] = ACCESS_TOKEN
    params["v"] = API_VERSION

    response = requests.post(url, params=params)
    data = response.json()

    # Debug
    # print(json.dumps(data, indent=4, ensure_ascii=False))

    if "error" in data:
        error_msg = data["error"].get("error_msg", "Unknown error")
        print(f"⚠️ VK API Error: {error_msg}")
        return None

    if filename:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

    return data


def post_message(owner_id: str, message: str):
    """Post a message to a wall (user or group)."""
    params = {
        "owner_id": owner_id,  # user id (sans '-') ou -group id
        "message": message
    }
    return vk_request("wall.post", params, "vk_wall_post.txt")


def get_user_info(user_ids: str):
    """Get VK user info (id, name, photo, etc.)."""
    params = {
        "user_ids": user_ids,
        "fields": "photo_max,city,verified"
    }
    return vk_request("users.get", params, "vk_user_info.txt")


def get_wall(owner_id: str, count: int = 5):
    """Get latest wall posts."""
    params = {
        "owner_id": owner_id,
        "count": count
    }
    return vk_request("wall.get", params, "vk_wall.txt")
