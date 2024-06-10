# Instructions for Managing Coveo Listings

The scripts assume you have a `.env` file with a `TOKEN=XXXX` variable that can authenticate the requests. You can generate a long-lived token via the Platform or use a temporary one from Swagger.

## Scripts Overview

1. **`constants.py`** - Used to define constants such as `ORG_ID`.
2. **`create_listings.py`** - Used to create listings from provided CSV. Adjust the path in the `constants.py` file. For Conforama, we had multiple URLs per listing due to French, German, and Italian languages, so the script may look a bit different for that.
3. **`delete_configs.py`** - Used to delete all the configs.

## Sample Configurations

Sample configs for a single-language implementation can be found on Barca. For example:

```
curl -X 'GET'
'https://platform.cloud.coveo.com/rest/organizations/barcagroupproductionkwvdy6lp/commerce/v2/configurations/listings?page=0&perPage=10'
-H 'accept: /'
```



Specific config for the towels page: [https://sports.barca.group/browse/promotions/accessories/towels#sortCriteria=relevance](https://sports.barca.group/browse/promotions/accessories/towels#sortCriteria=relevance)


```
curl -X 'GET'
'https://platform.cloud.coveo.com/rest/organizations/barcagroupproductionkwvdy6lp/commerce/v2/configurations/listings/00f1ef42-a6ac-49e7-85ce-35e8cdbe6ed5'
-H 'accept: /'
-H 'Authorization: Bearer <TOKEN>'
```


### Sample Configuration JSON

```json
{
  "id": "00f1ef42-a6ac-49e7-85ce-35e8cdbe6ed5",
  "name": "Towels",
  "matching": {
    "id": "3818d8e8-f1d4-4fcc-a7d2-cd5cda231fad",
    "url": "https://sports.barca.group/browse/promotions/accessories/towels",
    "global": false
  },
  "patterns": [
    {
      "id": "3818d8e8-f1d4-4fcc-a7d2-cd5cda231fad",
      "url": "https://sports.barca.group/browse/promotions/accessories/towels",
      "global": false
    }
  ],
  "queryConfiguration": {
    "id": "7a387eb6-af73-40e0-a9ed-b6ff4a733282",
    "additionalFields": [],
    "facets": {
      "enableIndexFacetOrdering": false,
      "freezeFacetOrder": false,
      "facets": [......],
    "perPage": 24,
    "sorts": [
      {
        "sortCriteria": "relevance"
      },
      {
        "sortCriteria": "fields",
        "fields": [
          {
            "field": "ec_promo_price",
            "direction": "asc",
            "displayName": "Price (Low to High)",
            "displayNames": [
              {
                "value": "Prix (bas à élevé)",
                "language": "fr"
              },
              {
                "value": "Price (Low to High)",
                "language": "en"
              }
            ]
          }
        ]
      },
      {
        "sortCriteria": "fields",
        "fields": [
          {
            "field": "ec_promo_price",
            "direction": "desc",
            "displayName": "Price (High to Low)",
            "displayNames": [
              {
                "value": "Price (High to Low)",
                "language": "en"
              },
              {
                "value": "Prix (De haut en bas)",
                "language": "fr"
              }
            ]
          }
        ]
      }
    ]
  },
  "rules": {
    "id": "c2d418bf-d4ec-4345-baec-03273b0ef859",
    "rankingRules": [],
    "filterRules": [
      {
        "id": "9abf0264-3b43-43ca-85ec-a75cf826b8e8",
        "name": "Include product cat_slug contains accessories/towels",
        "updatedAt": "2024-01-11T15:24:20.236Z",
        "essential": true,
        "locales": [],
        "filters": [
          {
            "fieldName": "cat_slug",
            "operator": "contains",
            "value": {
              "type": "array",
              "values": [
                "accessories/towels"
              ]
            }
          }
        ],
        "action": "include"
      }
    ],
    "pinRules": []
  },
  "additionalFields": [],
  "scope": "specific"
}


