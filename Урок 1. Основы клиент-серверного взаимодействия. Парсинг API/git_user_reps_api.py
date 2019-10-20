import requests
import json

git_api_link = 'https://api.github.com/'
user_name = input('Введите имя пользователя GitHub: ')

req_reps = requests.get(f'{git_api_link}users/{user_name}/repos')
user_repos = json.loads(req_reps.text)

print([d["name"] for d in user_repos])

with open(f'{user_name}_repos.json', 'w', encoding='utf-8') as j:
    json.dump([d["name"] for d in user_repos], j)
print('Записано в json в файл ', f'{user_name}_repos.json')
