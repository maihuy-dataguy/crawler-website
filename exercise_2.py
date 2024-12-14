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
driver = webdriver.Chrome()


def extract_product_detail(asin):
    # Open URL
    link = 'https://www.amazon.com/dp/{}'.format(asin)
    driver.get(link)
    sleep(random.randint(5, 10))
    # ================================Get title
    title_elements = driver.find_elements(By.CSS_SELECTOR, "div.centerColAlign span#productTitle")
    titles = [elem.text for elem in title_elements]
    # ==================================Get price/list price
    price_whole_elements = driver.find_elements(By.CSS_SELECTOR, "div#corePrice_feature_div span.a-price-whole")
    price_fraction_elements = driver.find_elements(By.CSS_SELECTOR, "div#corePrice_feature_div span.a-price-fraction")
    new_prices = [f"{price_whole_elements[i].text}.{price_fraction_elements[i].text}"
                  for i in range(len(price_whole_elements))]

    list_price_elements = driver.find_elements(By.CSS_SELECTOR,
                                               "div#corePriceDisplay_desktop_feature_div .basisPrice [aria-hidden]")
    list_prices = [elem.text for elem in list_price_elements]
    if not list_prices:
        list_prices.append('')
    # =======================================Get rating
    rating_elements = driver.find_elements(By.CSS_SELECTOR, "span.reviewCountTextLinkedHistogram")
    ratings = [elem.get_attribute('title') for elem in rating_elements]
    # =======================================Get rating count
    rating_count_elements = driver.find_elements(By.CSS_SELECTOR, "a#acrCustomerReviewLink")
    rating_counts = set([elem.text for elem in rating_count_elements])
    # =======================================Get image url
    image_url_elements = driver.find_elements(By.CSS_SELECTOR, "div.imgTagWrapper img[src]")
    image_urls = [elem.get_attribute('src') for elem in image_url_elements]
    # =====================================DataFrame
    df = pd.DataFrame(list(zip(titles, new_prices, list_prices, ratings, rating_counts, image_urls)),
                      columns=['title', 'new_price', 'list_price', 'rating', 'rating_count', 'image_url'])
    df.insert(0, "asin", asin)
    df['list_price'] = df['list_price'].str[1:]
    return df


dfs = []

for asin in asins:
    df = extract_product_detail(asin)
    dfs.append(df)

result = pd.concat(dfs)
result.to_csv('output/exercise_2.csv', index=False)
