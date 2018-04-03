# Homework 1
# Jin Peng
# jjp2172

import requests

payload = {"date": "1996-06-10"}
r = requests.get("https://api.nasa.gov/planetary/apod?api_key=cfOaZGAuPEAEv430BClSMaaIGIyQ83rMAEGNsUR0", params=payload)
content = r.json()
print(content["url"])
