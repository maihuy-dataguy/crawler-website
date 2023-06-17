from pandas import DataFrame
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd

# Asin (shall init on configuration)
asins = ['B07MFZXR1B', 'B07CRG7BBH', 'B07VS8QCXC']

# Declare browser
driver = webdriver.Chrome('chromedriver')


def extract_product_detail(link):
    # Open URL
    driver.get(link)
    sleep(random.randint(5, 10))
    # ================================Get title
    title_elements = driver.find_elements(By.CSS_SELECTOR, ".centerColAlign .product-title-word-break")
    titles = [elem.text for elem in title_elements]
    # ==================================Get price/list price
    new_price_elements = driver.find_elements(By.CSS_SELECTOR, ".centerColAlign .a-price-whole")
    new_prices = [elem.text for elem in new_price_elements]

    list_price_elements = driver.find_elements(By.CSS_SELECTOR, ".centerColAlign .basisPrice [aria-hidden]")
    list_prices = [elem.text for elem in list_price_elements]
    if not list_prices:
        list_prices.append('')
    # =======================================Get rating
    rating_elements = driver.find_elements(By.CSS_SELECTOR, ".centerColAlign .reviewCountTextLinkedHistogram")
    ratings = [elem.get_attribute('title') for elem in rating_elements]
    # =======================================Get rating count
    rating_count_elements = driver.find_elements(By.CSS_SELECTOR, "#acrCustomerReviewLink")
    rating_counts = set([elem.text for elem in rating_count_elements])
    # =======================================Get image url
    image_url_elements = driver.find_elements(By.CSS_SELECTOR, ".leftCol .imgTagWrapper [src]")
    image_urls = [elem.get_attribute('src') for elem in image_url_elements]
    # =====================================DataFrame
    df = pd.DataFrame(list(zip(titles, new_prices, list_prices, ratings, rating_counts, image_urls)),
                      columns=['title', 'new_price', 'list_price', 'rating', 'rating_count', 'image_url'])
    df.insert(0, "asin", link.split('/')[-1])
    df['list_price'] = df['list_price'].str[1:]
    return df


dfs = []

for asin in asins:
    df = extract_product_detail('https://www.amazon.com/dp/{}'.format(asin))
    dfs.append(df)

result = pd.concat(dfs)
result.to_csv('output/exercise_2.csv', index=False)
