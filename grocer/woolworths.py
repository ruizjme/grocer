#!/usr/bin/env python

import json
import requests
import random
import pprint
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

api_base = 'https://www.woolworths.com.au/apis/ui/'

def _get_request(endpoint, payload={}, headers={}):
    api_base = 'https://www.woolworths.com.au/apis/ui/'
    r = requests.get(api_base+endpoint, data=payload, headers=headers)
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

    for cat in categories:
        if cat['UrlFriendlyName'] == category:
            return cat['NodeId']
    return None

def list_categories():
    """List category names
    """
    categories = get_categories()
    return list(set([cat['UrlFriendlyName'] for cat in categories]))

def get_products(category):
    """Get product data from category
    """
    if category not in list_categories():
        raise ValueError("Bad category '{}'.".format(category))
    cat_id = get_category_id(category)

    bundles = []
    bundle_names = []
    for i in range(1, 200):
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

        r = requests.post(api_base+'browse/category', data=payload, )

        try:
            r = json.loads(r.text)
        except:
            print(r, r.text)
            raise ValueError("{} - {}. Could not retrieve JSON.")
        if r == []:
            break
        bundles += [b for b in r['Bundles'] if b['Name'] not in bundle_names]
        bundle_names += [b['Name'] for b in r['Bundles']]
        print(i)
    return bundles

if __name__ == '__main__':
    pprint.pprint(len(get_products('whisky')))
    l = list_categories()
    pprint.pprint(l)
    print(len(l))
