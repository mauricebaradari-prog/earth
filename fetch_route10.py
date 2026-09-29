import urllib.request
import re
import sys

url = 'https://maps.app.goo.gl/c6fhhjSxrSDDaDv69'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req)
    final_url = resp.geturl()
    print("Final URL:", final_url)
except Exception as e:
    print("Error:", e)
