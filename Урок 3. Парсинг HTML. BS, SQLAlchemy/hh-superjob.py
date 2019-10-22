from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
from pymongo import MongoClient
from pprint import pprint

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
main_link_hh ='https://hh.ru/search/vacancy?text='
main_link_sj = 'https://www.superjob.ru'
vacancy = 'python'
pages = 9
df = pd.DataFrame(columns=['vacancy_title', 'company_title', 'vacancy_address', 'vacancy_link', 'min_salary', 'max_salary', 'salary_currency', 'source'])

#HeadHunter

for i in range(0, pages+1):
    html = requests.get(main_link_hh + vacancy + '&page=' + str(i), headers=headers).text
    parsed_html = bs(html,'lxml')

    vacancies = parsed_html.find_all('div',{'class':'vacancy-serp-item'})
    for v in vacancies:
        vacancy_title = v.find('a', {'data-qa':'vacancy-serp__vacancy-title'}).get_text()
        vacancy_company = v.find('div', {'class':'vacancy-serp-item__meta-info'}).get_text()
        vacancy_address = v.find('span', {'data-qa':'vacancy-serp__vacancy-address'}).get_text()
        vacancy_link = v.find('a', {'data-qa':'vacancy-serp__vacancy-title'})['href']
        vacancy_salary = v.find('div', {'data-qa':'vacancy-serp__vacancy-compensation'})
        if not vacancy_salary:
            salary_min = None
            salary_max = None
            salary_cur = None
        else:
            salary = re.findall('\d+[\s\d]*', vacancy_salary.get_text().replace('\xa0', ''))
            salary_cur = re.search('([A-яA-z]{3}\.*)', vacancy_salary.get_text()).group()
            if len(salary) > 1:
                salary_min = int(salary[0])
                salary_max = int(salary[1])
            else:
                if 'от' in vacancy_salary.get_text():
                    salary_min = int(salary[0])
                    salary_max = None
                else:
                    salary_min = None
                    salary_max = int(salary[0])
        df.loc[len(df)] = [vacancy_title, vacancy_company, vacancy_address, vacancy_link, salary_min, salary_max, salary_cur, 'HeadHunter']


#SuperJob

for i in range(pages+1):
    html = requests.get(main_link_sj +'/vacancy/search/?keywords=' + vacancy + '&page=' + str(i), headers=headers).text
    parsed_html = bs(html,'lxml')

    vacancies = parsed_html.find_all('div',{'class':'_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})

    for v in vacancies:
        vacancy_title = v.find('div', {'class':'_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).get_text()
        vacancy_company = v.find('span', {'class':'_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _3e53o _15msI'}).get_text()
        vacancy_address = v.find('span', {'class':'_3mfro f-test-text-company-item-location _9fXTd _2JVkc _3e53o'}).span.next_sibling.next_sibling.get_text()
        vacancy_link = main_link_sj + v.find('div', {'class':'_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).parent['href']
        vacancy_salary = v.find('span', {'class':'_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).get_text().replace('\xa0', '')

        if vacancy_salary == 'По договорённости':
            salary_min = None
            salary_max = None
            salary_cur = None
        else:
            salary = re.findall('\d+[\s\d]*', vacancy_salary)
            salary_cur = 'руб.'
            if len(salary) > 1:
                salary_min = int(salary[0])
                salary_max = int(salary[1])
            else:
                if 'от' in vacancy_salary:
                    salary_min = int(salary[0])
                    salary_max = None
                else:
                    salary_min = None
                    salary_max = int(salary[0])
        df.loc[len(df)] = [vacancy_title, vacancy_company, vacancy_address, vacancy_link, salary_min, salary_max, salary_cur, 'SuperJob']

print(df.info())
print(df.head().to_string())
print(df.tail().to_string())


# Подключаемся к MongoDB
client = MongoClient('localhost',27017)
db = client['BG_256']
vacs = db.vacancies_hh_sj


# Функция для отправки датафрейма в базу
def insert_mongo(df):
    vacs.insert_many(df.to_dict('records'))

# Функция для вывода на экран вакансий с зп больше указанной суммы
def show_min_salary(sal):
    v_s = vacs.find({'$or': [{'min_salary':{'$gt': sal}}, {'max_salary':{'$gt': sal}}]})
    for i in v_s:
        pprint(i)

insert_mongo(df)

show_min_salary(100000)


# Функцию update не смог реализовать. По хорошему должна быть одна функция - либо вставляет новые 
# значения, либо обновляет существующие. Но update не работает по аналогии с insert, с параметрами
# не разобрался, все время ошибки.
# vacs.update_many({}, {df_dict}, True)

