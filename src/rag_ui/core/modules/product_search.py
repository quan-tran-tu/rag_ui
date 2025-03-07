import requests
import json

WEBSOSANH_URL = "https://websosanh.vn/search-api/get-search-product"

def websosanh_search(keyword: str) -> str:
    """
    Fetch products from websosanh.vn based on 'keyword'.
    Args:
        keyword (str): The keyword to search for.
    Returns:
        str: JSON dumps of list of products (only the first 'limit' products).
    """
    limit = 3
    data = {
        "startOffset":0,
        "numRow":0,
        "defaultRow":40,
        "categoryIds":[],
        "merchantIds":[],
        "regionIds":[],
        "isGetResult":True,
        "numPromotedCustomerProduct":0,
        "propertyFilters":[],
        "propertyRangeFilters":[],
        "keyword":keyword,
        "productType":"0",
        "isAppend":True,
        "pageIndex":1,
        "isDesktop":True
    }
    response = requests.post(WEBSOSANH_URL, json=data)
    response.raise_for_status()
    response = response.json()
    products = []
    products_json = response["searchProductModels"][:limit]
    for product in products_json:
        products.append({
            'productId': product['productId'],
            'image': product['image'],
            'productName': product['productName'],
            'price': product['price'],
            'detailUrl': 'https://websosanh.vn' + product['detailUrl'],
            'merchantDomain': product['merchantDomain'],
            'provins': product['provins'],
        })

    return json.dumps(products)