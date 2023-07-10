import pandas as pd
import plotly.graph_objects as go

data_cpu4 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-09-11-BOT-IOT-RASP4/Uso de CPU do sensor-data-as-seriestocolumns-2020-09-11 17_46_28.csv", sep=',', index_col=0, parse_dates=True, infer_datetime_format=True)
data_cpu3 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-09-11-BOT-IOT-RASP3/original/Uso de CPU do sensor-data-as-seriestocolumns-2020-09-11 13_41_37.csv", sep=',', index_col=0, parse_dates=True, infer_datetime_format=True)
data_cpu4 = data_cpu4.iloc[:,0:3]
data_cpu3 = data_cpu3.iloc[:,0:3]

data_cpu4.rename(columns={"Time": "tempo", "CPU user time": "cpu_user", "CPU system time": "cpu_system"},inplace=True)
data_cpu3.rename(columns={"Time": "tempo", "CPU user time": "cpu_user", "CPU system time": "cpu_system"},inplace=True)

print('data_cpu4')
print(data_cpu4['cpu_user'])
print(data_cpu4['cpu_system'])
print('data_cpu3')
print(data_cpu3['cpu_user'])
print(data_cpu3['cpu_system'])

data_cpu4['cpu'] = data_cpu4['cpu_user'] + data_cpu4['cpu_system']
data_cpu3['cpu'] = data_cpu3['cpu_user'] + data_cpu3['cpu_system']

print('CPU4')
print(data_cpu4.head())
print('CPU3')
print(data_cpu3.head())

data_load4 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-09-11-BOT-IOT-RASP4/CPU Load-data-as-seriestocolumns-2020-09-11 17_46_37.csv", sep=',', index_col=0, parse_dates=True, infer_datetime_format=True)
data_load3 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-09-11-BOT-IOT-RASP3/original/CPU Load-data-as-seriestocolumns-2020-09-11 13_41_46.csv", sep=',', index_col=0, parse_dates=True, infer_datetime_format=True)
data_load4 = data_load4.iloc[:,0:3]
data_load3 = data_load3.iloc[:,0:3]


data_load4.rename(columns={"Time": "tempo", "Processor load (1 min average per core)": "carga1","Processor load (5 min average per core)": "carga5", "Processor load (15 min average per core)": "carga15"},inplace=True)
data_load3.rename(columns={"Time": "tempo", "Processor load (1 min average per core)": "carga1","Processor load (5 min average per core)": "carga5", "Processor load (15 min average per core)": "carga15"},inplace=True)


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
                x=data_cpu3.index.time,
                y=data_cpu3['cpu'],
                name="Uso do Processador Rasp 3",
                mode="lines",
                line_color='orange',
                opacity=0.8))

fig.add_trace(go.Scatter(
                x=data_cpu3.index.time,
                y=data_cpu4['cpu'],
                name="Uso do Processador Rasp 4",
                mode="lines",
                line_color='green',
                opacity=0.8))


#fig.update_layout(width=700, height=400, legend=dict(orientation="h"))
fig.update_layout(xaxis=dict(nticks=7), legend=dict(orientation="h"))
fig.layout.template = 'plotly_white'

fig.show()

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
                x=data_load3.index.time,
                y=data_load3['carga1'],
                name="Carga da CPU Rasp 3",
                mode="lines",
                line_color='red',
                opacity=0.8))

fig2.add_trace(go.Scatter(
                x=data_load3.index.time,
                y=data_load4['carga1'],
                name="Carga da CPU Rasp 4",
                mode="lines",
                line_color='blue',
                opacity=0.8))


fig2.update_layout(xaxis=dict(nticks=7))

#fig2.update_layout(width=700, height=400, legend=dict(orientation="h"))
fig2.update_layout(xaxis=dict(nticks=7), legend=dict(orientation="h"))
fig2.layout.template = 'plotly_white'

fig2.show()

# fig3 = make_subplots(rows=2, cols=1, subplot_titles=("(a) Uso do Processador", "(b) Carga do Processador"))
#
# fig3.add_trace(go.Scatter(
#                 x=data_cpu4.index,
#                 y=data_cpu4['cpu'],
#                 name="Uso do Processador",
#                 mode="lines",
#                 line_color='orange',
#                 opacity=0.8), row=1, col=1)
#
# fig3.add_trace(go.Scatter(
#                 x=data_load4.index,
#                 y=data_load4['carga1'],
#                 name="Carga da CPU (média de 1min por núcleo)",
#                 mode="lines",
#                 line_color='blue',
#                 opacity=0.8), row=2, col=1)
#
# #fig3.update_layout(width=700, height=400, legend=dict(orientation="h"))
# fig3.update_layout(xaxis=dict(nticks=7), legend=dict(orientation="h"))
# fig3.layout.template = 'plotly_white'
#
# fig3.show()



# fig4 = go.Figure(data=[go.Histogram(x=data_cpu3['cpu'])])
#
# fig4.update_layout(
#     bargap=0.01, # gap between bars of adjacent location coordinates
#     bargroupgap=0.01 # gap between bars of the same location coordinates
# )
# fig4.layout.template = 'plotly_white'
#
# fig4.show()
#
# fig5 = go.Figure(data=[go.Histogram(x=data_cpu4['cpu'])])
#
# fig5.update_layout(
#     #title_text='Distribuição da Memória Disponível (%)', # title of plot
#     #xaxis_title_text='Percentual de Memória Disponível', # xaxis label
#     #yaxis_title_text='Frequencia', # yaxis label
#     bargap=0.01, # gap between bars of adjacent location coordinates
#     bargroupgap=0.01 # gap between bars of the same location coordinates
# )
# fig5.layout.template = 'plotly_white'
#
# fig5.show()
#
# fig6 = go.Figure(data=[go.Histogram(x=data_load3['carga1'])])
#
# fig6.update_layout(
#     #title_text='Distribuição da Memória Disponível (%)', # title of plot
#     #xaxis_title_text='Percentual de Memória Disponível', # xaxis label
#     #yaxis_title_text='Frequencia', # yaxis label
#     bargap=0.01, # gap between bars of adjacent location coordinates
#     bargroupgap=0.01 # gap between bars of the same location coordinates
# )
# fig6.layout.template = 'plotly_white'
#
# fig6.show()
#
# fig7 = go.Figure(data=[go.Histogram(x=data_load4['carga1'])])
#
# fig7.update_layout(
#     #title_text='Distribuição da Memória Disponível (%)', # title of plot
#     #xaxis_title_text='Percentual de Memória Disponível', # xaxis label
#     #yaxis_title_text='Frequencia', # yaxis label
#     bargap=0.01, # gap between bars of adjacent location coordinates
#     bargroupgap=0.01 # gap between bars of the same location coordinates
# )
# fig7.layout.template = 'plotly_white'
#
# fig7.show()

print('Uso máximo da CPU - RASP3')
print(data_cpu3.max())

print('Uso máximo da CPU - RASP4')
print(data_cpu4.max())

print('Uso mínimo da CPU - RASP3')
print(data_cpu3.min())

print('Uso mínimo da CPU - RASP4')
print(data_cpu4.min())

print('Uso médio da CPU - RASP3')
print(data_cpu3.mean())

print('Uso médio da CPU - RASP4')
print(data_cpu4.mean())

print('Uso mediano da CPU - RASP3')
print(data_cpu3.median())

print('Uso mediano da CPU - RASP4')
print(data_cpu4.median())

###################################

print('Carga máxima da CPU - RASP3')
print(data_load3.max())

print('Carga máxima da CPU - RASP4')
print(data_load4.max())

print('Carga mínima da CPU - RASP3')
print(data_load3.min())

print('Carga mínima da CPU - RASP4')
print(data_load4.min())

print('Carga média da CPU - RASP3')
print(data_load3.mean())

print('Carga média da CPU - RASP4')
print(data_load4.mean())

print('Carga mediana da CPU - RASP3')
print(data_load3.median())

print('Carga mediana da CPU - RASP4')
print(data_load4.median())