from lxml import html
import requests
import pandas as pd
from datetime import datetime

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

main_link1 = 'https://mail.ru'
main_link2 = 'https://lenta.ru'
df_m = pd.DataFrame(columns=['Source', 'Title', 'Link', 'Date'])
df_l = pd.DataFrame(columns=['Source', 'Title', 'Link', 'Date'])



# Mail.ru

req = requests.get(main_link1, headers = headers).text
root = html.fromstring(req)

title_list = root.xpath("//h3[contains(@class,'news-item__title')]/text() | //div[contains(@class,'news-item_inline')]//a/text()")
link_list = root.xpath("//div[contains(@class, 'news-item_main')]/a/@href | //div[contains(@class, 'news-item_inline')]//a/@href")
date_list = []
for i in link_list:
    if 'https:' in i:
        req = requests.get(i, headers = headers).text
        root = html.fromstring(req)
        date_news = root.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
        try:
            date_list.append(date_news[0])
        except:
            date_list.append(datetime.today().strftime('%d-%m-%Y'))
    else:
        date_list.append(datetime.today().strftime('%d-%m-%Y'))
    
for j in range(len(title_list)):
    df_m.loc[len(df_m)] = [main_link1, title_list[len(df_m)], link_list[len(df_m)], date_list[len(df_m)]]
    

# Lenta.ru

req = requests.get(main_link2, headers = headers).text
root = html.fromstring(req)

title_list = root.xpath("//div[@class='first-item']//h2//a/text() | //div[contains(@class, 'span8')]//div[@class='item']/a/text()")
link_list = root.xpath("//div[@class='first-item']//h2//a/@href | //div[contains(@class, 'span8')]//div[@class='item']/a/@href")
for i in range(len(link_list)):
    if 'https:' not in link_list[i]:
        link_list[i] = main_link2 + link_list[i]
date_list = root.xpath("//div[@class='first-item']//h2//a/time/@datetime | //div[contains(@class, 'span8')]//div[@class='item']/a/time/@datetime")

for j in range(len(title_list)):
    df_l.loc[len(df_l)] = [main_link2, title_list[len(df_l)], link_list[len(df_l)], date_list[len(df_l)]]
    
df = pd.concat([df_m, df_l], join='outer', ignore_index=True)
print(df.to_string())