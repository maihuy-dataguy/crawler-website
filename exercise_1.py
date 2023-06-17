from pandas import DataFrame
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd

# Category_id (shall init on configuration)
category_ids = ['193870011', '172456', '16225007011']

# Declare browser
driver = webdriver.Chrome('chromedriver')


def extract_best_seller_product_info(link):
    # Open URL
    driver.get(link)
    sleep(random.randint(5, 10))
    # ================================Get rank
    rank_elements = driver.find_elements(By.CSS_SELECTOR, ".zg-bdg-body")
    ranks = [elem.text for elem in rank_elements[:8]]

    # ==================================Get link/name
    link_elements = driver.find_elements(By.CSS_SELECTOR, ".p13n-sc-uncoverable-faceout [tabindex]")
    links = [elem.get_attribute('href') for elem in link_elements[:8]]
    name_elements = driver.find_elements(By.CSS_SELECTOR, "._cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
    names = [elem.text for elem in name_elements[:8]]
    # ====================================Get price
    price_elements = driver.find_elements(By.CSS_SELECTOR, ".p13n-sc-uncoverable-faceout .a-size-base")
    prices = [elem.text for elem in price_elements[:8]]
    # =====================================DataFrame
    df = pd.DataFrame(list(zip(ranks, names, prices, links)), columns=['rank', 'product_name', 'price', 'url'])
    df['price'] = df['price'].str[1:]
    df.insert(0, "category_id", link.split('/')[-1])
    return df


dfs = []

for category_id in category_ids:
    df = extract_best_seller_product_info('https://www.amazon.com/gp/bestsellers/hi/{}'.format(category_id))
    dfs.append(df)

result = pd.concat(dfs)
result.to_csv('output/exercise_1.csv', index=False)
