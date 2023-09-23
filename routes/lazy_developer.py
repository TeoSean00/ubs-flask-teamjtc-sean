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


def getNextProbableWords(classes: List[Dict], statements: List[str]) -> Dict[str, List[str]]:
  # Fill in your solution here and return the correct output based on the given input
  MAX_NUM_RETURNS: int = 5
    
  class_dict = {}  # Dictionary to store class definitions
  enum_dict = {}   # Dictionary to store enum definitions
  result = {}      # Dictionary to store the final output
  polymorphic_classes = set() # List to store classes with polymorphic types
  none_classes = set() # List to store classes with none types
  
  class_names = [] # List to store class names
  for subclass in classes:
      class_names.append(list(subclass.keys())[0])
  
  # Process class and enum definitions
  for class_info in classes:
      key = next(iter(class_info))
      value = class_info[key]

      if value == '':
          none_classes.add(key)
      elif isinstance(value, list):  # Enum
          if any(class_name in value for class_name in class_names):
              polymorphic_classes.add(key)
          else:
              enum_dict[key] = value
      elif isinstance(value, dict):  # Class
          class_dict[key] = list(value.keys())
  
  # Process interior types
  for class_info in classes:
      key = next(iter(class_info))
      value = class_info[key]

      if isinstance(value, dict):  # Class
          for v_key, v_value in value.items():
              if any(polymorphic_class_string in v_value for polymorphic_class_string in polymorphic_classes):
                  polymorphic_classes.add(f"{key}.{v_key}")
  
  # Process statements
  for statement in statements:
      if statement.endswith('.'):
          prefix = statement[:-1]

          if prefix in polymorphic_classes or prefix in none_classes:
              result[statement] = [""]
              continue
          elif prefix in class_dict:
              # matches = [key for key in class_dict if key.startswith(prefix)]
              matches = class_dict[prefix]
          elif prefix in enum_dict:
              # matches = [key for key in enum_dict if key.startswith(prefix)]
              matches = enum_dict[prefix]

          probable_words = [word for word in matches]
          probable_words.sort()
          result[statement] = probable_words[:MAX_NUM_RETURNS]
      else:
          if statement in polymorphic_classes or statement in none_classes:
              result[statement] = [""]
              continue

          class_name, attribute = statement.split('.')

          if class_name in class_dict:
              probable_words = [word for word in class_dict[class_name] if word.startswith(attribute)]
              probable_words.sort()
              result[statement] = probable_words[:MAX_NUM_RETURNS]
          elif class_name in enum_dict:
              probable_words = [word for word in enum_dict[class_name] if word.startswith(attribute)]
              probable_words.sort()
              result[statement] = probable_words[:MAX_NUM_RETURNS]
  
  return result