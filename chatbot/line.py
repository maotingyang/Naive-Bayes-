import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

import sys
sys.path.append('../src')
import testing

# Flask app should start in global layout
app = Flask(__name__)
testing.load_training_data('../model/ntusd_model.db','../dict/ntusd-full.dic')

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    #askweather的地方是Dialogflow>Intent>Action 取名的內容
    # if req.get("result").get("action") != "askweather":
    #     return {}
    result = req.get("queryResult")
    parameters = result.get("parameters")
    #parameters.get("weatherlocation")的weatherlocation是Dialogflow > Entitiy
    #也就是步驟josn格式中parameters>weatherlocation
    comments = parameters.get("comments")
    if "咖啡" in comments:
        comments = comments.replace("咖啡", "")  
        print(comments)
    #先設定一個回應
    #如果是Taipei,cost的位置就回營18
    # cost = {'Taipei':'18', 'Kaohsiung':'20', 'Taichung':'10','Tainan':'25'}
    result = testing.test_sentance(comments)
    if result['pos'] > result['neg']:
        speech = '您開心我們也開心！期待很快能再見到您！'
    elif result['neg'] > result['pos']:
        speech = '對不起，似乎讓您有不好的體驗，隨即贈送折價券給您！'
    else:
        speech = '您的意見我們收到了，感謝您的稱讚和指教，我們會繼續努力，隨即贈送折價券給您！'
    #speech就是回應的內容
    # speech = "The temperatrue of " + zone + " is " + str(cost[zone])
    print("Response:")
    print(speech)
    #回傳
    return {
        "fulfillmentText":speech
        # "speech": speech,
        # "displayText": speech,
        # #"data": {},
        # #"contextOut": [],
        # "source": "agent"
    }

if __name__ == "__main__":
    app.run(debug=True,port=5000)