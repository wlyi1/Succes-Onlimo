description = 'home'

def run():
    import pandas as pd
    import pymysql
    import sqlalchemy as sql
    import streamlit as st
    import datetime 
    from datetime import datetime as dt
    import matplotlib.pyplot as plt
    import seaborn as sns
    import streamlit.components.v1 as components
    import stlib
    from stlib import libcontents
    import importlib

    st.title('Stasiun Onlimo - MA')

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

    def run_query(query):
        engine = sql.create_engine('mysql+pymysql://root@localhost:3306/onlimo_ma?charset=utf8mb4')
        df = pd.read_sql_query(query, engine)
        return df

    id_ol = list(range(41,45))
    varname = []
    for i in id_ol:
                 varname.append('ol' +str(i))


    for df in varname:
        globals()[f'{df}'] = run_query(f'select * from {df};')   
        globals()[f'pH_{df}'] = [x for x in globals()[f'{df}'][-24:]['pH']]
        globals()[f'ab_pH_{df}'] = sum(map(lambda x : x<5 and x>9, globals()[f'pH_{df}']))
        globals()[f'DO_{df}'] = [x for x in globals()[f'{df}'][-24:]['DO_']]
        globals()[f'ab_DO_{df}'] = sum(map(lambda x : x<1, globals()[f'DO_{df}']))
        globals()[f'NH4_{df}'] = [x for x in globals()[f'{df}'][-24:]['NH4']]
        globals()[f'ab_NH4_{df}'] = sum(map(lambda x : x>100, globals()[f'NH4_{df}']))
        globals()[f'NO3_{df}'] = [x for x in globals()[f'{df}'][-24:]['NO3']]
        globals()[f'ab_NO3_{df}'] = sum(map(lambda x : x>100, globals()[f'NO3_{df}']))
        globals()[f'tgl_{df}'] = globals()[f'{df}']['TGL'].max().strftime(("%Y-%m-%d %H:%M"))



    #KLHK

    def status_onlimo(id_ol):
        st.header(id_ol)
        globals()[f'header_a_{id_ol}'], globals()[f'header_b_{id_ol}'] = st.columns(2)
        tgl_hm = globals()[f'{id_ol}']['TGL'].max().strftime(("%Y-%m-%d %H:%M"))
        tgl = globals()[f'{id_ol}']['TGL'].max().strftime(("%Y-%m-%d %H:%M"))

        if tgl == dt.today().strftime('%Y-%m-%d'): 
            globals()[f'header_a_{id_ol}'].button(tgl_hm, key=f'{id_ol}_a')
            globals()[f'header_b_{id_ol}'].success('ONLINE')

        elif tgl < dt.today().strftime('%Y-%m-%d'): 
            globals()[f'header_a_{id_ol}'].button(tgl_hm, key=f'{id_ol}_b')
            globals()[f'header_b_{id_ol}'].warning('OFFLINE')

        else:
            globals()[f'header_a_{id_ol}'].button(tgl_hm, key=f'{id_ol}_b')                  
            globals()[f'header_b_{id_ol}'].error('ERROR')   

        col1, col2, col3, col4 = st.columns(4)
        col1.metric('pH', globals()[f'ab_pH_{id_ol}'], globals()[f'pH_{id_ol}'][-1])
        col2.metric('DO', globals()[f'ab_DO_{id_ol}'], globals()[f'DO_{id_ol}'][-1])
        col3.metric('NH', globals()[f'ab_NH4_{id_ol}'], globals()[f'NH4_{id_ol}'][-1])
        col4.metric('NO', globals()[f'ab_NO3_{id_ol}'], globals()[f'NO3_{id_ol}'][-1])

        st.markdown("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


    for ol in varname:
        status_onlimo(ol)



    

    
    
    
    