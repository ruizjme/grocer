#!/usr/bin/env python

"""
Maps (some of) the Woolworths REST API endpoints.
"""

import json
import requests

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
                'Search/suggestion?Key=peters', # GET
                'Search/products' # POST with payload
                ]

def _get_request(endpoint, params={}, payload={}, headers={}):
    api_base = 'https://www.woolworths.com.au/apis/ui/'
    qsp = '?'+'&'.join(["{}={}".format(k,v.replace(' ','+'))
                            for k,v in params.items()]) if params else ''
    r = requests.get(api_base+endpoint+qsp, data=payload, headers=headers)

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

def list_categories():
    """List category names
    """
    categories = get_categories()
    return list(set([cat['UrlFriendlyName'] for cat in categories]))

def get_category_id(category):
    """Return the category id for a given category name
    """
    categories = get_categories()

    assert category in [cat['UrlFriendlyName'] for cat in categories]

    for cat in categories:
        if cat['UrlFriendlyName'] == category:
            return cat['NodeId']
    return None

def get_products(category, max_pages=200, sort_type="CUPAsc",
                    filters=[]):
    """Get product data from category
    """

    sort_types = [  "TraderRelevance",
                    "AvailableDate",
                    "PriceAsc",
                    "PriceDesc",
                    "Name",
                    "NameDesc",
                    "CUPAsc",
                    "CUPDesc",
                    "BrowseRelevance",  ]
    assert sort_type in sort_types
    assert max_pages > 1

    cat_id = get_category_id(category)

    bundles = []
    bundle_names = []

    # TODO: use max_pages = r['TotalRecordCount'] / 36 if not max_pages
    for i in range(1, max_pages):
        payload = { "categoryId": cat_id,
                    "url":"/shop/browse/pantry",
                    "formatObject":'{\"name\":\"%s\"}' % category,
                    "pageNumber":i,
                    "pageSize":36,
                    # "location":"/shop/browse/pantry",
                    # "isSpecial":'false',
                    # "isBundle":'false',
                    # "isMobile":'false',
                    "sortType":sort_type,
                    "filters":filters
                    }

        r = _post_request('browse/category', payload=payload)
        if r == []:
            break

        bundles += [b for b in r['Bundles'] if b['Name'] not in bundle_names]
        bundle_names += [b['Name'] for b in r['Bundles']]

    return bundles

def get_search_suggestion(query):
    """Search/suggestion?Key=peters"""
    r = _get_request('Search/suggestion', params={'Key':query})
    return r

def get_search(query):
    """Get a list of bundles as a result of a search query"""
    payload = { "SearchTerm": query,
                "PageNumber":1,
                "PageSize":24,
                # "IsSpecial":false,
                # "Location":"/shop/search/products?searchTerm=peter%20drumstick",
                "Passes":[6,11,12,15,26],
                "SortType":"TraderRelevance",
                "Filters":[],
                }
    r = _post_request('Search/products', payload=payload)
    return r

if __name__ == '__main__':
    import pprint
    pprint.pprint(get_products('pantry',2))
