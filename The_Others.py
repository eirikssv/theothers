import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
# import leafmap.foliumap as leafmap
from pages.mods.funcs import *


st.set_page_config(layout="wide",
                page_title='The Others',
                )

@st.cache_data
def last_seddel():
    df = pd.read_csv('others_with_coordinates.csv')
    return df

@st.cache_data
def last_cords():
    cords = pd.read_pickle('ListeKommunekoderKoordinater.pkl')
    return cords

df = last_seddel()
cords = last_cords()
object_to_date = [  'Dokument salgsdato', 
                        # 'Dokument versjonstidspunkt', 
                        # 'Oppdateringstidspunkt', 
                        'Siste fangstdato',
                        'Landingsdato',
                        ]
for el in object_to_date:
    df[el] = pd.to_datetime(df[el], dayfirst=True)


_, col1, _ = st.columns([1/6,4/6,1/6])
with col1:
    logo()
    selected = menu()


arter = ['Breiflabb', 'Brosme', 'Gapeflyndre']



if selected == 'Sesong':
    _, col1, _ = st.columns([1/6,4/6,1/6])
    with col1:
        left, right = st.tabs(['🐟 Fiskeslag', '⚓ Landing'])
        with left:
            fiskeslag(df, arter, cords)
        with right:
            st.write('Landing')


elif selected == 'Historisk':
    _, col1, _ = st.columns([1/6,4/6,1/6])
    with col1:
        historisk()
elif selected == 'Min profil':
    _, col1, _ = st.columns([1/6,4/6,1/6])
    with col1:
        min_profil()
elif selected == 'Om':
    _, col1, _ = st.columns([1/6,4/6,1/6])
    with col1:
    
        st.write('Dev stuff')
        om(df)



else:
    st.write('Noe gikk galt')





