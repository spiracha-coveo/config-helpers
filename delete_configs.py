import os
import requests
from dotenv import load_dotenv
from constants import ORG_ID, ENDPOINT

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")
HEADERS = {
    'accept': '*/*',
    'Authorization': f'Bearer {TOKEN}',
}

def fetch_listings(url, token):
    page = 0
    total_pages = float('inf')
    all_listing_ids = []
    all_listing_names = []

    while page < total_pages:
        params = {
            'page': page,
            'perPage': 10
        }

        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f'Failed to fetch listings. Status code: {response.status_code}')
            exit(1)
        else:
            data = response.json()

            listing_ids, listing_names = fetch_listings_ids(data['items'])
            
            all_listing_ids.extend(listing_ids)
            all_listing_names.extend(listing_names)

            total_pages = data['totalPages']
            page += 1

    return all_listing_ids, all_listing_names

def fetch_single_listing(id):
    url = f'{ENDPOINT}{id}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f'Failed to fetch listing with id: {id}')
        return None
    else:
        return response.json()

def fetch_listings_ids(listings):
    listing_ids = []
    listing_names = []
    for listing in listings:
        listing_ids.append(listing['id'])
        listing_names.append(listing['name'])
    return listing_ids, listing_names

def delete_listings(listing_ids):
    for listing_id in listing_ids:
        delete_single_listing(listing_id)

def delete_single_listing(listing_id):
    url = f'{ENDPOINT}{listing_id}'
    response = requests.delete(url, headers=HEADERS)
    if response.status_code != 204:
        print(f'Failed to delete listing with id: {listing_id}')
    else:
        print(f'Deleted listing with id: {listing_id}')

def main():
    delete_listings()



if __name__ == '__main__':
    main()
