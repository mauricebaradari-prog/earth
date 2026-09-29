import requests
import json

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
way
  ["highway"]
  ["name"="B6"]
  (34.660, 32.628, 34.685, 32.700);
out geom;
"""

response = requests.post(overpass_url, data={'data': overpass_query})
data = response.json()

coords = []
for el in data['elements']:
    if el['type'] == 'way':
        for node in el['geometry']:
            coords.append([node['lon'], node['lat']])

print(len(coords))
with open('b6_coords.json', 'w') as f:
    json.dump(coords, f)
