#-*-coding:UTF-8 -*-
from flask import Flask
from flask import jsonify,  request
import json
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False


#建立url路徑---------------------------------------------------------------------------    

@app.route("/",methods=['GET'])
def home():
    return ('hello!')

@app.route("/shopee",methods=['GET'])
def shopee():

    #json data---------------------------------------------------------------------------
    f = open('shopee.json',encoding='UTF-8')
    data = json.load(f)
    data = tuple(data)
    f.close()
    
    aaa = []
    bbb = []
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
        try:
            for j in range(int(n)):
                bbb.append(aaa[j])
        except:
            pass

        for k in bbb:
            k['content'] = k['content'].split(k['content'][int(w)],1)[0]
            results.append(k)
            
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)