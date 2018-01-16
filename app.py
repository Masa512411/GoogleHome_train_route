import os
import json
import re
from datetime import datetime

from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response

import bs4
import requests 

app = Flask(__name__)

@app.route('/webhook',methods=['POST']) 
def main():
    req = request.get_json()
    train_route_name = req["result"]["parameters"]["train_route"]

    if train_route_name == "山陽本線":
        url = "https://transit.yahoo.co.jp/traininfo/detail/332/418/"
    elif train_route_name == "呉線":
        url = "https://transit.yahoo.co.jp/traininfo/detail/502/0/"
    
    operation_info = requests.get(url)
    soup = bs4.BeautifulSoup(operation_info.text,'lxml')

    if soup.findAll("span",{"class":"icnNormalLarge"}):
       speech = "{}は平常運転中です".format(train_route_name)
    else:
        delay_info = soup.findAll("dd",{"class":"trouble"})
        speech = delay_info[0].p.string

    res = make_response(jsonify({'speech':speech,'displayText':speech}))
    res.headers['Contest-Type'] = 'application/json'
    return res


if __name__ == '__main__':
    app.run()