from flask import Flask, request, render_template, redirect


import json
from flask.helpers import url_for
import numpy as np
import encoder
import decoder
app = Flask(__name__)



host = "http://localhost:80"

@app.route('/')
def index():
    # making list of pokemons
    lines =[]
    with open("./templates/ids.txt") as f:
        raw_data = f.readlines()

    for line in raw_data:
        lines.append(line)

    return render_template('table.html', len = len(lines), Data = lines)
    # return render_template('table.html')

@app.route('/client')
def client():
    title = "Hello"
    return render_template('index.html')


@app.route('/get', methods=['GET'])
def getData():
    idList = request.args.get('data')
    
    response = decoder.retrieve_data(host + "/sub", idList)
    response_list = json.loads(response)

    id_refined = decoder.refine_id(json.loads(idList))
    org_msg = decoder.get_original_msg(response_list, id_refined)
    print("Original Message..")
    print(org_msg)

    return org_msg

@app.route('/post', methods=['POST'])
def postData():

    data = request.form['data']
    print("Sending Data ...")
    response, id = encoder.send(host + '/pub', data)

        # Open a file with access mode 'a'
    with open("./templates/ids.txt", "a") as file_object:
        file_object.write(str(id) + '\n')


    return str(id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)