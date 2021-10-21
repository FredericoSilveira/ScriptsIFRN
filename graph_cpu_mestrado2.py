import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import csv
import datetime


data_cpu4 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-08-23-AUTORAL-RASP4/Uso de CPU do sensor-data-as-seriestocolumns-2020-08-24 09 26 04.csv", sep=',')
data_cpu3 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-08-25-AUTORAL-RASP3/Uso de CPU do sensor-data-as-seriestocolumns-2020-08-26 09 06 09.csv", sep=',')

data_cpu4.columns=['Tempo', 'cpu_idle', 'cpu_sistema', 'cpu_usuario', 'cpu_iowait']
data_cpu3.columns=['Tempo', 'cpu_idle', 'cpu_sistema', 'cpu_usuario', 'cpu_iowait']

data_cpu4.drop(columns=['cpu_idle', 'cpu_sistema'],inplace=True)
data_cpu3.drop(columns=['cpu_idle', 'cpu_sistema'],inplace=True)

data_cpu4 = data_cpu4[data_cpu4['cpu_usuario'].notnull()]
data_cpu3 = data_cpu3[data_cpu3['cpu_usuario'].notnull()]

data_cpu4['Tempo'] = pd.to_datetime(data_cpu4['Tempo'])
data_cpu3['Tempo'] = pd.to_datetime(data_cpu3['Tempo'])
data_cpu4 = data_cpu4.set_index('Tempo')
data_cpu3 = data_cpu3.set_index('Tempo')

# print('data_cpu4')
# print(data_cpu4['cpu_usuario'])
# print(data_cpu4['cpu_sistema'])
# print('data_cpu3')
# print(data_cpu3['cpu_usuario'])
# print(data_cpu3['cpu_sistema'])

print('CPU4')
print(data_cpu4.head())
print('CPU3')
print(data_cpu3.head())
#
# df_cpu = data_cpu3.copy()
# df_cpu.columns = ['Tempo', 'Rasp3']
# df_cpu['Rasp4'] = data_cpu4['cpu']
# df_cpu['Tempo'] = pd.to_datetime(df_cpu['Tempo'])
#
# df_cpu = df_cpu.set_index('Tempo')
# df_cpu.dropna()
# print(df_cpu)

data_load4 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-08-23-AUTORAL-RASP4/CPU Load in vm-detection-data-as-seriestocolumns-2020-08-26 10 56 51.csv", sep=',')
data_load3 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-08-25-AUTORAL-RASP3/CPU Load in vm-detection-data-as-seriestocolumns-2020-08-26 09 07 08.csv", sep=',')

data_load4.columns=['Tempo', 'carga1', 'carga5', 'carga15']
data_load3.columns=['Tempo', 'carga1', 'carga5', 'carga15']


data_load4.drop(columns=['carga5', 'carga15'],inplace=True)
data_load3.drop(columns=['carga5', 'carga15'],inplace=True)

data_load4 = data_load4[data_load4['carga1'].notnull()]
data_load3 = data_load3[data_load3['carga1'].notnull()]


data_load4['Tempo'] = pd.to_datetime(data_load4['Tempo'])  #format="%Y-%m-%d %H:%M:%S"
data_load3['Tempo'] = pd.to_datetime(data_load3['Tempo'])

data_load4 = data_load4.set_index('Tempo')
data_load3 = data_load3.set_index('Tempo')

print('LOAD4')
print(data_load4.head())
print('LOAD3')
print(data_load3.head())

# df_load = data_load3.copy()
# df_load.columns = ['Tempo', 'Rasp3']
# df_load['Rasp4'] = data_load4['carga1']
# df_load['Tempo'] = pd.to_datetime(df_load['Tempo'])
#
# df_load = df_load.set_index('Tempo')
# df_load.dropna()
# print(df_load)

# fig = make_subplots(rows=2, cols=1, subplot_titles=("(a) Uso do Processador", "(b) Carga do Processador"))
#
# # fig.add_trace(go.Scatter(
# #                 x=data_cpu.index,
# #                 y=data_cpu['cpu_user'],
# #                 name="User CPU (%)",
# #                 mode="lines",
# #                 line_color='orange',
# #                 opacity=0.8), row=1, col=1)
# #
# # fig.add_trace(go.Scatter(
# #                 x=data_cpu.index,
# #                 y=data_cpu['cpu_system'],
# #                 name="System CPU (%)",
# #                 mode="lines",
# #                 line_color='green',
# #                 opacity=0.8), row=1, col=1)
#
# fig.add_trace(go.Scatter(
#                 x=data_cpu3.index.time,
#                 y=data_cpu3['cpu'],
#                 name="Uso do Processador",
#                 mode="lines",
#                 line_color='orange',
#                 opacity=0.8), row=1, col=1)
#
# fig.add_trace(go.Scatter(
#                 x=data_cpu4.index.time,
#                 y=data_cpu4['cpu'],
#                 name="Uso do Processador",
#                 mode="lines",
#                 line_color='green',
#                 opacity=0.8), row=1, col=1)
#
# fig.add_trace(go.Scatter(
#                 x=data_load3.index.time,
#                 y=data_load3['carga1'],
#                 name="Carga da CPU (média de 1min por núcleo)",
#                 mode="lines",
#                 xaxis=dict(nticks=5),
#                 line_color='blue',
#                 opacity=0.8), row=2, col=1)
#
# fig.add_trace(go.Scatter(
#                 x=data_load4.index.time,
#                 y=data_load4['carga1'],
#                 name="Carga da CPU (média de 1min por núcleo)",
#                 mode="lines",
#                 xaxis=dict(nticks=5),
#                 line_color='rgb(204,102,119)',
#                 opacity=0.8), row=2, col=1)
#
#
# fig.update_layout(xaxis=dict(nticks=5))
#
# fig.update_layout(width=700, height=700, legend=dict(orientation="h"))
# fig.layout.template = 'plotly_white'
#
# fig.show()
fig = go.Figure()

fig.add_trace(go.Scatter(
                x=data_cpu3.index,
                y=data_cpu3['cpu_usuario'],
                name="Rasp 3",
                mode="lines",
                line_color='orange',
                opacity=0.8))

fig.add_trace(go.Scatter(
                x=data_cpu3.index,
                y=data_cpu4['cpu_usuario'],
                name="Rasp 4",
                mode="lines",
                line_color='green',
                opacity=0.8))


#fig.update_layout(width=700, height=400, legend=dict(orientation="h"))
#fig.update_layout(xaxis=dict(nticks=7), legend=dict(orientation="h"), xaxis_title='Tempo real', yaxis_title='Uso do processador (%)')
fig.update_layout(xaxis=dict(nticks=24, title='Tempo real', type='date', tickformat='%H:%M', tickangle=-45),
                  #xaxis_title='Tempo real',
                  yaxis_title='Uso do processador (%)',
                  width=840, height=420,
                  font=dict(size=16),
                  legend=dict(
                       x=0.9,
                       y=0.9,
                       traceorder='normal',))
fig.layout.template = 'plotly_white'



fig.show()

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
                x=data_load3.index,
                y=data_load3['carga1'],
                name="Rasp 3",
                mode="lines",
                line_color='red',
                opacity=0.8))

fig2.add_trace(go.Scatter(
                x=data_load3.index,
                y=data_load4['carga1'],
                name="Rasp 4",
                mode="lines",
                line_color='blue',
                opacity=0.8))


#fig2.update_layout(width=700, height=400, legend=dict(orientation="h"))
#fig2.update_layout(xaxis=dict(nticks=7), legend=dict(orientation="h"), xaxis_title='Tempo real', yaxis_title='Número de processos (1min por núcleo)')
fig2.update_layout(xaxis=dict(nticks=24, type='date', tickformat='%H:%M', tickangle=-45),
                   xaxis_title='Tempo real',
                   yaxis_title='Número de processos',
                   font=dict(size=16),
                   width=840, height=420,
                   legend=dict(
                       x=0.9,
                       y=0.9,
                       traceorder='normal',))
fig2.layout.template = 'plotly_white'

fig2.show()
