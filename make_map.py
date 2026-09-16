import sqlite3
import pandas as pd
import folium

# reconect to database and rerunning queries 
conn = sqlite3.connect("potholes.db")

ward_query = """
SELECT ward, AVG(response_days) as avg_days, COUNT(*) as total_requests
FROM closed_requests
WHERE ward IS NOT NULL
GROUP BY ward
ORDER BY avg_days DESC
"""
by_ward = pd.read_sql(ward_query, conn)
conn.close()


m = folium.Map(location=[41.8781, -87.6298], zoom_start=10,tiles=None)

# coloring each ward based on average day response time
folium.Choropleth(
    geo_data="chicago_wards.geojson",
    data=by_ward,
    columns=["ward", "avg_days"],
    key_on="feature.properties.ward",
    fill_color="YlOrRd", # color scale yellow to red 
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="Average Response Tome (days)",
).add_to(m)


# saving map as an HTML file
m.save("potholes_map.html")
print("Saved map to pothole_map.html")