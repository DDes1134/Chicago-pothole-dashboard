import sqlite3
import pandas as pd 

#load cleaned csvs
closed = pd.read_csv("potholes_closed_cleaned.csv")
still_open = pd.read_csv("potholes_open_cleaned.csv")

#connecting 
conn = sqlite3.connect("potholes.db")

closed.to_sql("closed_requests", conn, if_exists="replace", index = False)
still_open.to_sql("open_requests", conn, if_exists="replace", index=False)


conn.close()

print("Saved data into potholes.db (tables: closed_requests, open_requests)")
