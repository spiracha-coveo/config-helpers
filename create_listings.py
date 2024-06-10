import pandas as pd
import json
import requests
from dotenv import load_dotenv
import os

# Configuration constants
CSV_FILES = ['FILE.csv']
LISTING_STUB = 'listings-stub.json'
STAGING_TRACKING_ID = 'stg_conforama'
PROD_TRACKING_ID = 'prod_conforama'
CATEGORY_FIELD = 'ec_category'
STAGING_ORG_ID = 'conforamasuissesanonproduction1geoabvmw'
PROD_ORG_ID = 'conforamasuissesaproductiona7ej0kj7'

STAGING = False  # Toggle between staging and production

# Set organization and tracking IDs based on the environment
ORG_ID = STAGING_ORG_ID if STAGING else PROD_ORG_ID
TRACKING_ID = STAGING_TRACKING_ID if STAGING else PROD_TRACKING_ID

ENDPOINT = f'https://platform-eu.cloud.coveo.com/rest/organizations/{ORG_ID}/commerce/v2/configurations/listings/'

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")
HEADERS = {
    'accept': '*/*',
    'Authorization': f'Bearer {TOKEN}',
}

def read_csv_to_dataframe(csv_path):
    """Reads a CSV file into a pandas DataFrame."""
    try:
        df = pd.read_csv(csv_path, header=0)
        return df
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def read_json_to_dict(json_path):
    """Reads a JSON file into a Python dictionary."""
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{json_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_config_name(category_information, category_code):
    """Gets the configuration name based on category information."""
    if len(category_information) == 1:
        category_name = category_information['name'].iloc[0]
    else:
        filtered_df = category_information[category_information['url'].str.contains('/fr/')]
        category_name = filtered_df['name'].iloc[0] if not filtered_df.empty else None

    return category_name if not pd.isna(category_name) else category_code

def get_listing_json(category_code, url_lang_mapping, category_name):
    """Generates the listing JSON configuration."""
    listing_json = read_json_to_dict(LISTING_STUB)
    listing_json['patterns'] = url_lang_mapping
    listing_json['name'] = category_name
    listing_json['trackingId'] = TRACKING_ID
    listing_json['rules']['filterRules'] = [
        {
            "name": f'{CATEGORY_FIELD} contains {category_code}',
            "action": "include",
            "essential": True,
            "filters": [
                {
                    "fieldName": CATEGORY_FIELD,
                    "operator": "contains",
                    "value": {
                        "type": "array",
                        "values": [category_code]
                    }
                }
            ]
        }
    ]
    return listing_json

def get_url_patterns(category_information):
    """Generates URL patterns for the category."""
    urls = category_information['url'].tolist()
    base_url = "https://stg.conforama.ch" if STAGING else "https://www.conforama.ch"
    
    if len(urls) == 1 and urls[0].startswith('/c/'):
        urls_list = [{"url": f"{base_url}/{lang}{urls[0]}"} for lang in ['fr', 'de', 'it']]
    else:
        urls_list = [{"url": url.replace("https://www.conforama.ch", base_url)} for url in urls]
    
    return urls_list

def create_via_api(category_code, listing_json):
    """Creates a listing configuration via the API."""
    response = requests.post(ENDPOINT, headers=HEADERS, json=listing_json)
    
    if response.status_code != 201:
        print(f"----> Failed to update category configuration for category {category_code}. Status code: {response.status_code}")
    else:
        response_json = response.json()
        name = response_json.get('name')
        id = response_json.get('id')
        print(f"----> Category created successfully with name: {name}, id: {id}")
        return True

def create_config_for_category_code(category_code, category_information):
    """Creates a configuration for a given category code."""
    print(f"Creating config for category code: {category_code}")
    url_patterns = get_url_patterns(category_information)
    category_name = get_config_name(category_information, category_code)
    listing_json = get_listing_json(category_code, url_patterns, category_name)
    create_via_api(category_code, listing_json)

def main():
    for file in CSV_FILES:
        df = read_csv_to_dataframe(file)
        if df is not None:
            df_grouped = df.groupby('fieldvalue')
            for category_code, category_information in df_grouped:
                create_config_for_category_code(category_code, category_information)

if __name__ == '__main__':
    main()
