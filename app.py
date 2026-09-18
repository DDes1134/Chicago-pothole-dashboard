import streamlit as st 
import sqlite3
import pandas as pd 
import plotly.express as px 
import folium
from streamlit_folium import st_folium

# make width of the screen + give Title 
st.set_page_config(page_title="Live 2026 Chicago Pothole Dashboard", layout="wide")


#big heading 
st.title("2026 Chicago Pothole Response Dashboard")
st.write("Live Tracking on how long the City of Chicago takes to fix reported potholes in 2026. ")

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

# Sorted list of wards for the dropdown, plus an "All Wards" option
ward_options = ["All Wards"] + sorted(by_ward["ward"].unique().tolist())
selected_ward = st.selectbox("Select a ward to highlight:", ward_options)

# If they picked a specific ward (not "All Wards"), filter the table
# down to just that one row so they can see its exact numbers.
if selected_ward != "All Wards":
    filtered = by_ward[by_ward["ward"] == selected_ward]
    st.write(f"Ward {selected_ward}: average {filtered['avg_days'].values[0]:.1f} days, "
             f"{filtered['total_requests'].values[0]} total requests")

st.subheader("Map: Average Response Time By Ward")

# pulling the CartoDB key out of secrets.toml instead of hardcoding it,
# so the key itself never ends up visible in this file or on GitHub
CARTO_API_KEY = st.secrets["CARTO_API_KEY"]

# adding folium map
m = folium.Map(
    location=[41.8781, -87.6298],
    zoom_start=10,
    tiles=f"https://basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}.png?key={CARTO_API_KEY}",
    attr="CartoDB"
)

folium.Choropleth(
    geo_data="chicago_wards.geojson",
    data=by_ward,
    columns=["ward", "avg_days"],
    key_on="feature.properties.ward",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="Average Response Time (days)"
).add_to(m)

# This adds an invisible layer on top of your colored wards, 
# Choropleth alone doesn't support this, so did it separately.
folium.GeoJson(
    "chicago_wards.geojson",
    style_function=lambda x: {"fillColor": "transparent", "color": "transparent", "weight": 0},
    tooltip=folium.GeoJsonTooltip(fields=["ward"], aliases=["Ward:"])
).add_to(m)

# brige function to allow folium to opearate in streamlit 
st_folium(m, width=1200, height=600)

#subheader
st.subheader("Average Pothole Repair Time by Ward")

st.dataframe(by_ward)

#importing plotly 
by_ward_chart = by_ward.copy()
by_ward_chart["ward"] = by_ward_chart["ward"].astype(str)

fig = px.bar(
    by_ward_chart,
    x="ward",
    y="avg_days",
    color="avg_days",
    color_continuous_scale="YlOrRd",
    labels={"ward": "Ward", "avg_days": "Average Response Time (Days)"},
    title="Average Pothole Repair Time by Ward (2026)"
)
fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': by_ward["ward"]})

st.subheader("Ranked: Slowest to Fastest Wards")

# adding plotly figure 
st.plotly_chart(fig, use_container_width=True)