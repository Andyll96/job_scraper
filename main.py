import requests
import os
import json
from datetime import datetime, timezone 
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
STUDIOS_DB_ID = os.getenv('STUDIOS_DB_ID')
JOB_POSTINGS_DB_ID = os.getenv('JOB_POSTINGS_DB_ID')

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_pages(num_pages=None):
    """If num_pages is None, get all pages, otherwise just the defined number

    Args:
        num_pages (int, optional): number of desired pages. Defaults to None.
    """
    url = f"https://api.notion.com/v1/databases/{STUDIOS_DB_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{STUDIOS_DB_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    return results

get_pages()