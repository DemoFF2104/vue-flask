from typing import Text
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from rsa import code_message, gcd, decode_message
from keygen import gen_result
from shamir import step_1, step_2, step_3, step_4
from elgamal import key_generation, send_message, decode_message_el
from md5 import getHash
from sha1 import getHashSha

Numbers = [0, 0, 0]
number1 = 0
number2 = 0
TextArr = ['', '', '']
TextArrEl = []
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# sanity check route


@app.route('/number/gcd', methods=['GET', 'POST'])
def gcdR():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        Numbers[0] = post_data.get('number1')
        Numbers[1] = (post_data.get('number2'))
        response_object['message'] = 'Book added!'
    else:
        response_object['numbers'] = gcd(Numbers[0], Numbers[1])
    return jsonify(response_object)


@app.route('/number/inv', methods=['GET', 'POST'])
def invR():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        Numbers[0] = post_data.get('number1')
        Numbers[1] = (post_data.get('number2'))
        response_object['message'] = 'Book added!'
    else:
        response_object['numbers'] = inversion(Numbers[0], Numbers[1])
    return jsonify(response_object)


@app.route('/number/modul', methods=['GET', 'POST'])
def modulR():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        Numbers[0] = post_data.get('number1')
        Numbers[1] = (post_data.get('number2'))
        Numbers[2] = (post_data.get('number3'))
        response_object['message'] = 'Book added!'
    else:
        response_object['numbers'] = modul(Numbers[0], Numbers[1], Numbers[2])
    return jsonify(response_object)


@app.route('/rsa/code', methods=['GET', 'POST'])
def rsaCode():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TextArr[0] = post_data.get('text')
        response_object['message'] = 'Text coded!'
    else:
        codeText, d, n = code_message(TextArr[0])
        response_object['codeText'] = codeText
        response_object['dValue'] = d
        response_object['nValue'] = n
    return jsonify(response_object)


@app.route('/rsa/encode', methods=['GET', 'POST'])
def rsaEncode():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TextArr[0] = post_data.get('text')
        TextArr[1] = post_data.get('dValue')
        TextArr[2] = post_data.get('nValue')
        response_object['message'] = 'Text coded!'
    else:
        encodeText = decode_message(TextArr[0], TextArr[1], TextArr[2])
        response_object['codeText'] = encodeText

    return jsonify(response_object)


@app.route('/keygen', methods=['GET', 'POST'])
def keygen():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        response_object['message'] = 'Text coded!'
    else:
        p, q, g, Xa, Ya, Yb, Xb, answ1, answ2 = gen_result()
        response_object['pValue'] = p
        response_object['qValue'] = q
        response_object['gValue'] = g
        response_object['secKeyA'] = Xa
        response_object['secKeyB'] = Xb
        response_object['opKeyA'] = Ya
        response_object['opKeyB'] = Yb
        response_object['answ1'] = answ1
        response_object['answ2'] = answ2

    return jsonify(response_object)


#/////////////////////////////////Routes Shamir //////////////////////////////////////


@app.route('/shamir/step1', methods=['GET', 'POST'])
def step1():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TextArr[0] = post_data.get('inputTxt')
        response_object['message'] = 'Text coded!'
    else:
        step_2_txt, p, secret_1 = step_1(TextArr[0])
        response_object['pValue'] = p
        response_object['stepTxt1'] = step_2_txt
        response_object['secKeys1'] = secret_1
    return jsonify(response_object)


@app.route('/shamir/step2', methods=['GET', 'POST'])
def step2():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TextArr[0] = post_data.get('inputTxt')
        TextArr[1] = post_data.get('pValue')
        response_object['message'] = 'Text coded!'
    else:
        step_3_txt, secret_2 = step_2(TextArr[0], TextArr[1])
        response_object['stepTxt2'] = step_3_txt
        response_object['secKeys2'] = secret_2

    return jsonify(response_object)


@app.route('/shamir/step3', methods=['GET', 'POST'])
def step3():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TextArr[0] = post_data.get('inputTxt')
        TextArr[1] = post_data.get('pValue')
        TextArr[2] = post_data.get('secKeys1')
        response_object['message'] = 'Text coded!'
    else:
        step_4_txt = step_3(TextArr[0], TextArr[1], TextArr[2])
        response_object['stepTxt3'] = step_4_txt

    return jsonify(response_object)


@app.route('/shamir/step4', methods=['GET', 'POST'])
def step4():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TextArr[0] = post_data.get('inputTxt')
        TextArr[1] = post_data.get('pValue')
        TextArr[2] = post_data.get('secKeys2')
        response_object['message'] = 'Text coded!'
    else:
        answer_txt = step_4(TextArr[0], TextArr[1], TextArr[2])
        response_object['stepTxt4'] = answer_txt

    return jsonify(response_object)


#/////////////////////////////////Routes elGamal //////////////////////////////////////


@app.route('/elgamal/keygen', methods=['GET', 'POST'])
def key_generation_el():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        response_object['message'] = 'Text coded!'
    else:
        p, g, secKeyA, openKeyA, secKeyB, openKeyB = key_generation()
        response_object['pValue'] = p
        response_object['gValue'] = g
        response_object['secKeyA'] = secKeyA
        response_object['openKeyA'] = openKeyA
        response_object['secKeyB'] = secKeyB
        response_object['openKeyB'] = openKeyB
    return jsonify(response_object)


@app.route('/elgamal/send', methods=['GET', 'POST'])
def send_message_el():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TextArrEl.clear()
        TextArrEl.append(post_data.get('inputTxt'))
        TextArrEl.append(post_data.get('pValue'))
        TextArrEl.append(post_data.get('gValue'))
        TextArrEl.append(post_data.get('openKeyB'))
        response_object['message'] = 'Text coded!'
    else:
        sended_message, r_number = send_message(TextArrEl[0], TextArrEl[1],
                                                TextArrEl[2], TextArrEl[3])
        response_object['codeText'] = sended_message
        response_object['rNumbers'] = r_number
        print(sended_message, flush=True)
        print(r_number, flush=True)
    return jsonify(response_object)


@app.route('/elgamal/decode', methods=['GET', 'POST'])
def decode_message():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TextArrEl.clear()
        TextArrEl.append(post_data.get('inputTxt'))
        TextArrEl.append(post_data.get('rNumbers'))
        TextArrEl.append(post_data.get('secKeyB'))
        TextArrEl.append(post_data.get('pValue'))
        response_object['message'] = 'Text coded!'
    else:
        decoded_message = decode_message_el(TextArrEl[0], TextArrEl[1],
                                                     TextArrEl[2], TextArrEl[3])
        response_object['decodeText'] = decoded_message
    return jsonify(response_object)


#/////////////////////////////////Routes md5 //////////////////////////////////////


@app.route('/md5', methods=['GET', 'POST'])
def get_hash():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TextArrEl.clear()
        TextArrEl.append(post_data.get('inputTxt'))
        response_object['message'] = 'Text coded!'
    else:
        hash_text = getHash(TextArrEl[0])
        response_object['hashText'] = hash_text
    return jsonify(response_object)


#/////////////////////////////////Routes SHA1 //////////////////////////////////////


@app.route('/sha1', methods=['GET', 'POST'])
def get_hashSha():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TextArrEl.clear()
        TextArrEl.append(post_data.get('inputTxt'))
        response_object['message'] = 'Text coded!'
    else:
        hash_text = getHashSha(TextArrEl[0])
        response_object['hashText'] = hash_text
    return jsonify(response_object)


def inversion(a, b):
    a = int(a)
    b = int(b)
    U = [a, 1, 0]
    V = [b, 0, 1]
    T = [0, 0, 0]
    while V[0] != 0:
        q = U[0] // V[0]

        T[0] = U[0] % V[0]
        T[1] = U[1] - (q * V[1])
        T[2] = U[2] - (q * V[2])

        U = V
        V = [T[0], T[1], T[2]]
    if U[1] < 0:
        U[1] = U[1] + b

    return U[1]


def modul(a, x, p):
    a = int(a)
    x = int(x)
    p = int(p)
    if x == 0:
        result = 1
    else:
        bin_x = bin(x)[2:]
        result = a
        for i in range(1, len(bin_x)):
            result = ((result * result) * pow(a, int(bin_x[i]))) % p

    return result


if __name__ == '__main__':
    app.run(debug=True)