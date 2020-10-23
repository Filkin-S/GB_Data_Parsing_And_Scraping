from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import json

df = pd.DataFrame(columns=['ProductID', 'ProductName', 'ProductBrand', 'ProductCategoryName', 'ProductPrice'])

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')
time.sleep(5)
try:
    iframe = driver.find_element_by_class_name('flocktory-widget')
    driver.switch_to.frame(iframe)
    button = driver.find_element_by_class_name('PushTip-close')
    button.click()
    print('закрыли окно')
except:
    print('Нет всплывающего окна')
time.sleep(5)
# Здесь ожидание кликабельности так и не заработало. Выдает ошибку
# __init__() takes 2 positional arguments but 3 were given
# Пришлось по-кривому. Но кнопку все равно не всегда находит почему-то.
while True:
    try:
        # button = WebDriverWait(driver,10).until(
        #     EC.element_to_be_clickable(By.XPATH, '//div[@data-init="ajax-category-carousel"][1]//a[@class="next-btn sel-hits-button-next"]')
        # )
        button = driver.find_element_by_xpath('//div[@data-init="ajax-category-carousel"][1]//a[@class="next-btn sel-hits-button-next"]')
        button.click()
        print('кнопка нажата')
        time.sleep(2)
    except Exception as e:
        print(e)
        break

# Далее проблем никаких - информация лежит в json формате и мы просто берем её.
goods = driver.find_elements_by_xpath("//div[@data-init='ajax-category-carousel'][1]//a[@class='sel-product-tile-title']")\

for good in goods:
    good_info = json.loads(good.get_attribute('data-product-info'))
    ProductID = good_info["productId"]
    ProductName = good_info["productName"]
    ProductBrand = good_info["productVendorName"]
    ProductCategoryName = good_info["productCategoryName"]
    ProductPrice = good_info["productPriceLocal"]
    df.loc[len(df)] = [ProductID, ProductName, ProductBrand, ProductCategoryName, ProductPrice]

print(df.to_string())
