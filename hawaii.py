import os

import pandas as pd
import folium
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///hawaii.sqlite')

def runQuery(sql: str):
    """
    Executes a SQL Query
    """
    result = engine.connect().execute(text(sql))
    return pd.DataFrame(result.fetchall(), columns=result.keys())


query = """
SELECT * FROM station;
"""
runQuery(query)

query = """
SELECT * FROM measurement;
"""
runQuery(query)


query_last_date_measurement = """
    SELECT MAX(date) FROM measurement
"""
runQuery(query_last_date_measurement)

query_prec_last12 = f"""
    select date, prcp from 
    measurement
    where date >= date(
        (
            {
                query_last_date_measurement
            }
        )
        ,
        '-12 month'
    )
"""
prec_last12M = runQuery(query_prec_last12)
prec_last12M.index = prec_last12M.date
prec_last12M.index = pd.to_datetime(prec_last12M.index)
prec_last12M.sort_index(inplace=True)
prec_last12M


ax = prec_last12M[['prcp']].plot(figsize=(30,5))
ax.set_xlabel("Date")
ax.set_ylabel("Precipitacion")
ax.set_title("Precipitation las 12 Months")

map = folium.Map(location=[21.311389, -157.796389], zoom_start = 7)
map