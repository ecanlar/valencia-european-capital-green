# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 12:20:08 2023

@author: Eva Cantin Larumbe, Adriana Chust Vendrell, Mikel Baraza Vidal
"""

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import  Polygon, MultiPolygon
import numpy as np
import plotly.graph_objects as go
import os


st.title("Green Areas")
  
    
# green area map
root_dir = os.getcwd()
root_dir = root_dir.replace('pages', 'data/espacios_verdes.csv')
data_path =  root_dir.replace("\\", "/")
print(data_path)

espacios_verdes = pd.read_csv(data_path, sep=';', encoding='utf-8')
nuevos_nombres = {'Id Jardí / Id. Jardín': 'ID', 'Nom / Nombre': 'Nombre', 'Barri / Barrio': 'Barrio', 'Tipologia / Tipología': 'Tipología', 'Àrea / Área': 'Área'}
espacios_verdes = espacios_verdes.rename(columns=nuevos_nombres)

root_dir = os.getcwd()
root_dir = root_dir.replace('pages', 'data/espacios_verdes.geojson')
data_path =  root_dir.replace("\\", "/")
map_data = gpd.read_file(data_path)



m = folium.Map(location=[39.46978308235751, -0.37701884302171607], 
               zoom_start=12, tiles='cartodbpositron')

for i in range(len(map_data['geometry'])):
    geometry = map_data['geometry'][i]
    if isinstance(geometry, Polygon):
        coordinates=[]
        for lat, long in list(geometry.exterior.coords):
            coordinates.append((long, lat))
        folium.Polygon(locations=coordinates, color='green', fill=True, fill_color='green', fill_opacity=0.4, popup=map_data['nombre'][i]).add_to(m)
    
    elif isinstance(geometry, MultiPolygon):
        for polygon in geometry.geoms:
            coordinates=[]
            for lat, long in list(polygon.exterior.coords):
                coordinates.append((long, lat))
            folium.Polygon(locations=coordinates, color='green', fill=True, fill_color='green', fill_opacity=0.4, popup=map_data['nombre'][i]).add_to(m)


# call to render Folium map in Streamlit
st.write('One of the most important factors for becoming a green capital are green areas. As shown, Valencia is plenty of green parks and gardens.')
st_data = st_folium(m, width=725)






# Per district
st.header("Featuring green areas per district")
st.write('The aim is to study which additional features have the green areas in each district. In that way, we can improve green area activities in each district.')

huerto_distrito = pd.DataFrame(espacios_verdes.groupby('DM')['Superficie Huerto Urbano'].sum().reset_index())
caninos_distrito = pd.DataFrame(espacios_verdes.groupby('DM')['Número Zonas Socialización Canina'].sum().reset_index())
fitness_distrito = pd.DataFrame(espacios_verdes.groupby('DM')['Número Elementos Fitness'].sum().reset_index())


todos = pd.merge(huerto_distrito, caninos_distrito, on='DM')
todos = pd.merge(todos, fitness_distrito, on ='DM')
todos = todos.rename(columns={'Superficie Huerto Urbano': 'Urban garden', 'Número Zonas Socialización Canina': 'Canine areas', 'Número Elementos Fitness': 'Fitness areas'})

total = np.sum([todos['Urban garden'], todos['Canine areas'], todos['Fitness areas']], axis=0)
porcentaje_huerto = (todos['Urban garden'] / total) * 100
porcentaje_caninos = (todos['Canine areas'] / total) * 100
porcentaje_fitness = (todos['Fitness areas'] / total) * 100

fig = go.Figure()
fig.add_trace(go.Bar(y=todos.DM, x=porcentaje_huerto, name='Urban garden', orientation='h', marker=dict(color='cyan')))
fig.add_trace(go.Bar(y=todos.DM, x=porcentaje_caninos, name='Canine areas', orientation='h', marker=dict(color='pink')))
fig.add_trace(go.Bar(y=todos.DM, x=porcentaje_fitness, name='Fitness areas', orientation='h', marker=dict(color='yellow')))
fig.update_layout(barmode='stack', xaxis_title='% of additional features', yaxis_title='District', legend_title='Additional features',  width=700, height=550)

st.plotly_chart(fig)



# containers
st.header("Green containers")
st.write('Another relevant factor when being the green capital of Europe are ecological containers. Oil, batteries and clothes containers have been studying.')

root_dir = os.getcwd()
root_dir = root_dir.replace('pages', 'data/contenedores_aceite.csv')
data_path =  root_dir.replace("\\", "/")
contenedores_aceite = pd.read_csv(data_path, sep=';', encoding='utf-8')
nuevos_nombres = {'objectid':'ID', 'Tipus / Tipo': 'Tipo', 'Centre / Centro': 'Centro', 'Adreça / Direccion' : 'Dirección', 'Districte / Distrito': 'Distrito', 'Barri / Barrio': 'Barrio', 'Oli / Aceite': 'Aceite', 'Estat / Estado': 'Estado'}
contenedores_aceite = contenedores_aceite.rename(columns=nuevos_nombres)

root_dir = os.getcwd()
root_dir = root_dir.replace('pages', 'data/contenedores_pilas.csv')
data_path =  root_dir.replace("\\", "/")
contenedores_pilas = pd.read_csv(data_path, sep=';', encoding='utf-8')
nuevos_nombres = {'objectid':'ID', 'Tipus / Tipo': 'Tipo', 'Centre / Centro': 'Centro', 'Adreça / Direccion' : 'Dirección', 'Districte / Distrito': 'Distrito', 'Barri / Barrio': 'Barrio', 'Piles / Pilas': 'Pilas', 'Observació / Observación': 'Observació', 'Codi / Código': 'Código'}
contenedores_pilas = contenedores_pilas.rename(columns=nuevos_nombres)


root_dir = os.getcwd()
root_dir = root_dir.replace('pages', 'data/contenedores_ropa.csv')
data_path =  root_dir.replace("\\", "/")
contenedores_ropa = pd.read_csv(data_path, sep=';', encoding='utf-8')
contenedores_ropa = contenedores_ropa.rename(columns={'distrito':'Distrito'})



dic = {1:'Ciutat Vella', 2:"L'Eixample", 3:'Extramurs', 4:'Campanar', 5:'La Saïdia', 6:'El Pla del Real', 7:"L'Olivereta", 8:'Patraix', 9:'Jesús', 10:'Quatre Carreres', 11:'Poblats Marítims', 12:'Camins al Grau', 13:'Algirós', 14:'Benimaclet', 15:'Rascanya', 16:'Benicalap', 17:'Poblats del Nord', 18:"Poblats de l'Oest", 19:'Poblats del Sud'}

for i in range(len(contenedores_aceite['Distrito'])):
    contenedores_aceite['Distrito'][i] = dic[contenedores_aceite['Distrito'][i]]
serie_aceite = contenedores_aceite['Distrito'].value_counts()

for i in range(len(contenedores_pilas['Distrito'])):
    contenedores_pilas['Distrito'][i] = dic[contenedores_pilas['Distrito'][i]]
serie_pilas = contenedores_pilas['Distrito'].value_counts()

for i in range(len(contenedores_ropa['Distrito'])):
    contenedores_ropa['Distrito'][i] = dic[contenedores_ropa['Distrito'][i]]
serie_ropa = contenedores_ropa['Distrito'].value_counts()





# containers map

m = folium.Map(location=[39.46978308235751, -0.37701884302171607], 
               zoom_start=12, tiles='cartodbpositron')

group0 = folium.FeatureGroup(name='<span style=\\"color: green;\\">Oil</span>')
for i in range(len(contenedores_aceite['geo_point_2d'])):
    coordenadas = list(contenedores_aceite['geo_point_2d'])[i]
    lat = coordenadas.split()[0].replace(',', '')    
    long = coordenadas.split()[1]
    folium.CircleMarker(location=[lat, long], radius=1, weight=5, color='green', popup=contenedores_aceite.Tipo[i]).add_to(group0)
group0.add_to(m)

group1 = folium.FeatureGroup(name='<span style=\\"color: purple;\\">Batteries</span>')
for i in range(len(contenedores_pilas['geo_point_2d'])):
    coordenadas = list(contenedores_pilas['geo_point_2d'])[i]
    lat = coordenadas.split()[0].replace(',', '')    
    long = coordenadas.split()[1]
    folium.CircleMarker(location=[lat, long], radius=1, weight=5, color='purple', popup=contenedores_pilas.Tipo[i], legend_name='Batteries').add_to(group1)
group1.add_to(m)

group2 = folium.FeatureGroup(name='<span style=\\"color: orange;\\">Clothes</span>')
for i in range(len(contenedores_ropa['geo_point_2d'])):
    coordenadas = list(contenedores_ropa['geo_point_2d'])[i]
    lat = coordenadas.split()[0].replace(',', '')    
    long = coordenadas.split()[1]
    folium.CircleMarker(location=[lat, long], radius=1, weight=5, color='orange', popup=contenedores_ropa.Empresa[i]).add_to(group2)
group2.add_to(m)


folium.map.LayerControl('topright', collapsed=False).add_to(m)
st_data = st_folium(m, width=725)





# containers bar chart
st.header("Featuring green containers per district")
st.write('It has been decided to study the containers according to the districts of Valencia so as to improve the homogeneity between municipal districts.')

oil, pilas, ropa = pd.DataFrame(serie_aceite), pd.DataFrame(serie_pilas), pd.DataFrame(serie_ropa)
todos = pd.merge(oil, pilas, left_index=True, right_index=True)
todos = pd.merge(todos, ropa, left_index=True, right_index=True)
todos = todos.rename(columns={'Distrito_x': 'Oil', 'Distrito_y': 'Batteries', 'Distrito': 'Clothes'})
 
fig = go.Figure()
fig.add_trace(go.Bar(y=todos.index, x=todos.Oil, name='Oil', orientation='h', marker=dict(color='green')))
fig.add_trace(go.Bar(y=todos.index, x=todos.Batteries, name='Batteries', orientation='h', marker=dict(color='purple')))
fig.add_trace(go.Bar(y=todos.index, x=todos.Clothes, name='Clothes', orientation='h', marker=dict(color='orange')))
fig.update_layout(barmode='stack', xaxis_title='Sum of containers', yaxis_title='District', legend_title='Containers')


st.plotly_chart(fig)


