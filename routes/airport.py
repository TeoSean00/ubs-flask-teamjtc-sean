import json
import logging
from typing import Dict, List

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)


@app.route('/airport', methods=['POST'])
def solve_airport():
  res_json = request.get_json()
  sol = solve_airport_final(res_json)
  response = jsonify(sol)
  response.headers['Content-Type'] = 'application/json'
  
  return response


# Simple passenger class
class Passenger:
  def __init__(self, departureTime):
    self.departureTime = departureTime
    self.numberOfRequests = 0

  def askTimeToDeparture(self):
    self.numberOfRequests += 1
    return self.departureTime

  def getNumberOfRequests(self):
    return self.numberOfRequests
  

def solve_airport_final(in_str_ls: List[str]) -> List[str]:
  result = []

  for strList in in_str_ls:
    id = strList['id']
    timeList = strList['departureTimes']
    cutOff = strList['cutOffTime']
    res = execute(id, prioritisation_function, timeList, cutOff)
    result.append(res)

  return result


def prioritisation_function(passengers, cut_off_time):
    # return sorted array of passenger instances
    passengerList = []
    
    for passenger in passengers:
      currentTime = passenger.askTimeToDeparture()
      if currentTime >= cut_off_time:
        if len(passengerList) == 0:
          passengerList.append(passenger)
        else:
          if currentTime >= passengerList[-1].askTimeToDeparture():
            passengerList.append(passenger)
          else:
            inserted = False

            for idx, currentPassenger in enumerate(passengerList):
              if not inserted:
                if currentTime < currentPassenger.askTimeToDeparture():
                  passengerList.insert(passengerList.index(currentPassenger), passenger)
                  inserted = True

            if not inserted:
              passengerList.append(passenger)
                
    return passengerList


def execute(id, prioritisation_function, passenger_data, cut_off_time):
  print('id', id)
  print('cut_off_time', cut_off_time)
  print('passengerdata', passenger_data)

  totalNumberOfRequests = 0
  passengers = []

  # Initialise list of passenger instances
  for i in range(len(passenger_data)):
    passengers.append(Passenger(passenger_data[i]))

  # Apply solution and re-shuffle with departure cut-off time
  prioritised_and_filtered_passengers = prioritisation_function(passengers, cut_off_time)

  # Sum totalNumberOfRequests across all passengers
  for i in range(len(passengers)):
    totalNumberOfRequests += passengers[i].getNumberOfRequests()

  # Print sequence of sorted departure times
  prioritised_filtered_list = []

  for i in range(len(prioritised_and_filtered_passengers)):
    prioritised_filtered_list.append(prioritised_and_filtered_passengers[i].departureTime)
  
  print('prioritised_filtered_list', prioritised_filtered_list)

  return {
    "id": id,
    "sortedDepartureTimes": prioritised_filtered_list,
    "numberOfRequests": totalNumberOfRequests
  }