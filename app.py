import pandas as pd
from datetime import datetime
import streamlit as st

if st.button("Check Stations For Most Recent Data"):
    station_list = pd.read_csv('station_list.csv')
    station_list["ts_id"] = station_list["ts_id"].astype("Int64")

    today = datetime.today().strftime('%Y-%m-%d')
    three_months_ago = (datetime.today() - pd.DateOffset(months=3)).strftime('%Y-%m-%d')

    most_recent_dates_list = []

    for ts_id in station_list['ts_id']:
        url_csv = (
            f"http://waterdata.capitolregionwd.org/KiWIS/KiWIS?"
            f"service=kisters&type=queryServices&request=getTimeseriesValues&"
            f"datasource=0&format=csv&ts_id={ts_id}&from={three_months_ago}&to={today}"
        )
        try:
            df = pd.read_csv(url_csv, sep=';', skiprows=2, header=0)
            df.rename(columns={'#Timestamp': 'Date'}, inplace=True)
            most_recent_date = df["Date"].max()
            station_name = station_list[station_list["ts_id"] == ts_id]["station_name"].iloc[0]
        except:
            print(f"Error reading CSV for ts_id: {ts_id}")
            continue
        most_recent_dates_list.append({"Station Name": station_name, "Date": most_recent_date})
    most_recent_dates_df = pd.DataFrame(most_recent_dates_list)
    most_recent_dates_df["Date"] = pd.to_datetime(most_recent_dates_df["Date"]).dt.tz_convert(None)
    
    st.dataframe(most_recent_dates_df, height=1000)
