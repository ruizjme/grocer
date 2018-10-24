import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class Grocery(object):

    def __init__(self, name, supermarket, price, pricePerUnit, unit,
                    brand=None, weight=None):
        self.name = name
        self.brand = brand
        self.supermarket = supermarket
        self.weight = weight
        self.price = price
        self.pricePerUnit = pricePerUnit
        self.unit = unit

def load_all_items(driver):
    '''
    Scroll down all the way in order to load all the items in the category.
    '''

    time.sleep(1)

    SCROLL_PAUSE_TIME = 0.6

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def _collect_data_Woolworths(driver):
    """
    Store the relevant fields in lists for each category.
    """

    # Collect product name
    products_name = [elem.text for elem in driver.find_elements_by_css_selector('.tileList .shelfProductTile-content .shelfProductTile-descriptionLink')]
    # Collect product price dollars
    products_price_dollars = [elem.text for elem in driver.find_elements_by_css_selector('.tileList .shelfProductTile-content .price-dollars')]
    # Collect product price cents
    products_price_cents = [elem.text for elem in driver.find_elements_by_css_selector('.tileList .shelfProductTile-content .price-cents')]

    products_price_per_unit = []

    for elem in driver.find_elements_by_css_selector('.tileList .shelfProductTile-content'):
        try:
            ppu = elem.find_element_by_css_selector('.shelfProductTile-cupPrice').text
        except NoSuchElementException:
            ppu = '$0.00 / 1KG'
        products_price_per_unit.append(ppu)
        print(ppu)

    # Collect pricePerUnit
    #products_price_per_unit = [elem.text for elem in driver.find_elements_by_css_selector('.tileList .shelfProductTile-content .shelfProductTile-cupPrice')]
    # Check that attirbute count matches
    # assert len(products_name) == len(products_brand) == len(products_supermarket) == len(products_weight) == len(products_price) == len(products_price_per_unit)

    products_ppu = []
    products_unit = []

    for product_ppu in products_price_per_unit:
        try:
            match = re.search(r'\$([0-9]{1,3}\.[0-9]{1,2}) \/ (\w+)', product_ppu)
            products_ppu.append(float(match.group(1)))
            products_unit.append(match.group(2))
        except AttributeError:
            products_ppu.append(0.0)
            products_unit.append('n/a')


    products_price = []

    for i in range(len(products_price_dollars)):
        products_price.append(float(products_price_dollars[i]+'.'+products_price_cents[i]))

    ####################################

    # Generate list of objects
    products = []
    for i in range(len(products_name)):
        try:
            products.append(Grocery(products_name[i], 'Woolworths', products_price[i], products_ppu[i], products_unit[i]))
        except:
            products.append(Grocery('Error', 'Woolworths', '', 0.0, ''))

    # To sort the list in place...
    #print('Sorting...')
    #products.sort(key=lambda x: x.pricePerUnit, reverse=False)
    #products.sort(key=lambda x: x.unit, reverse=False)

    return products

def get_products_Woolworths(category, maxPage=None):
    driver = webdriver.Chrome()

    products = []
    pageNumber = 1

    while True:
        try:
            print("Loading page {}".format(pageNumber))
            driver.implicitly_wait(10)
            driver.get('https://www.woolworths.com.au/shop/browse/'+category+'?pageNumber='+str(pageNumber))
            driver.find_element_by_css_selector('._pagingNext')

            # dirty hack to speed up testing
            if maxPage and (pageNumber == maxPage):
                raise NoSuchElementException

            print('Collecting data...')
            products_temp = _collect_data_Woolworths(driver)
            for prod in products_temp:
                products.append(prod)

            print('Page {} done!'.format(pageNumber))
            pageNumber += 1

        except NoSuchElementException:
            print('Collecting data...')
            products_temp = _collect_data_Woolworths(driver)
            for prod in products_temp:
                products.append(prod)

            print('Page {} done!'.format(pageNumber))
            driver.close()
            return products


def load_dataframe(products):
    df = pd.DataFrame(columns=['pricePerUnit','unit','name','supermarket'])

    for i, grocery in enumerate(products):
        df.loc[i] = [grocery.pricePerUnit, grocery.unit, grocery.name, grocery.supermarket]

    return df
