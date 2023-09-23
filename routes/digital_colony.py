import json
import logging
from typing import Dict, List
import copy

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)
@app.route('/digital-colony', methods=['POST'])
def solve_digital_colony():
  res_json = request.get_json()
  sol = calculate_digital_colony(res_json)

  response = jsonify(sol)
  response.headers['Content-Type'] = 'application/json'
  
  return response

def calculate_digital_colony(input: List[str]) -> List[str]:
  colony10 = input[0]
  colony50 = input[1]
  count = 0
  overall = ""
  stringNow = colony10['colony']

  while count < 10:
    currentWeight10 = sum(int(char) for char in stringNow)
    temp = ""

    for i in range(len(stringNow)-1):
      sliced = stringNow[i:i+2]
      res = pair_calculate(sliced, currentWeight10)
      temp = temp + sliced[0] + res

      if i == len(stringNow)-2:
        temp = temp + sliced[1]

    # if count <= 4:
    #   print('count', count)
    #   print('stringNow:', stringNow)
    #   print('currentWeight10:', currentWeight10)
    #   print('temp:', temp)

    stringNow = temp

    if count == 9:
      overall = temp
      break

    count += 1

  return [str(sum(int(char) for char in overall)), "123"]

def pair_calculate(inputstr, total):
  first, second = inputstr[0], inputstr[1]
  diff = 0
  if int(first) >= int(second):
    diff = int(first) - int(second)
  else:
    diff = 10 - abs(int(first) - int(second))
  value = str(diff + total)
  return value[-1]