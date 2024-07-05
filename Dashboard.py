import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Dashboard de Ações')

df_ibov = pd.read_csv('../../IBOV-top10.csv', parse_dates=True, index_col='Date')
st.dataframe(df_ibov, use_container_width=True, column_config={
    "Date": st.column_config.DatetimeColumn(format="DD/MM/YYYY"
)})
