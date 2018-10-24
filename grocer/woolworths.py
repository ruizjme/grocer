#!/usr/bin/env python

import json
import requests
import re

"""
Interesting Bundle keys (r['Bundles'][0]['Products'][0]):
-----------------------
Barcode
Brand
CupMeasure
CupPrice
DetailsImagePaths
Description
DisplayQuantity
Name
PackageSize
Price
RichDescription
UrlFriendlyName
Stockcode --> for https://www.woolworths.com.au/apis/ui/product/detail/193885
"""

endpoints = [   'products/', # append comma-separated Stockcodes
                'browse/category',
                'PiesCategoriesWithSpecials', # to get categoryId list
                'product/detail/', # append Stockcode
                ]

def _get_request(endpoint, payload={}, headers={}):
    api_base = 'https://www.woolworths.com.au/apis/ui/'
    r = requests.get(api_base+endpoint, data=payload, headers=headers)
    try:
        data = json.loads(r.text)
    except TypeError:
        raise TypeError("{} - {}".format(r, r.text))
    return data

def _post_request(endpoint, payload={}, headers={}):
    api_base = 'https://www.woolworths.com.au/apis/ui/'
    r = requests.post(api_base+endpoint, data=payload, headers=headers)
    try:
        data = json.loads(r.text)
    except TypeError:
        raise TypeError("{} - {}".format(r, r.text))
    return data

def get_categories():
    data = _get_request('PiesCategoriesWithSpecials')
    categories = data['Categories']
    for cat in categories:
        if cat['Children']:
            categories += cat['Children']
        cat.pop('Children', None)
    return categories

def get_category_id(category):
    """Return the category id for a given category name
    """
    categories = get_categories()

    if category not in [cat['UrlFriendlyName'] for cat in categories]:
        raise ValueError("Bad category '{}'.".format(category))

    for cat in categories:
        if cat['UrlFriendlyName'] == category:
            return cat['NodeId']
    return None

def list_categories():
    """List category names
    """
    categories = get_categories()
    return list(set([cat['UrlFriendlyName'] for cat in categories]))

def get_products(category, max_pages=200):
    """Get product data from category
    """
    cat_id = get_category_id(category)

    bundles = []
    bundle_names = []
    for i in range(1, max_pages):
        payload = { "categoryId": cat_id,
                    "url":"/shop/browse/pantry",
                    "formatObject":'{\"name\":\"%s\"}' % category,
                    "pageNumber":i,
                    "pageSize":36,
                    # "location":"/shop/browse/pantry",
                    # "sortType":"TraderRelevance",
                    # "isSpecial":'false',
                    # "isBundle":'false',
                    # "isMobile":'false',
                    # "filters":[]
                    }
        
        r = _post_request('browse/category', payload=payload)
        
        if r == []:
            break
        
        bundles += [b for b in r['Bundles'] if b['Name'] not in bundle_names]
        bundle_names += [b['Name'] for b in r['Bundles']]
    
    return bundles

if __name__ == '__main__':
    import pprint
    pprint.pprint(len(get_products('whisky',5)))
