import requests
import os
import json
import logging.config
import pathlib
from datetime import datetime, timezone 
from dotenv import load_dotenv
from scrape import scrape_website

load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
STUDIOS_DB_ID = os.getenv('STUDIOS_DB_ID')
JOB_POSTINGS_DB_ID = os.getenv('JOB_POSTINGS_DB_ID')

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

logger = logging.getLogger("my_app")

def setup_logging():
    config_file = pathlib.Path('configs/logging/config.json')
    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)

def get_pages(num_pages=None):
    """Gets all pages from Studios database.

    Args:
        num_pages (int, optional): number of desired pages. Defaults to None. If None, get all pages

    Returns:
        dict: reduced dictionary that contains studios active status and urls
    """
    url = f"https://api.notion.com/v1/databases/{STUDIOS_DB_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    logger.debug(json.dumps(data, indent=4))
    try:
        raw_data = data["results"]
    except KeyError:
        logger.error("Unable to find 'results' key in raw_data")

    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{STUDIOS_DB_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        raw_data.extend(data["results"])

    # dump raw data to json file
    # with open('raw_db.json', 'w', encoding='utf8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=4)

    studio_data = {}
    for page in raw_data:
        studio_data[page.get('properties', {}).get('Studio Name', {}).get('title')[0].get('plain_text', '')] = {
            'active': page.get('properties', {}).get('Active', {}).get('checkbox', False),
            'studio_website': page.get('properties', {}).get('Studio Website', {}).get('url', ''),
            'linkedin_url': page.get('properties', {}).get('LinkedIn URL', {}).get('url', ''),
            'careers_page': page.get('properties', {}).get('Careers Page', {}).get('url', ''),
        }
    sorted_studio_data = dict(sorted(studio_data.items()))

    # dump studio data to json file
    with open('studio_db.json', 'w', encoding='utf8') as f:
        json.dump(sorted_studio_data, f, ensure_ascii=False, indent=4)

    return sorted_studio_data

def scrape_job_postings(pages_dict={}):
    """_summary_

    Returns:
        _type_: _description_
    """
    for studio, studio_data in pages_dict.items():
        if not studio_data.get('active', False):
            logger.warning(f"Studio not active:{studio}")
            continue

        if not studio_data.get('careers_page', ''):
            logger.warning(f"Careers page unavailable")

        process_website(studio, studio_data.get('careers_page', ''))
    return None

def remove_unicode(s):
    return ''.join(c for c in s if ord(c) < 128)

def process_website(studio, url):
    logger.debug(f"{studio} - {url}")
    raw_html = scrape_website(url)
    clean_html = remove_unicode(raw_html)
    with open(f"{studio}.html", "w") as file:
        file.write(clean_html)
    logger.info(f"HTML file created: {studio}.html")

def main():
    """_summary_
    """
    setup_logging()
    studios_data = get_pages()
    scrape_job_postings(studios_data)

if __name__ == "__main__":
    main()