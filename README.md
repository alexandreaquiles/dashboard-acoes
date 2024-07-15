# Dashboard de Ações

Dashboard implementado com [Streamlit](https://streamlit.io/) com dados históricos do período de 04/07/2019 a 04/07/2024 das ações com maior participação na composição do índice IBOVESPA. São elas: 

- B3SA3
- BBAS3
- BBDC4
- ELET3
- ITSA4
- ITUB4
- PETR3
- PETR4
- VALE3
- WEGE3.SA

https://dashboard-acoes-5vzjz4owuyka89dxhjd7kp.streamlit.app/


## Conceitos explorados 

No Dashboard:

- Retornos acumulados históricos para comparação dos ativos
- Estatísticas básicas (média e desvio padrão) dos preços e dos retornos logarítmicos para cada ação
- Histograma e boxplot dos retornos logarítmicos para cada ação
- Filtros por período

Na Simulação de Portfólio

- Composição randômica de carteira com 1000 simulações, escolhendo a com maior taxa de Sharpe
- Retorno esperado, risco, taxa livre de risco (SELIC) e taxa de sharpe usados como indicadores
- Retornos acumulados do portfólio comparando com IBOVESPA para o mesmo período
- Heatmap com correlação dos ativos do portfólio
- Gráfico da fronteira eficiente com destaque para a máxima taxa de Sharpe e menor risco

Foi considerada a composição do índice IBOVESPA para o dia 04/07/2024.

Os dados históricos de cada ação foram obtidos do Yahoo! Finance.


Referências:

- Composição do índice IBOVESPA: https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm
- Sistema Gerenciador de Séries Temporais do BCB (SELIC anualizada - código 1178) https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries
- Yahoo! Finance: https://finance.yahoo.com/