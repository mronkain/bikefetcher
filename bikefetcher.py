#!/usr/bin/python

import requests
import json
import svgwrite

def main():

  try:
    result = requests.get("http://api.citybik.es/v2/networks/citybikes-helsinki")
  except:
    print "Error retrieving URL with requests package"

    #Check status code
  if result.status_code != 200:
    print "Error: Status Code " + str(result.status_code)

  else:
    data = json.loads(result.content)
    stations = data["network"]["stations"]
    salmisaari = filter(lambda x: x["name"] == "Salmisaarenranta", stations)
    count = salmisaari[0]["free_bikes"]
    color = "red"
    if count > 3:
      color = "green"
    elif count > 0:
      color = "yellow"

    dwg = svgwrite.Drawing("", (100, 100), debug=True)
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=color))
    paragraph = dwg.add(dwg.g(font_size=24))
    paragraph.add(dwg.text(count, (30, 30)))

    print "Content-Type: image/svg+xml;charset=utf-8"
    print
    print dwg.tostring()


main()