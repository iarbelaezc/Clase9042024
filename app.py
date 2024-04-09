import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import json

with open('Mapa de Accidentalidad Vial Municipio de Medellín 2016.geojson', "r") as read_file:
    data = json.load(read_file)

st.title("Accidentalidad Municipio de Medellín 2016")

st.write('Se entiende por accidente de tránsito  evento, generalmente involuntario, generado al menos por un un vehículo en movimiento, que causa daños a '
         'personas y bienes involucrados en él, e igualmente afecta la normal circulación de los vehículos que se movilizan por la vía o vías comprendidas en el' 
         'lugar o dentro de la zona de influencia del hecho0 (Ley 769 de 2002 - Código Nacional de Tránsito)'
         )
st.subheader('Sistema de consulta de Accidentalidad municipio de Medellín')

La = []
Lo= []
day=[]
hour=[]
neig=[]
dir=[]    

# Decodificar el archivo en formato JSON (Java Script Object Notation)
for feature in data['features']:
    coordinates = feature['geometry']['coordinates']
    dia=feature['properties']['dia']
    Hora=feature['properties']['hora']
    barrio=feature['properties']['barrio']
    direccion=feature['properties']['direccion']
    La.append(coordinates[1])
    Lo.append(coordinates[0])  
    day.append(dia)
    hour.append(Hora)
    neig.append(barrio)
    dir.append(direccion)
    
nm= st.slider('Selecciona el número de registros de accidentes quieres visualizar', 5, 1500)
#Construir la tabla de datos (dataframe)
dfLa = pd.DataFrame({'lat':La[0 : nm]})
dfLo = pd.DataFrame({'lon':Lo[0 : nm]})
dfdia= pd.DataFrame({'día' :day[0:nm]})
dfhor= pd.DataFrame({'Hora' :hour[0:nm]})
dfbarr=pd.DataFrame({'Barrio':neig[0:nm]})
dfdir=pd.DataFrame({'Dirección':dir[0:nm]})
df_g=pd.concat([dfLa, dfLo, dfdia, dfhor,dfdir,dfbarr], axis=1)

# Mostrar la tabla de datos (dataframe)
st.dataframe(df_g)
#Dibujar el mapa utilizando las columnas 'lat', 'lon'.
st.map(df_g)

# Realizar un filtrado de los datos
st.subheader('Filtrado')
option_hour_min = st.selectbox('Selecciona filtro por Hora',
                               ('08:00:00', '09:00:00', '10:00:00','11:00:00','12:00:00','13:00:00','14:00:00'),key='1')
#option_hour_max = st.selectbox('Selecciona filtro por Hora',
#                               ('08:00:00', '09:00:00', '10:00:00','11:00:00','12:00:00','13:00:00','14:00:00'),key='2')
option_day = st.selectbox('Selecciona filtro por día',('LUNES', 'MARTES', 'MIÉRCOLES','JUEVES','VIERNES','SÁBADO','DOMINGO'))
#df_filtrado = df_g.query('día == "MIÉRCOLES" and Hora >= "08:00:00" and Hora <= "10:00:00"')
df_filtrado = df_g.query('día == @option_day and Hora >=  @option_hour_min ')
st.dataframe(df_filtrado)

try:
   st.metric("Cantidad de Incidentes dentro del filtro", df_filtrado.shape[0])
except:
    pass


st.map(df_filtrado)
#st.write(df)
