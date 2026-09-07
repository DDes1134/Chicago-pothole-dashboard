import requests 
import pandas as pd 

#Pull url 
url = "https://data.cityofchicago.org/resource/v6vf-nfxy.json" 

# parameters for needed columns onlys 
params = {
    "$select": "sr_number,sr_type,created_date,closed_date,"
    "street_address,zip_code,ward,latitude,longitude",
    "$where": "sr_type = 'Pothole in Street Complaint' AND created_date >= '2026-01T00:00'",
    "$limit": 52000
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data)

print(f"Downloaded {len(df)} pothole requests")

df.to_csv("potholes_raw.csv", index=False)
print("Saved to potholes_raw.csv")