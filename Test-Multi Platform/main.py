import streamlit as st
import stlib
from stlib import libcontents
import importlib


modulenames = libcontents.packages()
desc = []
modules = []

for modname in modulenames:
    m = importlib.import_module('.'+modname,'stlib')
    modules.append(m)
    try:
        desc.append(m.desc)
    except:
        desc.append(modname)
        
def format_func(name):
    return desc[modulenames.index(name)]


    
with st.sidebar:
    page = st.selectbox('Select:',modulenames, format_func=format_func)

modules[modulenames.index(page)].run()