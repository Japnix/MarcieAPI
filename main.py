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


def makecards():

    cards = loadJson('https://fftcg.square-enix-games.com/en/get-cards')

    mykeys = ('Element', 'Name_EN', 'Cost', 'Code', 'Multicard', 'Type_EN', 'Category_1', 'Text_EN', 'Job_EN', 'Power',
              'Ex_Burst', 'Set', 'Rarity')

    for card in cards:
        for key in list(card):
            if key in mykeys:
                if key == "Multicard" or key == "Ex_Burst":
                    card[key] = prettyTrice(card[key])
                    if card[key] == "True":
                        card[key] = True
                    else:
                        card[key] = False
                elif key == 'Power':
                    if card[key] == "":
                        card[key] = None
                    else:
                        card[key] = card[key]
                elif key == "Rarity":
                    card[key] = card[key][0]
                elif key == "Code":
                    if re.search(r'PR-\d{3}', card[key]):
                        card[key] = card[key]
                    else:
                        card[key] = card[key][:-1]
                else:
                    card[key] = prettyTrice(card[key])
            else:
                del card[key]

        card['Text_EN'] = card['Text_EN'].split('\n')

    with open('cards.json', 'w') as outfile:
        json.dump(cards, outfile)

    myjson = json.dumps(cards)
    mydict = json.loads(myjson)

    return mydict


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


with open('completeset.json', 'r') as infile:
    mycards = json.load(infile)


if __name__ == '__main__':
    app.run()
