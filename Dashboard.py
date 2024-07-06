import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

df_top10 = pd.read_csv('top10-stocks.csv', parse_dates=True, index_col='Date')

min_date = df_top10.index[0].to_pydatetime()
max_date = df_top10.index[-1].to_pydatetime()

color_scheme=px.colors.qualitative.Plotly

st.title('Dashboard de Ações')
st.sidebar.title('Filtros')

todo_periodo = st.sidebar.checkbox('Dados de todo o período', value = True)
if todo_periodo:
    start_date = ''
    end_date = ''
else:
    start_date, end_date = st.sidebar.slider('Datas', min_date, max_date, (min_date, max_date))

if start_date and end_date:
    df_top10 = df_top10[(df_top10.index >= start_date) & (df_top10.index <= end_date)]

df_log_returns = np.log(df_top10 / df_top10.shift(1)).dropna()
df_cumulative_returns = np.exp(df_log_returns.cumsum())

aba1, aba2, aba3 = st.tabs(['Gráficos', 'Estatísticas', 'Dados brutos'])

with aba1:
    fig_precos = px.line(data_frame=df_top10, y=df_top10.columns, color_discrete_sequence=color_scheme)
    fig_precos.update_layout(
        title='Fechamento histórico',
        xaxis_title='Data',
        yaxis_title='Preço fechamento',
        legend_title='Ticker')
    st.plotly_chart(fig_precos, use_container_width= True)

    fig_retornos_acumulados = px.line(data_frame=df_cumulative_returns, y=df_cumulative_returns.columns, color_discrete_sequence=color_scheme)
    fig_retornos_acumulados.update_layout(
        title='Retornos acumulados',
        xaxis_title='Data',
        yaxis_title='Retorno acumulado',
        legend_title='Ticker')
    st.plotly_chart(fig_retornos_acumulados, use_container_width= True)

with aba2:
    for i, ticker in enumerate(df_top10.columns):
        coluna1, coluna2 = st.columns([0.3, 0.7])
        with coluna1:
            price_mean = df_top10[ticker].mean()
            price_std = df_top10[ticker].std()
            log_returns_mean = df_log_returns[ticker].mean() * 100
            log_returns_std = df_log_returns[ticker].std() * 100
            st.metric('Média de preços para o período', 'R$ {:.2f}'.format(price_mean).replace('.', ','))
            st.metric('Desvio padrão dos preços para o período', 'R$ {:.2f}'.format(price_std).replace('.', ','))
            st.metric('Média de retornos logarítmicos para o período', '{:.2f} %'.format(log_returns_mean).replace('.', ','))
            st.metric('Desvio padrão dos retornos logarítmicos para o período', '{:.2f} %'.format(log_returns_std).replace('.', ','))
        with coluna2:
            color = color_scheme[i]
            fig_hist = px.histogram(data_frame=df_log_returns[ticker], marginal='box', color_discrete_sequence=[color])
            fig_hist.update_layout(
                title='Histograma dos Retornos Logarítmicos',
                xaxis_title='Valor',
                yaxis_title='Contagem',
                legend_title='Ticker')
            st.plotly_chart(fig_hist, use_container_width= True)

with aba3:
    st.dataframe(df_top10, use_container_width=True, column_config={
        'Date': st.column_config.DatetimeColumn(format='DD/MM/YYYY')
    })
