# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 12:35:51 2023

@author: Eva Cantin Larumbe, Adriana Chust Vendrell, Mikel Baraza Vidal
"""

import folium
import json
import pandas as pd
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
from shapely.geometry import Point, Polygon
import numpy as np
import os

# CODE
#------------------------------------------------------------------------------------------------------------------------
root_dir = os.getcwd()
root_dir = root_dir.replace('pages', 'data/distritos.json')
data_path =  root_dir.replace("\\", "/")

with open(data_path) as f:
    data = json.load(f)  # cargamos los datos
    
#SELECT BOXES
#------------------------------------------------------------------------------------------------------------------------
valencia_coords = [39.4699, -0.3763]  # primera vista general
distrito_names = []  # nombres de todos los distritos
for feature in data['features']:
    distrito_names.append(feature['properties']['name']) #Añadimos cada uno de los nombres de los distritos a la lista.
public_transports = ["Bus", "Subway", "Valenbisi"] #los tipos de transporte 

# Configurar la página de la aplicación
st.title("Navigating Valencia:")  # título
st.header("A Guide to Public Transport")
transporte_seleccionado = st.selectbox("Select a type of means of transport:", public_transports) #box transporte

distrito_names.insert(0, "All")  #La primera opción será "Todos" para ver todos los distritos
distrito_seleccionado = st.selectbox("Select a district:", distrito_names) #box distrito

# FILTRADO DE DATOS Y POLÍGONOS DE LOS DISTRITOS
if distrito_seleccionado == "All":
    filtered_data = data
    valencia_map = folium.Map(location=valencia_coords, zoom_start=11) # un mapa mucho más grande y de toda Valencia
else:
    filtered_data = {
        "type": "FeatureCollection",
        "features": [
            feature for feature in data['features']
            if feature['properties']['name'] == distrito_seleccionado
        ]
    }
    district_coordinates = filtered_data['features'][0]['geometry']['coordinates'][0]
    district_coords = [[coord[1], coord[0]] for coord in district_coordinates]
    district_center = [
       np.mean([coord[0] for coord in district_coords]),
       np.mean([coord[1] for coord in district_coords])
   ]   #obtenemos las coordenadas mas centradas dentro del poligono para generar el mapa de nuevo
    valencia_map = folium.Map(location=district_center, zoom_start=14) #creamos el mapa pero con un zoom mas grande ya que ahora nos centramos en un distrito
# Agregar los polígonos de los distritos al mapa

for feature in filtered_data['features']:
    coordinates = [[coord[1], coord[0]] for coord in feature['geometry']['coordinates'][0]]
    district_polygon = folium.vector_layers.Polygon(
        locations=coordinates,
        color='green',
        fill_color='green',
        fill_opacity=0.1,
        weight=0.8
    )
    district_polygon.add_to(valencia_map) #dibujo de los polígonos, en cada caso

    if distrito_seleccionado == "All":
           district_name = feature['properties']['name']
           district_popup = folium.Popup(district_name, max_width=200)
           district_polygon.add_child(district_popup)  # Agregar etiqueta emergente al polígono

#SELECCION DE TRANSPORTES 

marker_cluster = MarkerCluster() #para hacer los clusters

#-----------------------------------------------BUS----------------------------------------------------------------------

root_dir = os.getcwd()
root_dir = root_dir.replace('pages', 'data/emt_con_distritos.csv')
data_path =  root_dir.replace("\\", "/")

emt_data = pd.read_csv(data_path)

# Filtrar las paradas de autobús del distrito seleccionado
if transporte_seleccionado == "Bus" and distrito_seleccionado != "All":
    bus_stops = emt_data[emt_data['distritos'] == distrito_seleccionado] #solo las paradas dentro de ese distrito
    
    for index, row in bus_stops.iterrows():
        stop_lat = row['geo_point_2d'].split(',')[0]  # Obtener la latitud de la parada
        stop_lon = row['geo_point_2d'].split(',')[1]  # Obtener la longitud de la parada
        stop_name = row['Denominació / Denominación']  # Obtener el nombre de la parada
        
        folium.Marker(
            location=[float(stop_lat), float(stop_lon)],
            popup=stop_name,
            icon=folium.Icon(color='red', icon='bus', prefix='fa')
        ).add_to(valencia_map)  #meter los iconos
        
elif transporte_seleccionado == "Bus" and distrito_seleccionado == "All":
    bus_stops = emt_data #todas
    for index, row in bus_stops.iterrows():
        stop_lat = row['geo_point_2d'].split(',')[0]  # Obtener la latitud de la parada
        stop_lon = row['geo_point_2d'].split(',')[1]  # Obtener la longitud de la parada
        stop_name = row['Denominació / Denominación']  # Obtener el nombre de la parada
        
        folium.Marker(
            location=[float(stop_lat), float(stop_lon)],
            popup=stop_name,
            icon=folium.Icon(color='red', icon='bus', prefix='fa')
        ).add_to(marker_cluster)


    valencia_map.add_child(marker_cluster) #Añadimos al mapa los clusters



#-----------------------------------------------SUBWAY-------------------------------------------------------------------

subway_data = pd.read_csv('../data/subway_con_distritos.csv')


if transporte_seleccionado == "Subway" and distrito_seleccionado != "All":
    subway_stops = subway_data[subway_data['distritos'] == distrito_seleccionado]
    for index, row in subway_stops.iterrows():
        stop_lat = row['geo_point_2d'].split(',')[0]  # Obtener la latitud de la parada
        stop_lon = row['geo_point_2d'].split(',')[1]  # Obtener la longitud de la parada
        stop_name = row['Denominació / Denominación']  # Obtener el nombre de la parada
        
        folium.Marker(
            location=[float(stop_lat), float(stop_lon)],
            popup=stop_name,
            icon=folium.Icon(color='blue', icon='subway', prefix='fa')
        ).add_to(valencia_map)
        
elif transporte_seleccionado == "Subway" and distrito_seleccionado == "All":
    subway_stops = subway_data
    for index, row in subway_stops.iterrows():
        stop_lat = row['geo_point_2d'].split(',')[0]  # Obtener la latitud de la parada
        stop_lon = row['geo_point_2d'].split(',')[1]  # Obtener la longitud de la parada
        stop_name = row['Denominació / Denominación']  # Obtener el nombre de la parada
        
        folium.Marker(
            location=[float(stop_lat), float(stop_lon)],
            popup=stop_name,
            icon=folium.Icon(color='blue', icon='subway', prefix='fa')
        ).add_to(marker_cluster)


    valencia_map.add_child(marker_cluster) #Añadimos al mapa los clusters


#-----------------------------------------------VALENBISI----------------------------------------------------------------

bike_data = pd.read_csv('../data/bikes_con_distritos.csv')


if transporte_seleccionado == "Valenbisi" and distrito_seleccionado != "All":
    bike_stops = bike_data[bike_data['distritos'] == distrito_seleccionado]
    for index, row in bike_stops.iterrows():
        stop_lat = row['geo_point_2d'].split(',')[0]  # Obtener la latitud de la parada
        stop_lon = row['geo_point_2d'].split(',')[1]  # Obtener la longitud de la parada
        stop_name = row['Direccion']  # Obtener el nombre de la parada
        
        folium.Marker(
            location=[float(stop_lat), float(stop_lon)],
            popup=stop_name,
            icon=folium.Icon(color='green', icon='bicycle', prefix='fa')
        ).add_to(valencia_map)
        
elif transporte_seleccionado == "Valenbisi" and distrito_seleccionado == "All":
    bike_stops = bike_data
    for index, row in bike_stops.iterrows():
        stop_lat = row['geo_point_2d'].split(',')[0]  # Obtener la latitud de la parada
        stop_lon = row['geo_point_2d'].split(',')[1]  # Obtener la longitud de la parada
        stop_name = row['Direccion']  # Obtener el nombre de la parada
        
        folium.Marker(
            location=[float(stop_lat), float(stop_lon)],
            popup=stop_name,
            icon=folium.Icon(color='green', icon='bicycle', prefix='fa')
        ).add_to(marker_cluster)


    valencia_map.add_child(marker_cluster) #Añadimos al mapa los clusters


# MOSTRAR EL MAPA FINAL
folium.TileLayer('cartodbpositron').add_to(valencia_map)
# Mostrar el mapa interactivo en Streamlit
folium_static(valencia_map)
