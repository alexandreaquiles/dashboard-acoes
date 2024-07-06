import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from bcb import sgs

st.title('Simulação de Portfólio de Ações')

df_ibov = pd.read_csv('../../IBOV-top10.csv', parse_dates=True, index_col='Date')
df_ibovespa = pd.read_csv('../../IBOVESPA.csv', parse_dates=True, index_col='Date')
df_ibovespa = df_ibovespa[['Close']].copy()

all_tickers = list(df_ibov.columns)

min_date = df_ibov.index[0].to_pydatetime()
max_date = df_ibov.index[-1].to_pydatetime()

work_days = 252

st.sidebar.title('Portfólio de Ações')

todo_periodo = st.sidebar.checkbox('Dados de todo o período', value = True)
if todo_periodo:
    start_date = ''
    end_date = ''
else:
    start_date, end_date = st.sidebar.slider('Datas', min_date, max_date, (min_date, max_date))

if start_date and end_date:
    df_ibov = df_ibov[(df_ibov.index >= start_date) & (df_ibov.index <= end_date)]
    df_ibovespa = df_ibovespa[(df_ibovespa.index >= start_date) & (df_ibovespa.index <= end_date)]

def get_risk_free_rate(start_date, end_date):
    cdi = sgs.get({'BCB-Demab': 11}, start=start_date, end = end_date)
    risk_free_rate_cdi = cdi.mean() / 100 * work_days
    return risk_free_rate_cdi[0]

def random_allocation(size):
    rand = np.random.rand(size)
    normalized_rand = rand / rand.sum()
    return normalized_rand

def allocation_simulation(log_returns, risk_free_rate, iterations=1000):
    portfolio_size = len(log_returns.columns)
    days = len(log_returns)

    weights = np.zeros((iterations, portfolio_size))
    cumulative_returns = np.zeros((iterations, days))
    risk = np.zeros(iterations)
    expected_return = np.zeros(iterations)
    sharpe = np.zeros(iterations)
    
    for i in range(iterations):
        allocation = random_allocation(portfolio_size)
        weights[i, :] = allocation

        portfolio_returns = log_returns @ allocation 
        cumulative_returns[i, :] = np.exp(portfolio_returns.cumsum())

        expected_return_iteration = days * (np.exp(portfolio_returns.mean()) - 1)
        risk_iteration = np.sqrt(days) * (np.exp(portfolio_returns.std()) - 1)
        sharpe_iteration = (expected_return_iteration - risk_free_rate) / risk_iteration

        expected_return[i] = expected_return_iteration
        risk[i] = risk_iteration
        sharpe[i] = sharpe_iteration

    return weights, cumulative_returns, risk, expected_return, sharpe

def optimize_portfolio(tickers):
    df_portifolio = df_ibov[tickers]
    log_returns = np.log(df_portifolio / df_portifolio.shift(1)).dropna()
    risk_free_rate = get_risk_free_rate(start_date, end_date)
    weights, cumulative_returns, risk, expected_return, sharpe = allocation_simulation(log_returns, risk_free_rate)
    max_sharpe_idx = np.argmax(sharpe)
    return weights[max_sharpe_idx], cumulative_returns[max_sharpe_idx], risk[max_sharpe_idx], expected_return[max_sharpe_idx], sharpe[max_sharpe_idx]

tickers = st.sidebar.multiselect('Selecione os tickers', options=all_tickers, default=all_tickers, placeholder='Escolha um ou mais tickers')
if len(tickers) == 0:
    st.sidebar.error('Por favor, selecione um ou mais tickers.', icon='⛔')
if st.sidebar.button('Otimizar Portfólio'):
    weights, cumulative_returns, risk, expected_return, sharpe = optimize_portfolio(tickers)
    rounded_weights = np.round(weights * 100).astype(int)
    st.header('Alocação')
    st.dataframe(pd.DataFrame(data=[rounded_weights], columns=tickers), use_container_width=True, hide_index=True)
    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric('Retorno esperado portfólio', '{:.2f} %'.format(expected_return).replace('.', ','))
    with coluna2:
        st.metric('Risco portfólio', '{:.2f} %'.format(risk).replace('.', ','))
    with coluna3:
        st.metric('Taxa de Sharpe portfólio', '{:.2f} %'.format(sharpe).replace('.', ','))

    log_ibovespa_returns = np.log(df_ibovespa / df_ibovespa.shift(1)).dropna()
    cumulative_ibovespa_returns = np.exp(log_ibovespa_returns.cumsum())
    cumulative_ibovespa_returns = cumulative_ibovespa_returns.rename(columns={'Close':'IBOVESPA'})
    cumulative_ibovespa_returns['Portfolio'] = cumulative_returns

    fig_retornos_acumulados = px.line(data_frame=cumulative_ibovespa_returns, y=cumulative_ibovespa_returns.columns)
    fig_retornos_acumulados.update_layout(
        title='Retornos acumulados Portfolio vs IBOVESPA',
        xaxis_title='Data',
        yaxis_title='Retorno acumulado',
        legend_title='')
    st.plotly_chart(fig_retornos_acumulados, use_container_width= True)

