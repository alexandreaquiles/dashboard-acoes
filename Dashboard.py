import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Dashboard de Ações')

df_ibov = pd.read_csv('../../IBOV-top10.csv', parse_dates=True, index_col='Date')

df_returns = np.log(df_ibov.pct_change().dropna())
df_cumulative_returns = (1 + df_returns).cumprod()

color_scheme=px.colors.qualitative.Plotly

aba1, aba2, aba3 = st.tabs(['Gráficos', 'Estatísticas', 'Dados brutos'])

with aba1:
    fig_precos = px.line(data_frame=df_ibov, y=df_ibov.columns, color_discrete_sequence=color_scheme)
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
    for i, ticker in enumerate(df_ibov.columns):
        coluna1, coluna2 = st.columns([0.3, 0.7])
        with coluna1:
            price_mean = df_ibov[ticker].mean()
            price_std = df_ibov[ticker].std()
            returns_mean = df_returns[ticker].mean() * 100
            returns_std = df_returns[ticker].std() * 100
            print(returns_mean)
            st.metric('Média de preços para o período', 'R$ {:.2f}'.format(price_mean).replace('.', ','))
            st.metric('Desvio padrão dos preços para o período', 'R$ {:.2f}'.format(price_std).replace('.', ','))
            st.metric('Média de retornos para o período', '{:.2f} %'.format(returns_mean).replace('.', ','))
            st.metric('Desvio padrão dos retornos para o período', '{:.2f} %'.format(returns_std).replace('.', ','))
        with coluna2:
            color = color_scheme[i]
            fig_hist = px.histogram(data_frame=df_returns[ticker], marginal='box', color_discrete_sequence=[color])
            fig_hist.update_layout(
                title='Histograma dos Retornos',
                xaxis_title='Valor',
                yaxis_title='Contagem',
                legend_title='Ticker')
            st.plotly_chart(fig_hist, use_container_width= True)

with aba3:
    st.dataframe(df_ibov, use_container_width=True, column_config={
        'Date': st.column_config.DatetimeColumn(format='DD/MM/YYYY'
    )})
