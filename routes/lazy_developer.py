import json
import logging
from typing import Dict, List

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/lazy-developer', methods=['POST'])
def evaluate_lazy_developer():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    # input_value = data.get("input")
    # result = input_value * input_value
    classes: List[Dict] = data.get("classes")
    statements: List[Dict] = data.get("statements")

    res: Dict[str, List[str]] = getNextProbableWords(classes=classes, statements=statements)

    logging.info("My result :{}".format(res))
    return json.dumps(res)


def getNextProbableWords(classes: List[Dict],
                         statements: List[str]) -> Dict[str, List[str]]:
  # Fill in your solution here and return the correct output based on the given input
  emptyString = set()
  normalClass = {}
  polymorphicType = set()
  enumType = {}
  keys = []
  result = {}

  # categorizing all keys in classes to their specific category
  for json in classes:
    key = list(json.keys())[0]
    value = json[key]
    # populating list of keys in classes
    keys.append(key)
    # categorize by type
    # emptyString
    if value == "":
      emptyString.add(key)
    # class
    elif isinstance(value, dict):
      normalClass[key] = value

  for json in classes:
    key = list(json.keys())[0]
    value = json[key]
    # polymorphic or enum type
    if isinstance(value, list):
      polymorphicCheck = True
      for substring in value:
        if substring not in keys:
          polymorphicCheck = False
          break
      # polymorphic
      if polymorphicCheck:
        polymorphicType.add(key)
      # enum
      else:
        enumType[key] = value
  
  # populating result dictionary
  for statement in statements:
    # 2 main cases, ends with '.' or does not end with '.'
    if statement.endswith("."):
      word = statement[:-1]
      # single word case
      if "." not in word:
        if word in emptyString or word in polymorphicType:
          result[statement] = [""]
        elif word in normalClass:
          value = list(normalClass[word].keys())
          sortedValue = sorted(value, key=lambda x: x)[:5]
          result[statement] = sortedValue
        elif word in enumType:
          value = enumType[word]
          sortedValue = sorted(value, key=lambda x: x)[:5]
          result[statement] = sortedValue
      # nested words case
      else:
        words = word.split(".")
        # emptystring or polymorphic type
        if words[0] in emptyString or words[0] in polymorphicType:
          result[statement] = [""]
        # normalclass type
        elif words[0] in normalClass:
          values = list(normalClass[words[0]].keys())
          exactMatch = False
          for value in values:
            if value == words[1]:
              exactMatch = True
              break
          # 2 cases here, if there's an exactMatch else return the most probable words instead
          if exactMatch:
            type = normalClass[words[0]][words[1]]
            if "<" in type:
              startIndex = type.index("<")
              endIndex = type.index(">")
              type = type[startIndex+1:endIndex]
            # After applying the necessary conversion to type, we look for type, type cant be found in normalClass too
            if type in emptyString or type in polymorphicType:
              result[statement] = [""]
            elif type in enumType:
              value = enumType[type]
              sortedValue = sorted(value, key=lambda x: x)[:5]
              result[statement] = sortedValue
          # if no exactMatch, return most probable words instead
          else:
            temp = []
            for value in values:
              if value.startswith(words[1]):
                temp.append(value)
            sortedValue = sorted(temp, key=lambda x: x)[:5]
            result[statement] = sortedValue
        # enum type
        elif words[0] in enumType:
          values = enumType[words[0]]
          temp = []
          for value in values:
            if value.startswith(words[1]):
              temp.append(value)
          sortedTemp = sorted(temp, key=lambda x: x)[:5]
          result[statement] = sortedTemp
          
    # other main case, where statement does not end with "."
    else:
      words = statement.split(".")
      # case where only 1 word
      if len(words) == 1:
        word = words[0]
        # emptystring or polymorphic type
        if word in emptyString or word in polymorphicType:
          result[statement] = [""]
        # normalclass type
        elif word in normalClass:
          value = list(normalClass[word].keys())
          sortedValue = sorted(value, key=lambda x: x)[:5]
          result[statement] = sortedValue
        # enumtype
        elif word in enumType:
          value = enumType[word]
          sortedValue = sorted(value, key=lambda x: x)[:5]
          result[statement] = sortedValue
      # case with multiple words
      else:
        # emptystring or polymorphic type
        if words[0] in emptyString or words[0] in polymorphicType:
          result[statement] = [""]
        # normalclass type
        elif words[0] in normalClass:
          values = list(normalClass[words[0]].keys())
          exactMatch = False
          for value in values:
            if value == words[1]:
              exactMatch = True
              break
          # 2 cases here, if there's an exactMatch else return the most probable words instead
          if exactMatch:
            type = normalClass[words[0]][words[1]]
            if "<" in type:
              startIndex = type.index("<")
              endIndex = type.index(">")
              type = type[startIndex+1:endIndex]
            # After applying the necessary slicing to type if needed
            if type in emptyString or type in polymorphicType:
              result[statement] = [""]
            elif type in enumType:
              value = enumType[type]
              sortedValue = sorted(value, key=lambda x: x)[:5]
              result[statement] = sortedValue
          # if no exactMatch, return most probable words instead
          else:
            temp = []
            for value in values:
              if value.startswith(words[1]):
                temp.append(value)
            sortedValue = sorted(temp, key=lambda x: x)[:5]
            result[statement] = sortedValue
        # enum type
        elif words[0] in enumType:
          values = enumType[words[0]]
          temp = []
          for value in values:
            if value.startswith(words[1]):
              temp.append(value)
          sortedTemp = sorted(temp, key=lambda x: x)[:5]
          result[statement] = sortedTemp

  return result