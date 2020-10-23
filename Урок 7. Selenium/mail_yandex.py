from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

df = pd.DataFrame(columns=['title', 'sender', 'date', 'text'])
login = input('Введите адрес почты на Яндекс: ')
password = input('Введите пароль: ')

driver = webdriver.Chrome()
driver.get('https://mail.yandex.ru')
assert "Яндекс.Почта" in driver.title
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'button2_theme_mail-white')))
button = driver.find_element_by_class_name('button2_theme_mail-white')
button.click()
#Вводим логин
time.sleep(1)
elem = driver.find_element_by_id('passp-field-login')
elem.send_keys(login)
elem.send_keys(Keys.RETURN)
#Вводим пароль
time.sleep(1)
elem = driver.find_element_by_id('passp-field-passwd')
elem.send_keys(password)
elem.send_keys(Keys.RETURN)
# После пароля может появиться предложение подключить уведомления,
# но у меня появилось только 1 раз, повторить не смог, чтобы прописать.
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'mail-MessageSnippet')))
# Находим все ссылки на письма, циклом заходим в каждое и собираем инфо в датасет.
mails = [link.get_attribute("href") for link in driver.find_elements_by_class_name('mail-MessageSnippet')]
for mail in mails:
    driver.get(mail)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'mail-Message-Body-Content')))
    title = driver.find_element_by_class_name('mail-Message-Toolbar-Subject').text
    sender = driver.find_element_by_class_name('mail-Message-Sender-Email').text
    date = driver.find_element_by_class_name('ns-view-message-head-date').text
    text = driver.find_element_by_class_name('mail-Message-Body-Content').text
    df.loc[len(df)] = [title, sender, date, text]

print(df.to_string())

