import streamlit as st
import requests
import json
import pandas as pd

# URL con la lista de canales
URL = 'https://www.tdtchannels.com/lists/tv.json'

@st.cache_data
def obtener_datos(URL):
    res = requests.get(URL)
    data = res.json()
    return data

data = obtener_datos(URL)
# guardar json
# with open('tdt.json', 'w') as f:
#     json.dump(data, f)

# Vamos a contruir un dataframe con los datos
# Primero hay que reconstruir la estrutura de datos porque es un json no normalizado

def aplana_json(data):
    '''
    Vamos a extraer estas columnas del json: 'country', 'ambito', 'canal', 'logo', 'url'

    Las nombramos diferente para que no colisionen con las variables
    '''
    datos = []  # lista donde almacenar los datos. Es la que va a devolver la función
    for country in data:
        nombrec = country['name']
        ambitos = country['ambits']
        for ambito in ambitos:
            nombrea = ambito['name']
            canales = ambito['channels']
            for canal in canales:
                nombre_canal = canal['name']
                logo = canal['logo']
                options = canal['options']
                url = ''
                for option in options:
                    url = option['url']
                    break
                # Anadimos: Spain/Internacional,  nombre de ámbito, nombre de canal, logo, url
                datos.append([nombrec, nombrea, nombre_canal, logo, url])  
    return datos  

@st.cache_data
def crea_dataframe(datos):
    columnas = ['country', 'ambito', 'canal', 'logo', 'url']
    df = pd.DataFrame(datos, columns=columnas)
    return df

df = crea_dataframe(aplana_json(data['countries']))

def get_countries():
    return df.country.unique()

def get_ambitos(country):
    return df[df.country==country].ambito.unique()

def get_canales(country, ambito):
    return df[df.country==country][df.ambito==ambito]


st.title("Aplicación canales TDT")
st.markdown("#### Ejercicio de clase con streamlit y los datos de tdtchannels.com")
st.markdown('> Para verlo en el navegador tienes que instalar un plugin para `m3u8`')

columnas = st.columns(2)
with columnas[0]:
    canales = df.canal.unique().tolist()
    canales.insert(0, '')
    canaloption = st.selectbox(
        'Selecciona un canal', canales)

with columnas[1]:
    countries = get_countries()
    zona = st.radio('Selecciona Zona', countries)
    ambitos = get_ambitos(zona)
    ambito = st.selectbox('Selecciona Ambito', ambitos)

    # st.write(get_canales(data, zona, ambito))
    canales = get_canales(zona, ambito)

if canaloption:
    canales = df[df.canal==canaloption]

canalestxt=''
for c in canales.itertuples():
    # imagen = f'![{c["name"]}]({c["logo"]})'
    imagen = f'<img src="{c.logo}" alt="{c.canal}" width="50px" >'
    texto = (f'[{imagen}]({c.url})')
    canalestxt += texto + ' '
st.markdown(canalestxt, unsafe_allow_html=True)

## TODO
# - [ ] ver imágenes en columnas
