import streamlit as st 
from streamlit_option_menu import option_menu
from PIL import Image 
# import leafmap.foliumap as leafmap
import plotly.express as px
import pandas as pd
from streamlit_folium import st_folium, folium_static
import folium
from last_seddel import *
from datetime import datetime

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

def bubblecolor(latest_date, eval_date):
    day_diff = (latest_date - eval_date).days
    if 0 <= day_diff <= 3:
        return 'green'
    elif 3 < day_diff <= 5:
        return 'yellow'
    elif 5 < day_diff <= 8:
        return 'orange'
    else:
        return 'red'



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

def min_profil():
    st.markdown('## Min profil')


def fiskeslag(df, arter, cords):
    
    

    st.markdown(
    """
    Denne siden gir deg oversikt over forrige ukes landinger i Norge, på den fiskearten du selv velger.
    På kartet tegnes bobler som viser informasjom om tilgjengelig mengde (boblestørrelse) og alder på fangst (farge).
    For å bruke verktøyet velger du først fiskeart i rullegardinsmenyen. Deretter vil det dukke opp en boble for hver lokasjon som har motatt
    fangst av denne arten innen den siste uke. Ved å trykke på en boble vil du få opp tilleggsinformasjon om fangsten.

    """)

    sel_art = st.selectbox('Velg en art', options=arter)
    # alder = st.slider('Alder på fangst', 0, 7*4*6, 7, 7)
    alder = 7*4*6
    filt = df[df['Art - FDIR'] == sel_art]
    latest_date = filt['Landingsdato'].max()
    start_date = latest_date - pd.Timedelta(days=alder)
    filt = filt[(filt['Landingsdato'] > start_date) & (filt['Landingsdato'] <= latest_date)]

    # locs = filt.groupby('Landingskommune')['Produktvekt'].sum().reset_index().query('Produktvekt > 0')
    locs = filt.groupby('Navn')['Produktvekt'].sum().reset_index().query('Produktvekt > 0')

    min_bubble = locs['Produktvekt'].min()
    max_bubble = locs['Produktvekt'].max()
    locs['BubbleSize'] = ((locs['Produktvekt'] - min_bubble) / (max_bubble - min_bubble)) * (10 - 1) + 1
    # df['Color'] = df['Landingsdato'].apply(lambda x: date_difference_color(pd.Timestamp("2023-08-10"), x))
    # locs['Color'] = locs['Landingsdato'].apply(lambda x: bubblecolor(latest_date, x))
 
    m = folium.Map(location=[65, 40], zoom_start=5, scrollWheelZoom=False, dragging=True, control_scale=False, prefer_canvas=True, zoom_control=True)
    # for i,row in locs.iterrows():
    #     kommunenavn = row['Landingskommune']
    #     if kommunenavn != 'OSLO':
    #         lat = cords[cords['Kommunenavn'] == kommunenavn]['Lat'].values[0]
    #         lon = cords[cords['Kommunenavn'] == kommunenavn]['Lon'].values[0]
            
    #         iframe = folium.IFrame('Kommune:' + str(row['Landingskommune']))
    #         popup = folium.Popup(iframe, max_width=300, min_width=100)
    #         folium.CircleMarker(
    #             location=[lat, lon],
    #             radius=row['BubbleSize'],  
    #             popup=popup,
    #             color='#3186cc',
    #             # color=row['Color'],
    #             fill=True,
    #             fill_color='#3186cc',
    #             tooltip=f"{row['Landingskommune']}: {row['Produktvekt']:,.0f} kg",
    #         ).add_to(m)
    for i, row in locs.iterrows():
        navn = row['Navn']
        lat = df[df['Navn'] == navn]['Lat'].values[0]
        lon = df[df['Navn'] == navn]['Lon'].values[0]
        if pd.isna(lat):
            continue
        iframe = folium.IFrame('Mottaker:' + str(row['Navn']))
        popup = folium.Popup(iframe, max_width=300, min_width=100)
        folium.CircleMarker(
            location=[lat, lon],
            radius=row['BubbleSize'],
            popup=popup,
            color='#3186cc',
            # color=row['Color'],
            fill=True,
            fill_color='#3186cc',
            tooltip=f"{row['Navn']}: {row['Produktvekt']:,.0f} kg",
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

        selected_mottak = str(map_out['last_object_clicked_tooltip']).split(':')[0]
        if selected_mottak == 'None':
            st.header('Velg en boble')
        else:
            tempdf = filt[filt['Navn'] == selected_mottak]
            st.title(selected_mottak.title())
            mottak_adresse = df[df['Navn'] == selected_mottak]['Adresse'].values[0]
            
            mottak_url = selected_mottak.lower().replace(' ', '+')
            mottak_url = 'https://www.gulesider.no/' + mottak_url + '/bedrifter/'
            st.write(f'**Adresse**: {mottak_adresse}, [Gule sider]({mottak_url})')
            tempdf = tempdf.groupby(['Landingsdato'])['Produktvekt'].sum().reset_index().sort_values(by='Landingsdato', ascending=False)
            st.header(f'Siste landinger av {sel_art.lower()}:')
            for i, row in tempdf.iterrows():
                #calculate how many days between today and row['Landingsdato']
                today = datetime.today()
                days = (today - row['Landingsdato']).days

                



                st.write(f"**{row['Landingsdato'].strftime('%d.%m.%Y')}:** {row['Produktvekt']:,.0f} kg, {days} dager siden")

            
def om(df):
    st.markdown('''
                
    TODO:
    - Filtrer masterframe på dato (siste uke. Gjøres i The_Others.py og sendes som argument til funksjonen)
    - Se på popup options
    - Se på fargekoder ift. alder på fangst
    - Lag funksjon der man trykker på Kommune, og får listet opp ny df per Mottaker ID. Bruk orgnummer.pkl til å hente forretningsnavn. 
                ''')
    
    st.write(df.sort_values(by='Landingsdato', ascending=False).head(20))
    latest_date = df['Landingsdato'].max()
    daysback = st.slider('Velg en verdi', 1, 30, 7)
    start_date = latest_date - pd.Timedelta(days=daysback)
    dfweek = df[(df['Landingsdato'] > start_date) & (df['Landingsdato'] <= latest_date)]
    dfweek = dfweek.sort_values(by='Landingsdato', ascending=True)
    st.write(dfweek)