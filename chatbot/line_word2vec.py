import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

import sys
sys.path.append('../data')
import emo_classify

# Flask app should start in global layout
app = Flask(__name__)

@app.route("/", methods=['GET'])  # 這應該是測試的，對應忘記打webhook的情況
def hello():
    return "Hello World!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = makeWebhookResult(req)  # 把資料丟進我的機器學習模型，處理後再丟出來

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):   # 程式邏輯之所在      
    result = req.get("queryResult")
    parameters = result.get("parameters")
    comments = parameters.get("comments")
    print(comments)
    result = emo_classify.retrieve(comments)  # 資料丟進機器學習模型，處理後再丟出來
    if result['emo'].iloc[0] > 0:
        speech = '您開心我們也開心！期待很快能再見到您！'
    elif result['emo'].iloc[0] < 0: 
        speech = '對不起，似乎讓您有不好的體驗，隨即贈送折價券給您！'
    else:
        speech = '您的意見我們收到了，感謝您的稱讚和指教，我們會繼續努力，隨即贈送折價券給您！'
    #speech就是回應的內容
    print("Response:")
    print(speech)
    #回傳
    return {
        "fulfillmentText":speech
    }

if __name__ == "__main__":          # 啟動server
    app.run(debug=True, port=5000)