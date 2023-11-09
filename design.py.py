import streamlit as st
import pandas as pd
import json 
import sqlalchemy

import plotly.express as px
import plotly.io as pio
from sqlalchemy import create_engine,text
from pandas.io import sql
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu

st.title("PHONEPE PULSE DATA EXTRACTION FROM GITHUB - GUVI PROJECT BY HEMAMALINI")
img = Image.open("phonepeimg.png")
st.image(img,width=150)
mytitle2=st.selectbox('***Select***', ['agg_trans', 'agg_user', 'map_trans','map_user','top_trans','top_user'])
st.write('**You selected**:',mytitle2 )
col1,col2= st.columns(2)
with col1 :
    Year = st.selectbox("Year of Selection ",('2018','2019','2020','2021','2022'))
with col2 :
    Quarter = st.selectbox("Quarter of the year",('1','2','3','4'))
st.write("Year selection is : ",Year,"Quarter of the year is",Quarter)
fitter_val =st.selectbox('**Select**', ['Transaction_count', 'Transaction_amount','Pincode','Registered_users','Registered_user','App_opens','Count','Amount','Brands','Count','Percentage'])
st.write('**You selected**:',fitter_val )
plots=st.sidebar.radio('Select Plot', ['Scatter Plot'],horizontal=True)
sub_botton=st.sidebar.button('Get '+plots)
sql=f'select * from {mytitle2} where year={Year} and quarter={Quarter}'

engine = create_engine("mysql+pymysql://root:Chandran143*@localhost:3306/hemdb",pool_size=1000, max_overflow=2000)
mysql_df=pd.read_sql_query(sql,engine.connect(), index_col=None,chunksize=None)


st.write(mysql_df)
fig = px.choropleth(mysql_df,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations = 'State',
                    #color=color_column,
                    color_continuous_scale=px.colors.diverging.RdYlGn,
                    height=700)
fig.update_geos(fitbounds='locations', visible=False)
st.plotly_chart(fig, use_container_width=True)
def scatterplot(mysql_df):
        if fitter_val=='Transaction_type':
            fin_filter_val='Transaction_amount'
        if fitter_val=="Amount":
            fin_filter_val='Amount'
        data = [dict(
            type = 'scatter',
            x = mysql_df['State'],
            y = mysql_df[fin_filter_val],
            mode = 'markers',
            transforms = [dict(
                type = 'groupby',
                groups = mysql_df['State'],
               )]
        )]

        fig_dict = dict(data=data)
        pio.show(fig_dict, validate=False)
        st.plotly_chart(fig_dict)
        st.show(scatterplot(mysql_df))
        
        
        
mytitle3 = st.selectbox('***Select this if scatter Plot***', mysql_df["State"].unique())
if sub_botton:
    if plots=='Line Graph':
        fig = px.line(mysql_df, x='State', y=fin_filter_val)
        fig.show()
        
        
if sub_botton:
    if plots=='Scatter Plot':
                mysql_df = mysql_df.loc[mysql_df['State'] == mytitle3] 
            
           
#                 mysql_df = mysql_df.query("State" == mytitle3)
                scatterplot(mysql_df)



