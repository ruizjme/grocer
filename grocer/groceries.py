import time
import pprint
import pandas as pd

import grocery          # For scraping catalogs
import mongo_interface  # For interfacing with MongoDB

categories = [	'specials',
                'fruit-veg',
                'meat-seafood-deli',
                'bakery',
                'dairy-eggs-fridge',
                'pantry',
                'freezer',
                'drinks',
                'liquor',
                'health-beauty',
                'household',
                'lunch-box'     ]

CATEGORY = categories[5]
DATABASE = 'test_db'

time0 = time.time()

# Store the data in a mongoDB
products = grocery.get_products_Woolworths(CATEGORY, 4)
df1 = grocery.load_dataframe(products)
mongo_interface.write_mongo(DATABASE, CATEGORY, df1)

# And retrieve the table to see if it worked
# df2 = mongo_interface.read_mongo(DATABASE, CATEGORY)
# print(df2)

# To see what tables exist in the database
# from pymongo import MongoClient
# client = MongoClient()
# db = client[DATABASE]
# print(db.collection_names(include_system_collections=False))

# example query
# for item in db[CATEGORY].find({'unit':'1KG'}):
    # pprint.pprint(item)

print('Total time: {} s'.format(time.time() - time0))
