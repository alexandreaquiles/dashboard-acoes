import numpy as np
import pandas as pd

def get_risk_free_rate(selic_data):
    return selic_data.mean() / 100

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
        cumulative_returns[i, :] = np.exp(portfolio_returns.cumsum()) - 1

        expected_return_iteration = days * (np.exp(portfolio_returns.mean()) - 1)
        risk_iteration = np.sqrt(days) * (np.exp(portfolio_returns.std()) - 1)
        sharpe_iteration = (expected_return_iteration - risk_free_rate) / risk_iteration

        expected_return[i] = expected_return_iteration
        risk[i] = risk_iteration
        sharpe[i] = sharpe_iteration

    return weights, cumulative_returns, risk, expected_return, sharpe