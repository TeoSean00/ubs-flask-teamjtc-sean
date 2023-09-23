import json
import logging
from typing import Dict, List

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

@app.route('/calendar-scheduling', methods=['POST'])
def calendar_solve():
  res_json = request.get_json()
  res_json.sort(key=lambda x: x["potentialEarnings"], reverse=True)
  sol = calculate_calendar(res_json)

  response = jsonify(sol)
  response.headers['Content-Type'] = 'application/json'
  
  print(response)
  return response

def calculate_calendar(lesson_requests: List[str]) -> List[str]:
  # Create a table to store the maximum earnings for each day
  dp_table = {day: 0 for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}

  # Create a table to track the selected lesson requests
  selected_lessons = {day: [] for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}

  # Iterate through lesson requests and populate the DP table
  for request in lesson_requests:
      duration = request["duration"]
      available_days = request["availableDays"]

      for day in available_days:
          if duration <= 12 - dp_table[day]:
              dp_table[day] += duration
              selected_lessons[day].append(request["lessonRequestId"])

  return selected_lessons