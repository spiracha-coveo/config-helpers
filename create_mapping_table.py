import json
import os
import requests
from dotenv import load_dotenv
from constants import BASE_URL, GLOBAL_CONFIG_URL, MAPPING_JSON_PATH, ENDPOINT

config_json = {}

def fetch_listings(url, token):
    """
    Fetch configuration listings from the specified URL using the provided token.
    """
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {token}',
    }

    page = 0
    total_pages = float('inf')

    while page < total_pages:
        params = {
            'page': page,
            'perPage': 10
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.text}")

        data = response.json()
        process_config_page(data)

        total_pages = data['totalPages']
        page += 1

def process_config_page(data):
    """
    Process configuration data retrieved from the API response.
    """
    for item in data['items']:
        matching_url = item['matching']['url']
        if matching_url == GLOBAL_CONFIG_URL:
            continue
        config_id = item['id']
        language, category = parse_url(matching_url)
        update_config(language, category, config_id)

def parse_url(url):
    """
    Parse the language and category from the given URL.
    """
    url_array = [part for part in url.split(BASE_URL) if part]
    if len(url_array) != 1:
        raise ValueError(f"Invalid URL: {url}")

    url_array = [part for part in url_array[0].split('/') if part]
    language = url_array[0]
    category = url_array[-1]
    return language, category

def update_config(language, category, config_id):
    """
    Update the configuration JSON with the provided language, category, and ID.
    """
    if category not in config_json:
        config_json[category] = {}
    config_json[category][language] = config_id

def write_config_to_json():
    """
    Write the configuration JSON to a file.
    """
    with open(JSON_OUTPUT_PATH, "w") as json_file:
        json.dump(config_json, json_file, indent=4)

def main():
    """
    Main function to fetch configuration listings and write them to a JSON file.
    """
    load_dotenv()
    token = os.getenv("TOKEN")

    fetch_listings(ENDPOINT, token)
    write_config_to_json()

if __name__ == "__main__":
    main()
