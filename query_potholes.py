import sqlite3
import pandas as pd 

conn = sqlite3.connect("potholes.db")

# trying to answer what ward takes the longest to respond. 
# SELECT ward -> calcualte the average reponse time per ward 
#                and how many requests are in each group.
# FROM closed requests -> only look at potholes that were actually closed 
# WHERE ward is NOT NULL -> -> skups rows where ward was not enterered 
# GROUP -> group by ward 
# ORDEY BY avg_days DESC -> sort by slowest ward first.

ward_query = """
SELECT ward, AVG(response_days) as avg_days, COUNT(*) as total_requests
FROM closed_requests
WHERE ward IS NOT NULL
GROUP BY ward
ORDER BY avg_days DESC
"""

# finding how many potholes are still open by zip code 
zip_query = """
SELECT zip_code, COUNT(*) as open_count
FROM open_requests
WHERE zip_code IS NOT NULL
GROUP BY zip_code
ORDER BY open_count DESC
"""

# send questions to data base to find answer
by_ward = pd.read_sql(ward_query, conn)
open_by_zip = pd.read_sql(zip_query, conn)

print("\nWard reponse time: ")
print(by_ward)

print("\nOpen (unfixed) potholes by zip code: ")
print(open_by_zip)