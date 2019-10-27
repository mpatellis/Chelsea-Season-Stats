import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

# This was my testing ground before I went to Jupyter Notebook
# It isn't really a complete picture of what I did but it's something so I felt I needed to include it

# 18 Chelsea fc
# 5  europa league league id
# 12945 2018/19 europa league season
# 8  premier league
# 12962 2018/19 premier league
# 24 fa cup
# 13136 2018/19 fa cup

# Not needed because everything is placed into dataframe.csv but I wanted it
# because I feel bad just deleting all my work
def buildDF():
    # FA Cup Reading
    ffr = open("fa_squad_format.txt", "r")

    fadf = pd.read_json(ffr, lines=True)
    fadf.set_index('player_id', inplace=True)
    fadf.drop(['position_id', 'number', 'captain', 'injured'], axis=1, inplace=True)

    # Premier League Reading
    fpr = open("premier_squad_format.txt", "r")

    premierdf = pd.read_json(fpr, lines=True)
    premierdf.set_index('player_id', inplace=True)
    premierdf.drop(['position_id', 'number', 'captain', 'injured'], axis=1, inplace=True)

    # Europa Squad Reading
    fer = open("europa_squad_format.txt", "r")

    europadf = pd.read_json(fer, lines=True)
    europadf.set_index('player_id', inplace=True)
    europadf.drop(['position_id', 'number', 'captain', 'injured'], axis=1, inplace=True)

    # Create total dataframe
    df = premierdf.add(fadf, fill_value=0)
    df = df.add(europadf, fill_value=0)
    df.fillna(0, inplace=True)

    f = open("dataframe.csv", "w")
    f.write(df.to_csv())
    f.close()

def get(endpoint, includes=''):
    http = 'https://soccer.sportmonks.com/api/v2.0'
    token = '?api_token=MyAPITokenWouldGoHere'
    rq = http + endpoint + token + includes
    print(rq)
    rs = requests.get(rq)

    if rs:
        print("API Call Successful")
    else:
        print("API Call Unsuccessful with code: " + str(rs.status_code))
    return rs

# If only I had googled instead of rewriting all this code
def processRawText(data):
    # Remove to [] and related } and ]
    try:        
        indexbracket = data.index("[") + 1
        data = data[indexbracket:len(data)-3]
    except ValueError:
        print("No {} or [] found")

    finalstr = ""
    strlen = len(data)
    i = 0
    while i < strlen:
        try:
            indexC = data.index('{', i, strlen)
        except ValueError:
            print("err")
            return finalstr

        if i != 0 and data[indexC-1] == ':':
            indexQ = indexC - 3
            name = ""

            while data[indexQ] != '\"':
                name = data[indexQ] + name
                indexQ -= 1
            finalstr = finalstr + data[i-1:indexQ]

            indexD = indexC + 2
            newdata = ""
            newdata = "\"" + name + "_"
            while data[indexD] != '}':
                if data[indexD] == ',':
                    finalstr = finalstr + newdata + ","
                    newdata = "\"" + name + "_"
                    indexD += 1
                else:
                    newdata = newdata + data[indexD]
                indexD += 1

            finalstr = finalstr + newdata
            if data[indexD + 1] == "}" and indexD + 2 != strlen:
                finalstr = finalstr + "},"
            elif data[indexD + 1] == "}" and indexD + 2 == strlen:
                finalstr = finalstr + "}"
            i = indexD + 2
        else:
            i += 1
    return finalstr

def init():
    f = open("dataframe.csv", "r")
    df = pd.read_csv(f)
    return df



end = '/players/'
inc = '&include='
r = get(end)
print(r.text)
df = init()

print(df.head(10))