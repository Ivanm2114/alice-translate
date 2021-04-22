import os
import requests
from flask import Flask, request
import logging
import json
import random

start = True
app = Flask(__name__)

sessionStorage = {}

logging.basicConfig(level=logging.INFO)


# создаем словарь, в котором ключ — название города,
# а значение — массив, где перечислены id картинок,
# которые мы записали в прошлом пункте.
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
    user_id = req['session']['user_id']

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None
        }
        return

    # если пользователь не новый, то попадаем сюда.
    # если поле имени пустое, то это говорит о том,
    # что пользователь еще не представился.
    if sessionStorage[user_id]['first_name'] is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.
        # И спрашиваем какой город он хочет увидеть.
        else:
            sessionStorage[user_id]['first_name'] = first_name
        res['response']['text'] = 'Привет, я переводчик\n' \
                                  'Испльзуйте конструкцию:\n "Переведи слово: (слово для перевода)"'
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


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
