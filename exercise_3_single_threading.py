
import numpy as np
from pandas import DataFrame
from selenium import webdriver
import time
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
from undetected_chromedriver import Chrome

# Category_id (shall init on configuration)
category_ids = ['c413893']
# Declare the number of pages to crawl (shall init on configuration)
num_pages = 7
# Declare products variable to store data
products = []

# Declare browser
driver = Chrome()


def extract_product(item):
    # ================================Get title
    title = item.find_element(By.CSS_SELECTOR, 'h2[data-name-id="ListingCardName"]')
    # ================================Get brand

    brand = item.find_element(By.CSS_SELECTOR, 'p[data-name-id="ListingCardManufacturer"]')
    # ================================Get new_price, list_price
    new_prices = item.find_elements(By.CSS_SELECTOR,
                                    'span[data-test-id="StandardPricingPrice-PRIMARY"]')
    if len(new_prices) == 0:
        new_prices = item.find_elements(By.CSS_SELECTOR,
                                        'span[data-test-id="StandardPricingPrice-SALE"]')
    list_prices = item.find_elements(By.CSS_SELECTOR,
                                     'span[data-test-id="StandardPricingPrice-PREVIOUS"] [data-name-id="PriceDisplay"]')
    # ==================================Get shipping fee
    shipping_fees = item.find_elements(By.CSS_SELECTOR, 'span[data-enzyme-id="DeliveryPromise"]')
    # ==================================Get rating, rating count
    ratings = item.find_elements(By.CSS_SELECTOR, 'p[data-name-id="ListingCardReviewStars-a11yLabel"]')
    rating = ""
    rating_count = ""
    if len(ratings) > 0:
        processed_ratings = ratings[0].text[6:].split('.')
        rating = processed_ratings[0] + "." + processed_ratings[1] \
            if len(processed_ratings) == 3 else processed_ratings[0]
        rating_count = processed_ratings[2].split(' ')[0] \
            if len(processed_ratings) == 3 else processed_ratings[1].split(' ')[0]

    # ==================================Get sponsor
    sponsored = item.find_elements(By.CSS_SELECTOR, 'div[data-testid="sponsored-tag"]')

    product = {
        'title': title.text,
        'brand': brand.text,
        'new_price': new_prices[0].text if len(new_prices) > 0 else "",
        'list_price': list_prices[0].text if len(list_prices) > 0 else "",
        'rating': rating,
        'rating_count': int(rating_count) if rating_count != '' else 0,
        'shipping_fee': "Free Shipping" if len(shipping_fees) > 0 else "",
        'sponsored': True if len(sponsored) > 0 else False
    }

    products.append(product)


def get_items_from_url(url):
    driver.get(url)
    time.sleep(random.randint(5, 10))
    item_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="Browse-Grid"] div[data-hb-id="Card"]')
    return item_elements


def extract_sectional_product_info(link, category_id):
    # Open URL
    item_elements = get_items_from_url(link)
    while True:
        if len(item_elements) == 48:
            break
        item_elements = get_items_from_url(link)

    for item in item_elements:
        extract_product(item)

    df1 = pd.DataFrame(products)
    products.clear()
    df1.insert(0, "category_id", category_id)
    df1.insert(0, "page", link[-1])
    return df1


def main():
    dfs = []
    for category_id in category_ids:
        for page in range(1, num_pages + 1):
            print('Crawl Page ' + str(page))
            df = extract_sectional_product_info(
                'https://www.wayfair.com/furniture/sb0/sectionals-{}.html?curpage={}'.format(category_id, page),
                category_id
            )
            dfs.append(df)

    print("-------Crawl Success!!-------")
    result = pd.concat(dfs).head(300)
    result.to_csv('output/exercise_3.csv', index=False)


if __name__ == '__main__':
    main()
