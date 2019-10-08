from fftcg_parser import *
import json
from flask import Flask, escape, request, Response
import re


app = Flask(__name__)

def checkAPI():
    args = request.args

    with open('settings.json', 'r') as myfile:
        settings = json.load(myfile)

    if settings['API_KEY'] == args['api_key']:
        return True
    else:
        return False


@app.route('/api/card/<code>')
def hello(code):
    if checkAPI() is True:
        card_list = []
        for card in mycards:
            if code in card['Code']:
                card_list.append(card)

        if len(card_list) == 1:
            return card_list[0]
        else:
            return Response(json.dumps(card_list), mimetype='application/json')
    else:
        return Response('401 Unauthorized API Key', 401)


@app.route('/api/set/<opus>')
def set_grab(opus):
    if checkAPI() is True:
        card_list = []
        for card in mycards:
            if int(opus) == int(roman.fromRoman(card['Set'].split()[1])):
                card_list.append(card)

        return Response(json.dumps(card_list), mimetype='application/json')
    else:
        return Response('401 Unauthorized API Key', 401)


@app.route('/api/')
def hello2():
    if checkAPI() is True:
        return Response(json.dumps(mycards), mimetype='application/json')
    else:
        return Response('401 Unauthorized API Key', 401)


#mycards = loadJson('https://fftcg.square-enix-games.com/en/get-cards')
mycards = loadJson('http://ffdecks.com/api/cards/basic')
mycards = ffdeckstomarcieapi(mycards)


if __name__ == '__main__':
    app.run()
