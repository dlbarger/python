'''

params = {
  "engine": "google_product",
  "product_id": "4172129135583325756",
  "gl": "us",
  "hl": "en",
  "api_key": "secret_api_key"
}

search = GoogleSearch(params)
results = search.get_dict()
product_results = results['product_results']
'''

from serpapi import GoogleSearch
import json

#API_KEY = "6e01ee98f78c5fdf7754c251b356d0172d535c1c82c2e95596cba2c95eda6c5f"
API_KEY = "8bbffa3a4a9e6f43effa961eba6c9355b9b16d30fa740ce3fe56762a360d519b"

def search_products(search_term, store_location, api_key):
    params = {
        "q": search_term,
        "tbm": "shop",
        "location": store_location,
        "hl": "en",
        "gl": "us",
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    return (results['shopping_results'])

def get_product(product_id, api_key):
    params = {
        "engine": "google_product",
        "product_id": product_id,
        "gl": "us",
        "hl": "en",
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return(results['product_results'])
    

if __name__ == "__main__":
    data = search_products("samsung flat screen tv", "Atlanta", API_KEY)
    
    print(json.dumps(data[1], indent=2))


    # cnt = len(data)
    # i = 0

    # while i < cnt:
    #     #print(json.dumps(data[i]["title"], indent=2))
    #     #print(json.dumps(data[i], indent=2))
    #     #print(json.dumps(get_product(data[i]["product_id"], API_KEY), indent=2))
    #     print(json.dumps(data[i]['serpapi_product_api'],indent=2))
    #     i += 1

    # print(i)

    
