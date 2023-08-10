import streamlit as st 
from streamlit_option_menu import option_menu
from PIL import Image 
import leafmap.foliumap as leafmap
import plotly.express as px
import pandas as pd
from streamlit_folium import st_folium, folium_static
import folium
from last_seddel import *


def logo():
    col1, col2, col3 = st.columns([0.4,0.2,0.4])
    image = Image.open('pages/resources/logo.png')
    col2.image(image, width=400)
    col2.markdown(
        """
        """,
        unsafe_allow_html=True,
    )

def add_header(text):
    st.markdown(f"<h1 style='text-align: center;'>{text}</h1>", unsafe_allow_html=True)


def menu():
    sel = option_menu(None, ["Sesong", "Historisk", "Min profil", 'Om'], 
    icons=['map', 'calendar-week', "file-earmark-person", 'patch-question'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    return sel

def sesong():
    
    df = pd.read_csv('wellbore_exploration_all.csv', 
                usecols=['wlbWellboreName', 'wlbNsDecDeg', 'wlbEwDesDeg'])

    df.columns = ['Well Name', 'latitude', 'longitude']

    col1, col2 = st.columns([1,1])

    col1.multiselect('Velg en verdi', options=['a', 'b', 'c'])
    col2.multiselect('Velg en verdi2', options=['a', 'b', 'c'])
    latcap = st.slider('Velg en verdi', df['latitude'].min(), df['latitude'].max(), float(2))
    df = df[df['latitude'] > latcap]
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_name='Well Name', zoom=5)
    fig.update_layout(
    legend_title='Uke',
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'style': "open-street-map",
        'center': {'lon': 13, 'lat': 66},
        'zoom': 4,
        'bearing': -55}
        )

    st.plotly_chart(fig, use_container_width=True)
    
    
    

def historisk():
    st.markdown('## Historisk')
    st.write('2+2')
    st.select_slider('Velg en verdi', options=['a', 'b', 'c'])

def min_profil():
    st.markdown('## Min profil')
    st.write('3+3')
    st.select_slider('Velg type fis', options=['a', 'b', 'c'])

def om(df, arter, cords):
    
    

    st.markdown(
    """
    Denne siden gir deg oversikt over forrige ukes landinger i Norge, på den fiskearten du selv velger.
    På kartet tegnes bobler som viser informasjom om tilgjengelig mengde (boblestørrelse) og alder på fangst (farge).
    For å bruke verktøyet velger du først fiskeart i rullegardinsmenyen. Deretter vil det dukke opp en boble for hver lokasjon som har motatt
    fangst av denne arten innen den siste uke. Ved å trykke på en boble vil du få opp tilleggsinformasjon om fangsten.

    TODO:
    - Filtrer masterframe på dato (siste uke. Gjøres i The_Others.py og sendes som argument til funksjonen)
    - Se på popup options
    - Se på fargekoder ift. alder på fangst
    - Lag funksjon der man trykker på Kommune, og får listet opp ny df per Mottaker ID. Bruk orgnummer.pkl til å hente forretningsnavn. 
    """)

    sel_art = st.selectbox('Velg en art', options=arter)
    filt = df[df['Art - FDIR'] == sel_art]
    locs = filt.groupby('Landingskommune')['Produktvekt'].sum().reset_index().query('Produktvekt > 0')

    min_bubble = locs['Produktvekt'].min()
    max_bubble = locs['Produktvekt'].max()
    locs['BubbleSize'] = ((locs['Produktvekt'] - min_bubble) / (max_bubble - min_bubble)) * (10 - 1) + 1


    m = folium.Map(location=[65, 40], zoom_start=5, scrollWheelZoom=False, dragging=True, control_scale=False, prefer_canvas=True, zoom_control=True)
    for i,row in locs.iterrows():
        kommunenavn = row['Landingskommune']
        if kommunenavn != 'OSLO':
            lat = cords[cords['Kommunenavn'] == kommunenavn]['Lat'].values[0]
            lon = cords[cords['Kommunenavn'] == kommunenavn]['Lon'].values[0]
            
            iframe = folium.IFrame('Kommune:' + str(row['Landingskommune']))
            popup = folium.Popup(iframe, max_width=300, min_width=100)
            folium.CircleMarker(
                location=[lat, lon],
                radius=row['BubbleSize'],  
                popup=popup,
                color='#3186cc',
                fill=True,
                fill_color='#3186cc',
                tooltip=f"{row['Landingskommune']}: {row['Produktvekt']:,.0f} kg",
            ).add_to(m)
            

            # folium.Marker(location=[lat, lon], popup=popup, tooltip=row['Landingskommune']).add_to(m)
    # for i,row in df.iterrows():
    #     iframe = folium.IFrame('Well name:' + str(row['Well Name']))
    #     popup = folium.Popup(iframe, max_width=300, min_width=300)
    #     folium.Marker(location=[row['latitude'], row['longitude']], popup=popup, tooltip=row['Well Name']).add_to(m)


    col1, col2= st.columns([12,12])
    with col1: 
        map_out = st_folium(m, width=1800, height=1000)
    with col2:
        try:
            st.write(map_out)
        except:
            st.write(map_out)    
    