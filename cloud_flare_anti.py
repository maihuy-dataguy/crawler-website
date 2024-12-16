import time
from selenium import webdriver
# import undetected_chromedriver as uc
from undetected_chromedriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from seleniumbase import Driver
from seleniumbase import SB
import sys

# def gen_driver():
#     try:
#         user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36"
#         chrome_options = uc.ChromeOptions()
#         # chrome_options.add_argument('--headless=new')
#         chrome_options.add_argument("--start-maximized")
#         chrome_options.add_argument("user-agent={}".format(user_agent))
#         driver = uc.Chrome(options=chrome_options)
#         stealth(driver,
#                 languages=["en-US", "en"],
#                 vendor="Google Inc.",
#                 platform="Win32",
#                 webgl_vendor="Intel Inc.",
#                 renderer="Intel Iris OpenGL Engine",
#                 fix_hairline=True
#                 )
#         return driver
#     except Exception as e:
#         print("Error in Driver: ", e)


# chrome = webdriver.Chrome(options=options)


with SB(uc=True, test=True) as sb:
    url = "https://www.scrapingcourse.com/cloudflare-challenge"
    sb.uc_open_with_reconnect(url, 4)
    print(sb.get_page_title())
    sb.uc_gui_handle_cf()  # Ready if needed!
    print(sb.get_page_title())
    sb.assert_element('input[name*="email"]')
    sb.assert_element('input[name*="login"]')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
