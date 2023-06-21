# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:22:26 2023

@author: Eva Cantin Larumbe, Adriana Chust Vendrell, Mikel Baraza Vidal
"""

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import os 




st.title("Air pollution")


#Map with air quality stations
st.header("Air Quality Stations")
st.write("There are ten Air Quality Stations in Valencia. However, five have been selected for this study. They are all widespread throughout the city. They can be seen in this map:")

m = folium.Map(location=[39.46978308235751, -0.37701884302171607], 
               zoom_start=13, tiles='cartodbpositron')

folium.Marker([39.456960, -0.376140], popup="Pista Silla", 
              tooltip="Pista Silla", icon=folium.Icon(color="red")).add_to(m)

folium.Marker([39.457840, -0.343440], popup="Avda. Francia", 
              tooltip="Avda. Francia", icon=folium.Icon(color="red")).add_to(m)

folium.Marker([39.4797037, -0.3364037], popup="Politecnico", 
              tooltip="Politecnico", icon=folium.Icon(color="red")).add_to(m)

folium.Marker([39.483229121883966, -0.4088682310697038], popup="Moli de Sol", 
              tooltip="Moli de Sol", icon=folium.Icon(color="red")).add_to(m)

folium.Marker([39.4806317, -0.3659541], popup="Viveros", 
              tooltip="Viveros", icon=folium.Icon(color="red")).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725, height=400)



#open the data
root_dir = os.getcwd()
print(root_dir)
root_dir = root_dir.replace('pages', 'data/calidad_aire_limpio.csv')
#data_path = os.path.join(root_dir, "data", "calidad_aire_limpio.csv")
data_path =  root_dir.replace("\\", "/")
print(data_path)


df = pd.read_csv(data_path, sep=";", encoding="UTF-8")
df3 = df
gases = ['PM10', 'NO', 'NO2', 'O3', 'SO2']
colors = ['blue', 'red', 'green', 'orange', 'purple']

st.header("Evolution of air pollution")
st.write("This line plot allows us to see the evolution of air pollution depending on the year(s), and Air Quality Station(s). Besides clicking on the legend, a specific gas can be selected to observe its pattern better.")

#Filters
year_option = sorted(df['Anyo'].unique().tolist()) 
year_option.append('All')
year = st.selectbox('Select a Year', year_option, 0) #select a year

station_option = df['Estacion'].unique().tolist()
station = st.multiselect('Select an Air Quality Station', station_option)

df = df[df.Estacion.isin(station)]

if year == 'All':
   df_year = df.groupby('Fecha')['PM10', 'NO', 'NO2', 'O3', 'SO2'].mean().reset_index()
   fig = px.line(df_year, x="Fecha", y=gases, color_discrete_sequence=colors,
                  labels={
                     "Fecha": "Date",
                     "value": "Value (µg/m3)",
                     "variable": "Gases"},
                  
                title='')
   fig.update_traces(mode="lines", hovertemplate=None)
   fig.update_layout(hovermode="x")
     #fig.update_xaxes(    dtick="M1",    tickformat="%b\n%Y")
   fig.update_xaxes(
   rangeslider_visible=True,
   rangeselector=dict(
          buttons=list([
              dict(count=1, label="1m", step="month", stepmode="backward"),
              dict(count=6, label="6m", step="month", stepmode="backward"),
              dict(count=1, label="1y", step="year", stepmode="backward"),
              dict(step="all")])))
    

   st.write(fig)
    
else:  
    df_year = df[df.Anyo == year]
    df_year = df_year.groupby('Fecha')['PM10', 'NO', 'NO2', 'O3', 'SO2'].mean().reset_index()
    fig = px.line(df_year, x="Fecha", y=gases, color_discrete_sequence=colors,
                  labels={
                     "Fecha": "Date",
                     "value": "Value (µg/m3)",
                     "variable": "Gases"},
                  
                title='')
    fig.update_traces(mode="lines", hovertemplate=None)
    fig.update_layout(hovermode="x")
      #fig.update_xaxes(    dtick="M1",    tickformat="%b\n%Y")
    fig.update_xaxes(
      rangeslider_visible=True,
      rangeselector=dict(
          buttons=list([
              dict(count=1, label="1m", step="month", stepmode="backward"),
              dict(count=6, label="6m", step="month", stepmode="backward"),
              dict(step="all")])))
    
    st.write(fig)


st.header('Air pollution in 2022')
st.write('As the data for 2023 has yet to be uploaded, and the prize was obtained in 2022, it is interesting to see if air pollution has been reduced regarding the previous year, 2021, and each Air Quality Station.')

#to obtain the values below
df1 = df3.groupby(['Estacion', 'Anyo'])['PM10', 'NO', 'NO2', 'O3', 'SO2', 'Fecha'].mean().reset_index()
df2022 = df1[df1.Anyo==2022].reset_index(drop=True)
df2021 = df1[df1.Anyo==2021].reset_index(drop=True)
#df2022.iloc[:, 2:].subtract(df2021.iloc[:, 2:])

station = st.selectbox('Select an Air Quality Station', station_option)

st.markdown("""<style>
            {background-color: #EEEEEE; 
             border: 2px solid #CCCCCC; 
             padding: 5% 5% 5% 10%; 
             border-radius: 5px;}
            </style>""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

if station == "Avda. Francia":
    col1.metric("PM10 (µg/m3)", "24.25", "11.05")
    col2.metric("NO (µg/m3)", "93.56", "0.44")
    col3.metric("NO2 (µg/m3)", "12.21", "-0.55")
    col4.metric("O3 (µg/m3)", "52.63", "-3.22")
    col5.metric("SO2 (µg/m3)", "3.52", "-0.36")
    
elif station == "Moli del Sol":
    col1.metric("PM10 (µg/m3)", "14.93", "-1.69")
    col2.metric("NO (µg/m3)", "4.21", "0.46")
    col3.metric("NO2 (µg/m3)", "16.58", "3.22")
    col4.metric("O3 (µg/m3)", "56.86", "3.49")
    col5.metric("SO2 (µg/m3)", "3.56", "0.08")
    
elif station == "Pista Silla":
    col1.metric("PM10 (µg/m3)", "17.97", "5.32")
    col2.metric("NO (µg/m3)", "8.31", "-2.17")
    col3.metric("NO2 (µg/m3)", "18.92", "-2.75")
    col4.metric("O3 (µg/m3)", "48.75", "-3.72")
    col5.metric("SO2 (µg/m3)", "3.39", "0.11")
    
elif station == "Politecnico":
    col1.metric("PM10 (µg/m3)", "15.09", "3.69")
    col2.metric("NO (µg/m3)", "3.47", "1.11")
    col3.metric("NO2 (µg/m3)", "12.06", "2.95")
    col4.metric("O3 (µg/m3)", "55.75", "-2.85")
    col5.metric("SO2 (µg/m3)", "3.37", "-0.19")
    
elif station == "Viveros":
    col1.metric("PM10 (µg/m3)", "23.67", "4.06")
    col2.metric("NO (µg/m3)", "4.34", "-0.61")
    col3.metric("NO2 (µg/m3)", "15.98", "-1.79")
    col4.metric("O3 (µg/m3)", "50.63", "-8.35")
    col5.metric("SO2 (µg/m3)", "3.60", "0.27")
