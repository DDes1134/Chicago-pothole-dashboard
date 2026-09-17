import streamlit as st 
import sqlite3
import pandas as pd 

# make width of the screen + give Title 
st.set_page_config(page_title="2026 Chicago Pothole Dashboard", layout="wide")


#big heading 
st.title("2026 Chicago Pothole Response Dashboard")
st.write("Tracking how long the City of Chicago takes to fix reported potholes in 2026. ")

#reconnecting to data base
conn = sqlite3.connect("potholes.db")

ward_query = """
SELECT ward, AVG(response_days) as avg_days, COUNT(*) as total_requests
FROM closed_requests
WHERE ward IS NOT NULL
GROUP BY ward
ORDER BY avg_days DESC
"""
by_ward = pd.read_sql(ward_query, conn)
conn.close

#subheader
st.subheader("Average Pothole Repair Time by Ward")

st.dataframe(by_ward)
