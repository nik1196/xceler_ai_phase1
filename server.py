
from flask import Flask, jsonify, request
import re
import socket
from stage1_calc4 import *

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def input_process():
        reply = {"reply":"Hello, how may i help you?"}
        return jsonify(reply)
@app.route('/input', methods = ['GET', 'POST'])
def input_process2():
        print(request)
        query = request.json['input']
	x = Calculator(query)
        result = x.calc()
        
        print(result)
        if result:
                reply = {"reply":' '.join(str(i) for i in result)}
                return jsonify(reply)
        else:
                reply = {"reply":"Invalid or malformed request, please try again."}
                return jsonify(reply)
if __name__ == '__main__':
    port = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    x = s.getsockname()[0]
    print(x)
    app.run(host=x, port=port)
