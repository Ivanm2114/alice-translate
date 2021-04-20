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

start = True

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
    global start
    if start:
        res['response']['text'] = 'Привет, я переводчик\n' \
                                  'Испльзуйте конструкцию: "Переведи слово: (слово для перевода)"'
        start = False
    else:
        word = req['request']["original_utterance"].split(':')[1]

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
