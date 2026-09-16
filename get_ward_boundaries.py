import requests

url = "https://data.cityofchicago.org/resource/p293-wvbd.geojson"

response = requests.get(url)

with open("chicago_wards.geojson", "wb") as f:
    f.write(response.content)

print("Saved ward boundries to chicago_wards.geojson")