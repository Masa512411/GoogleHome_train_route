import os
import json

from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response

import bs4
import requests 

app = Flask(__name__)

@app.route("/webhook",methods=['POST']) 
def webhook():
    req = request.get_json()
    train_route_name = req["result"]["parameters"]["train_route"]

    if train_route_name == "山陽本線":
        url = "https://transit.yahoo.co.jp/traininfo/detail/332/418/"
    elif train_route_name == "呉線":
        url = "https://transit.yahoo.co.jp/traininfo/detail/502/0/"
    
    operation_info = requests.get(url)
    soup = bs4.BeautifulSoup(operation_info.text,'lxml')
    update_time = soup.findAll("span",{"class":"subText"})[0].string
    

    if soup.findAll("span",{"class":"icnNormalLarge"}):
       speech = "{}は平常運転中です。{}".format(train_route_name,update_time)
    else:
        delay_info = soup.findAll("dd",{"class":"trouble"})
        speech = "{}。{}".format(delay_info[0].p.string,update_time)

    res = make_response(jsonify({'speech':speech,'displayText':speech}))
    res.headers['Content-Type'] = 'application/json'    
    return res
    

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    
    app.run(debug=False,port=port,host='0.0.0.0')
