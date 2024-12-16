import time

from undetected_chromedriver import Chrome

driver = Chrome()
category_ids = 'c413893'
driver.get("https://www.wayfair.com/furniture/sb0/sectionals-{}.html?curpage=1".format(category_ids))
pre_height = driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
count = 1

while True:
    print('-----scroll: {} times'.format(count))
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')
    print('new_height: {}\npre_height:{}'.format(new_height, pre_height))
    if new_height == pre_height:
        print("scroll done!!")
        break
    count += 1
    pre_height =new_height

time.sleep(10)