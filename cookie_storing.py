import time
import random
import pickle

from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By


def load_cookies(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)


driver = Chrome()
driver.get("https://www.scrapingcourse.com/antibot-challenge")
while True:
    rating_elements = driver.find_elements(By.CSS_SELECTOR, "div#challenge-info")
    if len(rating_elements) > 0:
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        print(rating_elements[0].text)
        break

driver2 = Chrome()
driver2.get("https://www.scrapingcourse.com/antibot-challenge")
while True:
    load_cookies(driver2)
    driver2.get("https://www.scrapingcourse.com/antibot-challenge")
    time.sleep(5)
    rating_elements = driver2.find_elements(By.CSS_SELECTOR, "div#challenge-info")
    if len(rating_elements) > 0:
        print(rating_elements[0].text)
        break
