import matplotlib.pyplot as plt
import pandas as pd
import plotly.offline as pyo
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import chart_studio.plotly as py

pd.options.plotting.backend = "plotly"

#plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.size'] =  14



data_mem_rasp4 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-09-11-BOT-IOT-RASP4/Memory usage-data-as-seriestocolumns-2020-09-11 17_46_47.csv", sep=',')
data_mem_rasp3 = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-09-11-BOT-IOT-RASP3/original/Memory usage-data-as-seriestocolumns-2020-09-11 13_41_54.csv", sep=',')


data_mem_rasp3.columns=['Tempo', 'Memoria livre']
data_mem_rasp4.columns=['Tempo', 'Memoria livre']

df = data_mem_rasp3.copy()
df.columns = ['Tempo', 'Rasp3']
df['Rasp4'] = data_mem_rasp4['Memoria livre']
df['Tempo'] = pd.to_datetime(df['Tempo'])

df['Rasp3'] = df['Rasp3']/1000000
df['Rasp4'] = df['Rasp4']/1000000

df = df.set_index('Tempo')
df.dropna()
print(df)


fig = go.Figure()

fig.add_trace(go.Scatter(
                x=df.index.time,
                y=df.Rasp4,
                name="Memória Livre (MB) Rasp 4",
                mode="lines",
                line_color='green',
                opacity=0.8))

fig.add_trace(go.Scatter(
                x=df.index.time,
                y=df.Rasp3,
                name="Memória Livre (MB) Rasp 3",
                mode="lines",
                line_color='orange',
                opacity=0.8))

fig.update_layout(xaxis=dict(nticks=7), legend=dict(orientation="h"))
fig.layout.template = 'plotly_white'

fig.show()


