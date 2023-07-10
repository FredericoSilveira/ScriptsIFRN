import pandas as pd
import pandas as pd
import plotly.graph_objs as go

data_mem_rasp4 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-08-23-AUTORAL-RASP4/Memory usage in vm-detection-data-as-seriestocolumns-2020-08-24 09 26 27.csv", sep=',', index_col=0, parse_dates=True, infer_datetime_format=True)
data_mem_rasp3 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-08-25-AUTORAL-RASP3/Memory usage in vm-detection-data-as-seriestocolumns-2020-08-26 09 06 58.csv", sep=',', index_col=0, parse_dates=True, infer_datetime_format=True)
data_mem_rasp3= data_mem_rasp3.iloc[:,0:3]
data_mem_rasp4= data_mem_rasp4.iloc[:,0:3]

data_mem_rasp3.rename(columns={"Time": "tempo", "Available memory": "memoria_disponivel"},inplace=True)
data_mem_rasp4.rename(columns={"Time": "tempo", "Available memory": "memoria_disponivel"},inplace=True)

#RASP4
data_mem_rasp4['memoria_disponivel'] = data_mem_rasp4['memoria_disponivel']/1000000
#RASP3
data_mem_rasp3['memoria_disponivel'] = data_mem_rasp3['memoria_disponivel']/1000000

print('RASP3')
print(data_mem_rasp3)
print('RASP4')
print(data_mem_rasp4)

mem_disp_rasp3_rel = data_mem_rasp3['memoria_disponivel']/1000
mem_disp_rasp4_rel = data_mem_rasp4['memoria_disponivel']/4000

#print(mem_disp_rasp4_rel)

mean_mem_disp_rasp3 = np.mean(mem_disp_rasp3_rel)
mean_mem_disp_rasp4 = np.mean(mem_disp_rasp4_rel)

#RASP3
#print(mean_mem_disp_rasp3)
#RASP4
#print(mean_mem_disp_rasp4)

num_rasp3 = len(data_mem_rasp3['memoria_disponivel'])
num_rasp4 = len(data_mem_rasp4['memoria_disponivel'])


list_mean_mem_disp_raps3 = num_rasp3 * [mean_mem_disp_rasp3]
list_mean_mem_disp_raps4 = num_rasp4 * [mean_mem_disp_rasp4]

fig = go.Figure()

fig.add_trace(go.Scatter(
                x=data_mem_rasp3.index,
                y=data_mem_rasp4['memoria_disponivel'],
                name="Rasp 4",
                mode="lines",
                line_color='green',
                opacity=0.8))

fig.add_trace(go.Scatter(
                x=data_mem_rasp3.index,
                y=data_mem_rasp3['memoria_disponivel'],
                name="Rasp 3",
                mode="lines",
                line_color='orange',
                opacity=0.8))

fig.update_layout(xaxis=dict(nticks=24, title='Tempo real', type='date', tickformat='%H:%M', tickangle=-45),
                   xaxis_title='Tempo real',
                   yaxis_title='Memória disponóvel (MB)',
                   width=840, height=420,
                   font=dict(size=16),
                   legend=dict(
                       x=0.9,
                       y=0.9,
                       traceorder='normal',))
fig.layout.template = 'plotly_white'

fig.show()


# fig_rasp4 = make_subplots(rows=2, cols=1, subplot_titles=("(a) Uso de memória", "(b) Relação Memória Livre/Memória Total"))
#
#
# fig_rasp4.add_trace(go.Scatter(
#                 x=data_mem_rasp4.index,
#                 y=data_mem_rasp4['memoria_disponivel'],
#                 name="Memória (GB)",
#                 mode="lines",
#                 line_color='red',
#                 opacity=0.8), row=1, col=1)
#
# fig_rasp4.add_trace(go.Scatter(
#                 x=data_mem_rasp4.index,
#                 y=mem_disp_rasp4_rel,
#                 name="Memória livre/Memória total",
#                 mode="lines",
#                 line_color='purple',
#                 opacity=0.8), row=2, col=1)
#
# fig_rasp4.add_trace(go.Scatter(
#                 x=data_mem_rasp4.index,
#                 y=list_mean_mem_disp_raps4,
#                 name="Memória livre/Memória total média",
#                 mode="lines",
#                 line_color='limegreen',
#                 opacity=0.8), row=2, col=1)
#
#
# fig_rasp4.update_layout(width=700, height=700, legend=dict(orientation="h"))
# fig_rasp4.layout.template = 'plotly_white'
#
#
# fig_rasp4.show()
#
#
# fig_rasp3 = make_subplots(rows=2, cols=1, subplot_titles=("(a) Uso de memória", "(b) Relação Memória Livre/Memória Total    "))
#
#
# fig_rasp3.add_trace(go.Scatter(
#                 x=data_mem_rasp3.index,
#                 y=data_mem_rasp3['memoria_disponivel'],
#                 name="Memória (MB)",
#                 mode="lines",
#                 line_color='red',
#                 opacity=0.8), row=1, col=1)
#
# fig_rasp3.add_trace(go.Scatter(
#                 x=data_mem_rasp3.index,
#                 y=mem_disp_rasp3_rel,
#                 name="Memória livre/Memória total",
#                 mode="lines",
#                 line_color='purple',
#                 opacity=0.8), row=2, col=1)
#
# fig_rasp3.add_trace(go.Scatter(
#                 x=data_mem_rasp3.index,
#                 y=list_mean_mem_disp_raps3,
#                 name="Memória livre/Memória total média",
#                 mode="lines",
#                 line_color='limegreen',
#                 opacity=0.8), row=2, col=1)
#
#
# fig_rasp3.update_layout(width=700, height=700, legend=dict(orientation="h"))
# fig_rasp3.layout.template = 'plotly_white'
#
#
# fig_rasp3.show()


# fig2 = go.Figure(data=[go.Histogram(x=mem_disp_rasp4_rel)])
#
# fig2.update_layout(
#     #title_text='Distribuição da Memória Disponível (%)', # title of plot
#     #xaxis_title_text='Percentual de Memória Disponível', # xaxis label
#     #yaxis_title_text='Frequencia', # yaxis label
#     bargap=0.01, # gap between bars of adjacent location coordinates
#     bargroupgap=0.01 # gap between bars of the same location coordinates
# )
# fig2.layout.template = 'plotly_white'
#
# fig2.show()

# fig3 = go.Figure(data=[go.Histogram(x=mem_disp_rasp3_rel, marker=dict(color='rgb(0, 0, 100)'))])
#
# fig3.update_layout(
#     #title_text='Distribuição da Memória Disponível (%)', # title of plot
#     #xaxis_title_text='Percentual de Memória Disponível', # xaxis label
#     #yaxis_title_text='Frequencia', # yaxis label
#     bargap=0.01, # gap between bars of adjacent location coordinates
#     bargroupgap=0.01 # gap between bars of the same location coordinates
# )
# fig3.layout.template = 'plotly_white'
#
# fig3.show()
#
#
# df =pd.DataFrame(dict(
#     equipamento=np.concatenate((["Raspberry Pi 3"]*len(mem_disp_rasp3_rel), ["Raspberry Pi 4"]*len(mem_disp_rasp4_rel))),
#     memoria=np.concatenate((mem_disp_rasp3_rel,mem_disp_rasp4_rel))
# ))
#
# print(df.head)
#
# #fig4= px.histogram(df, x="memoria", color="equipamento", barmode="overlay")
# fig4= px.histogram(df, x="memoria", color="equipamento", marginal="rug", hover_data=df.columns, labels={'memoria':'Memória Disponível (%)', 'count':'Frequencia'})
#
# fig4.update_layout(
#     #title_text='Distribuição da Memória Disponível (%)', # title of plot
#     #xaxis_title_text='Percentual de Memória Disponível', # xaxis label
#     #yaxis_title_text='Frequencia', # yaxis label
#     bargap=0.01, # gap between bars of adjacent location coordinates
#     bargroupgap=0.01 # gap between bars of the same location coordinates
# )
# fig4.layout.template = 'plotly_white'
#
# fig4.show()

fig5 = go.Figure()

fig5.add_trace(go.Histogram(
    x=mem_disp_rasp3_rel,
    histnorm='percent',
    name='Rasp 3', # name used in legend and hover labels
    xbins=dict( # bins used for histogram
        start=0,
        end=1,
        size=0.02
    ),
    marker_color='#EB89B5',
    opacity=0.75
))

fig5.add_trace(go.Histogram(
    x=mem_disp_rasp4_rel,
    histnorm='percent',
    name='Rasp 4',
    xbins=dict(
        start=-0,
        end=1,
        size=0.02
    ),
    marker_color='#330C73',
    opacity=0.75
))

fig5.update_layout(
    #title_text='Distribuição da Memória Disponível (%)', # title of plot
    #xaxis_title_text='Percentual de Memória Disponível', # xaxis label
    #yaxis_title_text='Frequencia', # yaxis label
    xaxis_title='Memória disponível (%)',
    yaxis_title='Frequência',
    legend=dict(
        x=0,
        y=0.9,
        traceorder='normal',),
    bargap=0.01, # gap between bars of adjacent location coordinates
    bargroupgap=0.01 # gap between bars of the same location coordinates
)
fig5.layout.template = 'plotly_white'

fig5.show()

# RASP 3

print('Uso máximo da memória - RASP3')
print(data_mem_rasp3.max())

print('Uso médio da memória - RASP3')
print(data_mem_rasp3.mean())

print('Uso mínimo da memória - RASP3')
print(data_mem_rasp3.min())

print('Uso mediano da memória - RASP3')
print(data_mem_rasp3.median())

# RASP 4

print('Uso máximo da memória - RASP4')
print(data_mem_rasp4.max())

print('Uso médio da memória - RASP4')
print(data_mem_rasp4.mean())

print('Uso mínimo da memória - RASP4')
print(data_mem_rasp4.min())

print('Uso mediano da memória - RASP4')
print(data_mem_rasp4.median())
