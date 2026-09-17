import pandas as pd 
import sqlite3 
import plotly.express as px 

# reconnecting and rerunning query 
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

#putting ward numbrs as categories to find boundries 
by_ward["ward"] = by_ward["ward"].astype(str)

#making bar chart from dataframe 
fig = px.bar(
    by_ward,
    x = "ward",
    y = "avg_days",
    color = "avg_days",
    color_continuous_scale = "YlOrRd",
    labels = {"ward": "Ward", "avg_days": "Average Response Time (Days)"},
    title = "Average Pothole Repair Time by Ward (2026)"
)

# keeping slowest to fastest ward sorting from SQL query,
# (chart order)
fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray':by_ward["ward"]})

fig.write_html("potholes_chart.html")
print("Saved chart to pothole_chart.html")