import os
import requests
from flask import Flask, request
import logging
import json
import random

start = True
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# создаем словарь, в котором ключ — название города,
# а значение — массив, где перечислены id картинок,
# которые мы записали в прошлом пункте.

cities = {
    'москва': ['1540737/daa6e420d33102bf6947',
               '213044/7df73ae4cc715175059e'],
    'нью-йорк': ['1652229/728d5c86707054d4745f',
                 '1030494/aca7ed7acefde2606bdc'],
    'париж': ["1652229/f77136c2364eb90a3ea8",
              '3450494/aca7ed7acefde22341bdc']
}

countries = {
    'москва': ['россия', 'российская федерация'],
    'нью-йорк': ['сша', 'соединенные штаты америки'],
    'париж': ['франция']
}

# создаем словарь, где для каждого пользователя
# мы будем хранить его имя
sessionStorage = {}

city = ''
city_guessed = False


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return json.dumps(response)


def handle_dialog(res, req):
    word = req['original_utterance'].split(':')[1]

    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"

    querystring = {"langpair": "ru|en", "q": word, "mt": "1", "onlyprivate": "0", "de": "a@b.c"}

    headers = {
        'x-rapidapi-key': "ff62ce869dmsh19d414c170f39aep18e37ajsn5ee33a675609",
        'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

    res['response']['text'] = response['responseData']['translatedText']
    return 


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
