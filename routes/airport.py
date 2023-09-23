import json
import logging
from typing import Dict, List

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/airport', methods=['POST'])
def solve_airport():
  res_json = request.get_json()
  sol = solve_airport_final(res_json)
  return json.dumps(sol)


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
    timeElpased = 0
    
    for passenger in passengers:
      currentTime = passenger.askTimeToDeparture()
      timeElpased += 1
      if timeElpased < cut_off_time and timeElpased < currentTime:
        if not passengerList:
          passengerList.append(passenger)
        else:
          for currentPassenger in passengerList:
            if currentTime < currentPassenger.askTimeToDeparture():
              timeElpased += 1
              passengerList.insert(passengerList.index(currentPassenger), passenger)
              break

    return passengerList


def execute(id, prioritisation_function, passenger_data, cut_off_time):
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
  print("totalNumberOfRequests: " + str(totalNumberOfRequests))

  # Print sequence of sorted departure times
  print("Sequence of prioritised departure times:")
  prioritised_filtered_list = []

  for i in range(len(prioritised_and_filtered_passengers)):
    print(prioritised_and_filtered_passengers[i].departureTime, end=" ")
    prioritised_filtered_list.append(prioritised_and_filtered_passengers[i].departureTime)

  print("\n")

  return {
    "id": id,
    "sortedDepartureTimes": totalNumberOfRequests,
    "numberOfRequests": prioritised_filtered_list
  }