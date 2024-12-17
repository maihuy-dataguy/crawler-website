import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
driver.get('https://www.wayfair.com/furniture/sb0/sectionals-c413893.html?curpage=1')
element = driver.find_elements(By.XPATH,"//div[@id='px-captcha']")
if len(element)>0:
    action = ActionChains(driver)
    click = ActionChains(driver)
    action.click_and_hold(element[0])
    action.perform()
    time.sleep(10)
    action.release(element[0])
    action.perform()
    time.sleep(0.2)
    action.release(element[0])

driver.get('https://www.wayfair.com/furniture/sb0/sectionals-c413893.html?curpage=1')
time.sleep(100)