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

  colony10 = res_json[0]
  sol = calculate_digital_colony(colony10, colony10["generations"])

  colony50 = res_json[1]
  sol2 = calculate_digital_colony(colony50, colony50["generations"])

  result = [sol, sol2]
  response = jsonify(result)
  response.headers['Content-Type'] = 'application/json'
  
  return response

def calculate_digital_colony(input, counter):
  count = 0
  overall10 = ""
  stringNow = input['colony']

  while count < counter:
    weight = sum(int(char) for char in stringNow)
    temp = ""

    for i in range(len(stringNow)-1):
      sliced = stringNow[i:i+2]
      res = pair_calculate(sliced, weight)
      temp = temp + sliced[0] + res

      if i == len(stringNow)-2:
        temp = temp + sliced[1]

    print(count)

    stringNow = temp

    if count == counter-1:
      overall10 = temp

    count += 1

  return str(sum(int(char) for char in overall10))


def pair_calculate(inputstr, total):
  first, second = inputstr[0], inputstr[1]
  diff = 0
  if int(first) >= int(second):
    diff = int(first) - int(second)
  else:
    diff = 10 - abs(int(first) - int(second))
  value = str(diff + total)
  return value[-1]