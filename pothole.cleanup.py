import pandas as pd 

# laoding the downloaded csv file
df = pd.read_csv("potholes_raw.csv")


# turning created data and closed data strings into 
# objects to subtract and find time finished.
df["created_date"] = pd.to_datetime(df["created_date"], errors = "coerce")
df["closed_date"] = pd.to_datetime(df["closed_date"], errors = "coerce")

#filtering the blank closed dates rows 
still_open = df[df["closed_date"].isna()].copy()
closed = df[df["closed_date"].notna()].copy()

print(f"Total Requests: {len(df)}")
print(f"Still open (no closed date): {len(still_open)}")
print(f"Requests closed: {len(closed)}")

# calculating how many days it took to close the pot hole request 
closed["response_days"] = (closed["closed_date"] - closed["created_date"]).dt.days

#checking if any rows have typos.
error_rows = closed[closed["response_days"] < 0]
print(f"Rows with negative response time: {len(error_rows)}")

closed = closed[closed["response_days"] >= 0]

#short summary 
print("\nResponse time summary (in days: )")
print(closed["response_days"].describe())

#saving cleaned files 
closed.to_csv("potholes_closed_cleaned.csv", index=False)
still_open.to_csv("potholes_open_cleaned.csv", index=False)

print("\nSaved potholes_closed_cleaned.csv and potholes_open_cleaned.csv")








