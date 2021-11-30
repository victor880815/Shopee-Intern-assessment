#-*-coding:UTF-8 -*-
from flask import Flask
from flask import jsonify,  request
import json
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False


#json data---------------------------------------------------------------------------
import json
f = open('shopee.json',encoding='UTF-8')
data = json.load(f)

f.close()

#建立url路徑---------------------------------------------------------------------------    
@app.route("/",methods=['GET'])
def home():
    return ('hello!')

@app.route("/shopee",methods=['GET'])
def test(): 
    #用於資料型態轉換之list  
    aaa = []
    ccc=[]
    #回傳之list
    results = []
    if 'q' and 'n' and 'w' in request.args:
        q = request.args['q']
        n = request.args['n']
        w = request.args['w']
        q = q.split(',')
        for i in data:
            for word in q:
                if word in i['content']:
                    aaa.append(i)
                elif word in i['comment']:
                    aaa.append(i)
        #print(aaa)
        try:
            for j in range(int(n)):
                bbb = tuple(aaa)
                print(bbb)
                results.append(bbb[j])
                ddd = tuple(ccc)
            for k in ddd:
                k['content'] = k['content'].split(k['content'][int(w)],1)[0]
                results.append(k)
        except:
            pass

    return jsonify(results)
    

if __name__ == "__main__":
    app.run(debug=True)