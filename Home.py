# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 11:59:35 2023

@author: Eva Cantin Larumbe, Adriana Chust Vendrell, Mikel Baraza Vidal
"""

import streamlit as st
import os 

st.set_page_config(
    page_title="Valencia capital verde Europea",)

def pagina_pricipal():
    st.markdown("# Valencia, Green European Capital of 2024")
    st.sidebar.markdown("# Home")

def Green_Areas():
    st.markdown("# Green areas")
    st.sidebar.markdown("# Green areas")
    
def Air_Pollution():
    st.markdown("# Air pollution")
    st.sidebar.markdown("# Air pollution")
    
def Transport():
    st.markdown("# Transport")
    st.sidebar.markdown("# Transport")



page_names_to_funcs = {
    "Main page": pagina_pricipal,
    "Green areas": Green_Areas,
    "Air pollution": Air_Pollution,
    "Transport":Transport
}


st.title('Valencia, Green European Capital of 2024')

st.markdown(
    """
    Last October 2022, Valencia was awarded the 2024 European Capital Green. The candidacy was based on four pillars: increasing green infrastructure and promoting urban biodiversity, the climate mission and energy efficiency, sustainable mobility, and the recovery of public space and sustainable food linked to the Horta.
"""
)

st.markdown(
'**👈 Select a pillar to analyse it!**'
)

from PIL import Image

current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "data", "valencia.jpg")

image = Image.open('data/valencia.jpg')

st.image(image, caption='2024 European Capital Green')

