import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "articles")


def list_articles():
    articles = []
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        return articles

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                articles.append(data)
    articles.sort(key=lambda x: x["date"], reverse=True)
    return articles


def get_article(article_id):
    file_path = os.path.join(DATA_DIR, f"{article_id}.json")
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_next_id():
    existing_ids = []
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        return 1
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            article_id = int(filename.replace(".json", ""))
            existing_ids.append(article_id)
    if not existing_ids:
        return 1
    return max(existing_ids) + 1


def create_article(title, content, date_str):
    article_id = get_next_id()
    article = {
        "id": article_id,
        "title": title.strip(),
        "content": content.strip(),
        "date": date_str.strip() or datetime.now().strftime("%Y-%m-%d"),
    }
    file_path = os.path.join(DATA_DIR, f"{article_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(article, f, indent=4)
    return article_id


def update_article(article_id, title, content, date_str):
    file_path = os.path.join(DATA_DIR, f"{article_id}.json")
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["title"] = title.strip()
    data["content"] = content.strip()
    data["date"] = date_str.strip() or data["date"]

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return True


def delete_article(article_id):
    file_path = os.path.join(DATA_DIR, f"{article_id}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
