import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Ticker da ação
ticker = "PETR4.SA"

## Intervalo de tempo do ativo
start_date = "2015-01-01"
end_date = "2023-05-15"

### API Yahoo Finance
data = yf.download(ticker, start=start_date, end=end_date)

#### Alteração para o período semanal (resample)
data_weekly = data.resample('W').last()

##### Linha de tendência com base no fechamento semanal
x = np.array(range(len(data_weekly)))
y = data_weekly['Close'].values
z = np.polyfit(x, y, 1)
p = np.poly1d(z)

###### Calcular o desvio padrão em relação à linha de tendência
std = np.std(y - p(x))

####### Linhas de desvio padrão
upper_bound = p(x) + std
lower_bound = p(x) - std
upper_bound_2 = p(x) + 2*std
lower_bound_2 = p(x) - 2*std

######## Plota a figura com a linha de tendência e as linhas de desvio padrão
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 6))

######### Gráfico do ativo
ax1.set_title('Cotação da PETR4')
ax1.set_ylabel('Preço (R$)')
ax1.grid(True)
ax1.plot(data_weekly.index, data_weekly['Close'], label='Preço', color='black')
ax1.plot(data_weekly.index, p(x), color='blue', label='Tendência')
ax1.plot(data_weekly.index, upper_bound, color='red', linestyle='--', label='1 Desvio Padrão (+)')
ax1.plot(data_weekly.index, lower_bound, color='green', linestyle='--', label='1 Desvio Padrão (-)')
ax1.plot(data_weekly.index, upper_bound_2, color='red', linestyle='-.', label='2 Desvios Padrões (+)')
ax1.plot(data_weekly.index, lower_bound_2, color='green', linestyle='-.', label='2 Desvios Padrões (-)')
ax1.legend()

########## Boxplot
current_price = data_weekly['Close'].iloc[-1]
ax2.boxplot(data_weekly['Close'], vert=True)
ax2.axhline(current_price, color='red', linestyle='--', label='Preço Atual: R${:.2f}'.format(current_price))
ax2.set_title('Boxplot')
ax2.set_ylabel('Preço (R$)')
ax2.legend()

########### Gráfico de histograma
ax3.hist(data_weekly['Close'], bins=20, color='blue', alpha=0.5)
ax3.set_title('Histograma de Preços')
ax3.set_xlabel('Preço (R$)')
ax3.set_ylabel('Frequência')

# Mostrar o gráfico
plt.show()
