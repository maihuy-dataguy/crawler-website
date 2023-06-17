import numpy as np
from pandas import DataFrame
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd

# Category_id (shall init on configuration)
category_ids = ['c413893']
# Declare the number of pages to crawl (shall init on configuration)
num_pages = 1

# Declare browser
driver = webdriver.Chrome('chromedriver')


def extract_sectional_product_info(link):
    # Open URL
    driver.get(link)
    sleep(random.randint(5, 10))
    # ================================Get title
    title_elements = driver.find_elements(By.CSS_SELECTOR, ".BrowseCore [data-enzyme-id = 'productNameSpacing']")
    titles = [elem.text for elem in title_elements]
    # ================================Get brand
    brand_elements = driver.find_elements(By.CSS_SELECTOR, ".BrowseCore ._1vgix4w0_6101")
    brands = [elem.text for elem in brand_elements]
    # ================================Get new_price, list_price
    price_elements = driver.find_elements(By.CSS_SELECTOR, ".SFPrice")
    prices = [elem.text.replace('From', '') for elem in price_elements]
    new_prices = ['$' + price.split('$')[1] for price in prices]
    list_prices = ['$' + price.split('$')[2] if len(price.split('$')) == 3 else '' for price in prices]
    # ==================================Get shipping fee
    shipping_fee_elements = driver.find_elements(By.CSS_SELECTOR, ".BrowseCore [data-enzyme-id='shippingSpacing']")
    shipping_fees = [elem.text.split("\n")[1]
                     if len(elem.text.split("\n")) == 3
                     else elem.text
                     for elem in shipping_fee_elements]
    # ==================================Get rating, rating_count
    ratings, rating_counts, rating_idx = [], [], []
    for i in range(1, len(titles) + 1):
        try:
            try:
                rating = driver.find_element("xpath", "/html/body/div[3]/div/div/div/div[1]/div[2]/div[3]/main/div/div["
                                                      "1]/div/div/div/div[{}]/div/div/div/a/div[5]/div/p".format(i))
            except NoSuchElementException:
                rating = driver.find_element("xpath", "/html/body/div[3]/div/div/div/div[1]/div[2]/div[2]/main/div/div["
                                                      "1]/div/div/div/div[{}]/div/div/div/a/div[5]/div/p".format(i))
            ratings.append(rating.text.split('stars')[0])
            try:
                rating_count = driver.find_element("xpath", "/html/body/div[3]/div/div/div/div[1]/div[2]/div["
                                                            "3]/main/div/div[1]/div/div/div/div[{}]/div/div/div/a/div["
                                                            "5]/div/div[2]".format(i))
            except NoSuchElementException:
                rating_count = driver.find_element("xpath", "/html/body/div[3]/div/div/div/div[1]/div[2]/div["
                                                            "2]/main/div/div[1]/div/div/div/div[{}]/div/div/div/a/div["
                                                            "5]/div/div[2]".format(i))
            rating_counts.append(rating_count.text[1:-1])
            rating_idx.append(i)
        except NoSuchElementException:
            print('No reviewers for ' + titles[i - 1])
    print(ratings)
    # ==================================Get sponsor
    is_sponsors, sponsor_idx = [], []
    for i in range(1, len(titles) + 1):
        try:
            try:
                is_sponsor = driver.find_element("xpath", "/html/body/div[3]/div/div/div/div[1]/div[2]/div[3]/main"
                                                          "/div/div[1]/div/div/div/div[{}]/div/div/div/a/div[{}]/div[1]/div"
                                                 .format(i, 7 if i in rating_idx else 6))
            except NoSuchElementException:
                is_sponsor = driver.find_element("xpath", "/html/body/div[3]/div/div/div/div[1]/div[2]/div[2]/main"
                                                          "/div/div[1]/div/div/div/div[{}]/div/div/div/a/div[{}]/div/div"
                                                 .format(i, 7 if i in rating_idx else 6))
            is_sponsors.append(is_sponsor.text)
            sponsor_idx.append(i)
        except NoSuchElementException:
            print('No sponsor for ' + titles[i - 1])
    print(sponsor_idx)
    # =====================================DataFrame
    df1 = pd.DataFrame(list(zip(titles, brands, new_prices, list_prices, shipping_fees)),
                       columns=['title', 'brand', 'new_price', 'list_price', 'shipping_fee'])
    df1.insert(0, "category_id", link.split('-')[-1][:-15])
    df1['index_'] = np.arange(1, len(df1) + 1)

    df2 = pd.DataFrame(list(zip(rating_idx, ratings, rating_counts)),
                       columns=['rating_idx', 'rating', 'rating_count'])
    df3 = df1.merge(df2, how="left", left_on='index_', right_on='rating_idx')
    df4 = pd.DataFrame(list(zip(sponsor_idx, is_sponsors)), columns=['sponsor_idx', 'is_sponsored'])
    df5 = df3.merge(df4, how="left", left_on='index_', right_on='sponsor_idx')
    df5 = df5[['category_id', 'title', 'brand',
               'new_price', 'list_price', 'rating', 'rating_count', 'shipping_fee', 'is_sponsored']]
    df5['is_sponsored'] = np.where(df5['is_sponsored'] == 'Sponsored', 'True', 'False')
    return df5


dfs = []

for category_id in category_ids:
    for page in range(1, num_pages + 1):
        print('Crawl Page ' + str(page))
        df = extract_sectional_product_info(
            'https://www.wayfair.com/furniture/sb0/sectionals-{}.html?curpage={}'.format(category_id, page)
        )
        dfs.append(df)

result = pd.concat(dfs).head(300)
result.to_csv('output/exercise_3.csv', index=False)
