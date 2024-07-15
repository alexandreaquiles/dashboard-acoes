import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from portfolio_simulation import get_risk_free_rate, allocation_simulation


df_top10 = pd.read_csv('top10-stocks.csv', parse_dates=True, index_col='Date')
df_ibovespa = pd.read_csv('IBOVESPA.csv', parse_dates=True, index_col='Date')[['Close']].copy()
df_selic = pd.read_csv('selic_anualizada.csv', parse_dates=True, index_col='Data')

all_tickers = list(df_top10.columns)

min_date = df_top10.index[0].to_pydatetime()
max_date = df_top10.index[-1].to_pydatetime()

st.title('Simulação de Portfólio de Ações')
st.sidebar.title('Portfólio de Ações')

todo_periodo = st.sidebar.checkbox('Dados de todo o período', value = True)
if todo_periodo:
    start_date = ''
    end_date = ''
else:
    start_date, end_date = st.sidebar.slider('Datas', min_date, max_date, (min_date, max_date))

if start_date and end_date:
    df_top10 = df_top10[(df_top10.index >= start_date) & (df_top10.index <= end_date)]
    df_ibovespa = df_ibovespa[(df_ibovespa.index >= start_date) & (df_ibovespa.index <= end_date)]
    df_selic = df_selic[(df_selic.index >= start_date) & (df_selic.index <= end_date)]

tickers = st.sidebar.multiselect('Selecione os tickers', options=all_tickers, default=all_tickers, placeholder='Escolha um ou mais tickers')
if len(tickers) == 0:
    st.sidebar.error('Por favor, selecione um ou mais tickers.', icon='⛔')
if st.sidebar.button('Otimizar Portfólio'):
    df_portifolio = df_top10[tickers]
    log_returns_portifolio = np.log(df_portifolio / df_portifolio.shift(1)).dropna()

    risk_free_rate = get_risk_free_rate(df_selic['SELIC_Anualizada'].values)

    weights_all_simulations, cumulative_returns_all_simulations, risk_all_simulations, expected_return_all_simulations, sharpe_all_simulations = allocation_simulation(log_returns_portifolio, risk_free_rate)

    max_sharpe_idx = np.argmax(sharpe_all_simulations)
    weights_max_sharpe = weights_all_simulations[max_sharpe_idx]
    cumulative_returns_max_sharpe = cumulative_returns_all_simulations[max_sharpe_idx]
    risk_max_sharpe = risk_all_simulations[max_sharpe_idx]
    expected_return_max_sharpe = expected_return_all_simulations[max_sharpe_idx]
    max_sharpe = sharpe_all_simulations[max_sharpe_idx]

    min_risk_idx = np.argmin(risk_all_simulations)
    min_risk = risk_all_simulations[min_risk_idx]
    min_risk_expected_return = expected_return_all_simulations[min_risk_idx]

    rounded_weights_max_sharpe = np.round(weights_max_sharpe * 100).astype(int)
    df_alocacao_max_sharpe = pd.DataFrame(data=[rounded_weights_max_sharpe], columns=tickers)

    log_ibovespa_returns = np.log(df_ibovespa / df_ibovespa.shift(1)).dropna()
    cumulative_ibovespa_returns = np.exp(log_ibovespa_returns.cumsum()) - 1
    cumulative_returns = cumulative_ibovespa_returns.rename(columns={'Close':'IBOVESPA'})
    cumulative_returns['Portfolio'] = cumulative_returns_max_sharpe

    log_returns_correlation_portifolio = log_returns_portifolio.corr()

    st.header('Alocação randômica')
    st.caption('com taxa de Sharpe máxima (em %)')

    st.dataframe(df_alocacao_max_sharpe, use_container_width=True, hide_index=True)

    st.subheader('Indicadores para o período')
    coluna1, coluna2, coluna3, coluna4 = st.columns(4)
    with coluna1:
        st.metric('Retorno esperado portfólio', '{:.2f} %'.format(expected_return_max_sharpe * 100).replace('.', ','))
    with coluna2:
        st.metric('Risco portfólio', '{:.2f} %'.format(risk_max_sharpe * 100).replace('.', ','))
    with coluna3:
        st.metric('Taxa livre de risco (SELIC)', '{:.2f} %'.format(risk_free_rate * 100).replace('.', ','))
    with coluna4:
        st.metric('Taxa de Sharpe portfólio', '{:.2f}'.format(max_sharpe).replace('.', ','))

    fig_retornos_acumulados = px.line(data_frame=cumulative_returns * 100, y=cumulative_returns.columns)
    fig_retornos_acumulados.update_layout(
        title='Retornos acumulados Portfolio vs IBOVESPA',
        xaxis_title='Data',
        yaxis_title='Retorno acumulado (%)',
        legend_title='')
    st.plotly_chart(fig_retornos_acumulados, use_container_width= True)

    fig_portifolio_heatmap = px.imshow(log_returns_correlation_portifolio, text_auto=True)
    fig_portifolio_heatmap.update_layout(title='Correlações entre ativos do Portifólio')
    st.plotly_chart(fig_portifolio_heatmap, use_container_width= True)

    fig_risk_return = px.scatter(x=risk_all_simulations * 100, y=expected_return_all_simulations * 100,opacity=.2)
    fig_risk_return.add_scatter(x=[risk_max_sharpe * 100], y=[expected_return_max_sharpe * 100], marker={'size': 10, 'symbol': 'star', 'color': 'red'}, name='max sharpe')
    fig_risk_return.add_scatter(x=[min_risk * 100], y=[min_risk_expected_return * 100], marker={'size': 10, 'symbol': 'star', 'color': 'black'}, name='min risk')
    fig_risk_return.update_layout(
        title='Risco vs Retorno simulações',
        xaxis_title='Risco (%)',
        yaxis_title='Retorno esperado (%)',
        legend_title='')
    st.plotly_chart(fig_risk_return, use_container_width= True)

