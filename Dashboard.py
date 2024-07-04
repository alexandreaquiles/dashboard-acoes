import streamlit as st
import pandas as pd
import plotly.express as px

df_ibov = pd.read_csv('../../IBOV-2024-07-04-top10-participacao.csv', parse_dates=True, index_col='Date')
st.dataframe(df_ibov, use_container_width=True)
