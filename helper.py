import json
import xmltodict

from collections import OrderedDict
from datetime import date, datetime, timedelta

def get_value(value, default):
  return int(value) if value else default

def get_wait_times(data):
  CALEXICO = '250302'
  OTAY = "250601"
  SY = "250401"
  SY_PEDWEST = "250407"
  TECATE = "250501"
  PORT_NUMBERS = [CALEXICO, SY, SY_PEDWEST, OTAY, TECATE]

  DEFAULT = "N/A"

  DELAY = "delay_minutes"
  NAME = "port_name"
  NUMBER = "port_number"
  PEDESTRIAN = "pedestrian_lanes"
  READY = "ready_lanes"
  SENTRI = "NEXUS_SENTRI_lanes"
  STANDARD = "standard_lanes"
  STATUS = "port_status"
  VEHICLE = "passenger_vehicle_lanes"

  data = json.loads(json.dumps(xmltodict.parse(data)))
  ports = data["border_wait_time"]["port"]

  wait_times = {
    "ports": [],
  }

  pedwest = ""

  for port in ports:
    if port[NUMBER] not in PORT_NUMBERS:
      continue

    if port[NUMBER] == SY_PEDWEST:
      pedwest = get_value(port[PEDESTRIAN][STANDARD][DELAY], DEFAULT)
      continue

    port = {
      "port_number": port[NUMBER],
      "name": port[NAME],
      "status": port[STATUS],
      "wait_times": {
        "vehicle": {
          "sentri": get_value(port[VEHICLE][SENTRI][DELAY], DEFAULT),
          "ready": get_value(port[VEHICLE][READY][DELAY], DEFAULT),
          "standard": get_value(port[VEHICLE][STANDARD][DELAY], DEFAULT),
        },
        "pedestrian": {
          "ready": get_value(port[PEDESTRIAN][READY][DELAY], DEFAULT),
          "standard": get_value(port[PEDESTRIAN][STANDARD][DELAY], DEFAULT),
          "pedwest": DEFAULT,
        },
      }
    }

    wait_times["ports"].append(port)

  for port in wait_times["ports"]:
    if port[NUMBER] == SY:
      port["wait_times"]["pedestrian"]["pedwest"] = pedwest

  return wait_times
