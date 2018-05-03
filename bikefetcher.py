#!/usr/bin/python

import requests
import json
import svgwrite

def count_to_color(count):
  if count == 0:
    return "rgb(255,0,0)"
  elif count > 9:
    return "rgb(0,255,0)"
  else:
    red = (255 - 2*count)
    green = 255
    if count <= 4:
      green = 255 - (4-count)*60

    return "rgb(" + str(red) + "," + str(green) + ",0)"


def main():

  try:
    query='''
{
  bikeRentalStation(id:"059") { 
    bikesAvailable
  }
}    
'''
    data = {'query': query, 'variables': None}
    result = requests.post("https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql/", data=json.dumps(data), headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

  except:
    print "Content-Type: text/plain;charset=utf-8"
    print
    print "Request failed for reasons"

  if result.status_code != 200:
    #Check status code
    print "Content-Type: text/plain;charset=utf-8"
    print
    print "Error: Status Code " + str(result.status_code)

  else:
    data = json.loads(result.content)
    salmisaari = data['data']['bikeRentalStation'] #filter(lambda x: x["name"] == "Salmisaarenranta", stations)
    if salmisaari:
      count = salmisaari["bikesAvailable"]
      
      color = count_to_color(count)
      dwg = svgwrite.Drawing("", (100, 100), debug=True)
      dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=color))
      paragraph = dwg.add(dwg.g(font_size=24))
      paragraph.add(dwg.text(count, (30, 30)))

      print "Content-Type: image/svg+xml;charset=utf-8"
      print
      print dwg.tostring()
    else:
      print "Content-Type: text/plain;charset=utf-8"
      print
      print "Error: Salmisaarenranta not found"
  

main()
