import pandas as pd 

# laoding the downloaded csv file
df = pd.read_csv("potholes_raw.csv")


# turning creadted data and closed data strings into 
# objects to subtracte and find time finished.
df["created_date"] = pd.to_datetime(df["created_date"], errors = "coerce")
df["closed_date"] = pd.to_datetime(df["closed_date"], errors = "coerce")



