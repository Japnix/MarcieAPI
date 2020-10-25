import json
import re
import urllib.request
import roman
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')


def getimageURL(code):
    """This function takes in a code as a string and returns an image link which points to square"""

    if re.search(r'[0-9]+\-[0-9]{3}[a-zA-Z]/[0-9]+\-[0-9]{3}[a-zA-Z]', code):
        URL = 'https://fftcg.cdn.sewest.net/images/cards/full/' + code[-6:] + '_eg.jpg'
    else:
        URL = 'https://fftcg.cdn.sewest.net/images/cards/full/' + code + '_eg.jpg'

    return URL


def urlset(cards_list):
    """This function takes in list of cards and creates a list of URL's and returns it as a list"""

    url_list = []
    for card in cards_list:
        if re.search(r'\/', card['Code']):
            for x in card['Code'].split('/'):
                if re.search(r'H|R|P|C|L', x):
                    url_list.append(
                        'https://storage.googleapis.com/marcieapi-images/' + x + '_eg.jpg')
                else:
                    url_list.append(
                        'https://storage.googleapis.com/marcieapi-images/' + x + card['Rarity'] + '_eg.jpg')
        elif card['Rarity'] == "P":
            url_list.append(
                'https://storage.googleapis.com/marcieapi-images/' + card['Code'] + '_eg.jpg')
        else:
            url_list.append(
                'https://storage.googleapis.com/marcieapi-images/' + card['Code'] + card['Rarity'] + '_eg.jpg')
    return list(dict.fromkeys(url_list))


# Loading JSON from file and load it into a variable
# data - untouched JSON from file
# card_list - list of cards

def loadJson(path):
    try:
        data = urllib.request.urlopen(path)
    except:
        return
    else:
        content = data.read().decode('utf-8')
        data = json.loads(content)
        cards_list = data

        return cards_list


def prettyTrice(string):
    # Weird bracket removal:
    string = string.replace(u"\u300a", '(')
    string = string.replace(u"\u300b", ')')
    string = string.replace('&middot;', u"\u00B7")

    # Replace Element Logos
    string = string.replace(u"\u571F", 'Earth')
    string = string.replace(u"\u6c34", 'Water')
    string = string.replace(u"\u706b", 'Fire')
    string = string.replace(u"\u98a8", 'Wind')
    string = string.replace(u"\u6c37", 'Ice')
    string = string.replace(u"\u5149", 'Light')
    string = string.replace(u"\u95c7", 'Dark')
    string = string.replace(u"\u96f7", 'Lightning')

    # Replace EX Burst
    string = string.replace('[[ex]]', '')
    string = string.replace('[[/]]', '')
    string = string.replace('EX BURST', '[EX BURST]')

    # Special Switch
    string = string.replace(u"\u300a"u"\u0053"u"\u300b", '[Special]')

    # Bubble used for Multicard and Ex_Burst
    string = string.replace(u'\u25CB', 'True')
    string = string.replace(u'\u3007', 'False')

    # Horizontal Bar
    string = string.replace(u'\u2015', '')

    # Formatting Fixes
    string = string.replace('[[', '<')
    string = string.replace(']]', '>')
    string = string.replace('<s>', '')
    string = string.replace('</>', '')
    string = string.replace('<i>', '')
    string = string.replace('<br> ', '\n')
    string = string.replace('<br>', '\n')

    # Formatting Fixes
    string = string.replace('[[', '<')
    string = string.replace(']]', '>')
    string = string.replace('<s>', '')
    string = string.replace('</>', '')
    string = string.replace('<i>', '')
    string = string.replace('<br> ', '\n')
    string = string.replace('<br>', '\n')

    # Replace Fullwidth Numbers with normal numbers
    string = string.replace(u"\uFF11", '1')
    string = string.replace(u"\uFF12", '2')
    string = string.replace(u"\uFF13", '3')
    string = string.replace(u"\uFF14", '4')
    string = string.replace(u"\uFF15", '5')
    string = string.replace(u"\uFF16", '6')
    string = string.replace(u"\uFF17", '7')
    string = string.replace(u"\uFF18", '8')
    string = string.replace(u"\uFF19", '9')
    string = string.replace(u"\uFF10", '0')
    string = string.replace(u"\u2015", "-")  # Damage 5 from Opus X cards
    string = string.replace(u"\u00fa", "u")  # Cuchulainn u with tilda

    string = string.replace(u"\u4E00"u"\u822C", 'Generic')  # Fixes #1

    # Tap Symbol
    string = string.replace(u"\u30C0"u"\u30EB", 'Dull')

    # Double quotes with YURI?
    string = string.replace("\"\"", '\"')

    return string


# This function is used to convert information from ffdecks JSON
# to marcieapi JSON.  FFDecks uses different characters to denote
# different things.

def ffdeckstostring(string):
    string = string.replace('{s}', '[Special]')
    string = string.replace('{a}', '(Water)')
    string = string.replace('{w}', '(Wind)')
    string = string.replace('{e}', '(Earth)')
    string = string.replace('{f}', '(Fire)')
    string = string.replace('{i}', '(Ice)')
    string = string.replace('{l}', '(Lightning)')
    string = string.replace('{d}', '(Dull)')

    string = string.replace('{x}', '[EX BURST]')
    string = string.replace('{0}', '(0)')
    string = string.replace('{1}', '(1)')
    string = string.replace('{2}', '(2)')
    string = string.replace('{3}', '(3)')
    string = string.replace('{4}', '(4)')
    string = string.replace('{5}', '(5)')
    string = string.replace('{6}', '(6)')
    string = string.replace('{7}', '(7)')
    string = string.replace('{8}', '(8)')
    string = string.replace('{9}', '(9)')

    string = string.replace('*', '')
    string = string.replace('%', '')
    string = string.replace('~', '')
    string = string.replace(u"\u2015", "-")  # Damage 5 from Opus X cards
    string = string.replace(u"\u00fa", "u")  # Cuchulainn u with tilda

    return string


# This function converts ffdecks inputs to marcieapi output

def ffdeckstomarcieapi(listofdicts):
    converted = []

    for x in range(0, len(listofdicts)):
        converted.append({})

    for card in range(0, len(listofdicts)):
        converted[card]['Category_1'] = ffdeckstostring(listofdicts[card]['category'])
        converted[card]['Code'] = ffdeckstostring(listofdicts[card]['serial_number'])
        converted[card]['Cost'] = listofdicts[card]['cost']
        converted[card]['Element'] = ffdeckstostring(listofdicts[card]['element'])
        converted[card]['Ex_Burst'] = listofdicts[card]['is_ex_burst']
        converted[card]['Job_EN'] = ffdeckstostring(listofdicts[card]['job'])
        converted[card]['Multicard'] = listofdicts[card]['is_multi_playable']
        converted[card]['Name_EN'] = ffdeckstostring(listofdicts[card]['name'])
        converted[card]['Power'] = listofdicts[card]['power']
        converted[card]['Rarity'] = ffdeckstostring(listofdicts[card]['rarity'])[0]

        if re.search(r'^PR-', converted[card]['Code']):
            converted[card]['Set'] = None
        else:
            setnumber = int(re.search(r'^\d+', converted[card]['Code']).group(0))
            converted[card]['Set'] = 'Opus ' + roman.toRoman(setnumber)
        converted[card]['Type_EN'] = ffdeckstostring(listofdicts[card]['type'])
        converted[card]['Text_EN'] = []

        for line in range(0, len(listofdicts[card]['abilities'])):
            converted[card]['Text_EN'].append(ffdeckstostring(str(listofdicts[card]['abilities'][line])))
    return converted


def addimageurltojson(cards_list, image_list):
    for card in cards_list:
        for url in image_list:
            if re.search(r'\/', card['Code']):
                if card['Code'].split('/')[0] in url:
                    card['image_url'] = url
                    card['image_url_jp'] = None

            elif card['Code'] == re.search(r'(PR-\d{3}|\d+-\d{3})', url).group(1):
                card['image_url'] = url
                card['image_url_jp'] = None


    return cards_list


def addjapaneseurls(cards):
    root_url = "http://www.square-enix-shop.com/jp/ff-tcg/card/cimg/large/opus"
    regex = re.compile('([0-9]+)(-[0-9]+)([A-Z])')

    final = []
    for card in cards:
        if re.search(regex, card['image_url']):
            set = re.search(regex, card['image_url']).group(1)
            cardnum = re.search(regex, card['image_url']).group(2)
            rarity = re.search(regex, card['image_url']).group(3)
            card['image_url_jp'] = root_url + set + '/' + set + cardnum + rarity + ".png"
            final.append(card)

    return final


# This function makes a cards JSON from square and writes it to cards.json in the local directory

def squaretomarcieapi(cards):
    mykeys = (
    'Rarity', 'Element', 'Name_EN', 'Cost', 'Multicard', 'Type_EN', 'Category_1', 'Text_EN', 'Job_EN', 'Power',
    'Ex_Burst', 'Set', 'Code')

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
                    elif card[key] == " ":
                        card[key] = None
                    elif re.search(r'\u2015', card[key]):
                        card[key] = None
                    elif re.search(r'\－', card[key]):
                        card[key] = None
                    else:
                        card[key] = int(card[key])
                elif key == "Rarity":
                    card[key] = card[key][0]
                elif key == "Code":
                    if re.search(r'PR-\d{3}', card[key]):
                        card[key] = card[key]
                    elif re.search(r'\/', card[key]):
                        card[key] = card[key]
                    elif re.search(r'S', card[key]):
                        card['Rarity'] = 'S'
                        card[key] = card[key][:-1]
                    else:
                        card[key] = card[key][:-1]
                elif key == "Cost":
                    card[key] = int(card[key])
                else:
                    card[key] = prettyTrice(card[key])
            else:
                del card[key]

        card['Text_EN'] = card['Text_EN'].split('\n')

        for line in range(len(card['Text_EN'])):
            card['Text_EN'][line] = re.sub(r'^\s+', '', card['Text_EN'][line])
            card['Text_EN'][line] = re.sub(r'\s+$', '', card['Text_EN'][line])

    myjson = json.dumps(cards)
    mydict = json.loads(myjson)

    return mydict
