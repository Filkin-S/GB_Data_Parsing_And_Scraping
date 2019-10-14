import requests
import json


lyrics_api_link = 'https://orion.apiseeds.com/api/music/lyric'
artist = input('Введите имя исполнителя: ')
track = input('Введите название песни: ')
apikey = '5KKjrguKyS9V0GPzosuYJdwDBeTofU5TllxHqJoFzQyHM2RMuXa2JRCWQyqPH92C'

req = requests.get(f'{lyrics_api_link}/{artist}/{track}?apikey={apikey}')
lyrics = json.loads(req.text)
lyrics_text = (lyrics['result']['artist']['name'] + ' - ' +
               lyrics['result']['track']['name'] + '\n\n' +
               lyrics['result']['track']['text'] + '\n\n')

print(lyrics_text)

with open(f'{artist}_{track}_lyrics', 'w', encoding='utf-8') as j:
    json.dump(lyrics, j)
print('Результат в формате json записан в файл ', f'{artist}_{track}_lyrics.json')

