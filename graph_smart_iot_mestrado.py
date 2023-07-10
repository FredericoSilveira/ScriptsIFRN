import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data_wlan_eth = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/Experimentos_Smart-iot/wlan0 In x Eth0 Out-data-as-seriestocolumns-2020-08-20 00_38_36.csv", sep=',', index_col=0, parse_dates=True, infer_datetime_format=True)
data_wlan_eth = data_wlan_eth.iloc[:,0:3]

data_wlan_eth.rename(columns={"Time": "tempo", "Interface wlan0: Inbound packets": "entrada_pacotes_wlan0", "Interface eth0: Outbound packets": "saida_pacotes_eth0"},inplace=True)
print(data_wlan_eth)

mask = (data_wlan_eth.index > '2020-08-19 23:53:01') & (data_wlan_eth.index <= '2020-08-20 00:35:00')

data_wlan_eth = data_wlan_eth.loc[mask]

data_attack = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/Experimentos_Smart-iot/Alertas de ataque-data-as-seriestocolumns-2020-08-20 00_38_56.csv", sep=',', index_col=0, parse_dates=True, infer_datetime_format=True)
data_attack = data_attack.iloc[:,0:3]
data_attack0 = data_attack.fillna(0)
print(data_attack)
print(data_attack0)

data_attack.rename(columns={"Time": "tempo", "attack": "ataque"},inplace=True)

mask = (data_attack.index > '2020-08-19 23:53:01') & (data_attack.index <= '2020-08-20 00:35:00')

data_attack = data_attack.loc[mask]

mask = (data_attack0.index > '2020-08-19 23:53:01') & (data_attack0.index <= '2020-08-20 00:35:00')

data_attack0 = data_attack0.loc[mask]

# wo = data_wlan_eth.index[~data_wlan_eth.index.isin(data_attack.index)].dropna()
# wo0 = data_wlan_eth.index[~data_wlan_eth.index.isin(data_attack0.index)].dropna()
#
# data_attack = data_attack.reindex(wo,fill_value=0)
# data_attack0 = data_attack0.reindex(wo0,fill_value=0)


fig = make_subplots(rows=2, cols=1)
#fig = make_subplots(rows=2, cols=1, subplot_titles=("(a) Pacotes por segundo - wlan0 x eth0", "(b) Ataques"))


fig.add_trace(go.Scatter(
                x=data_wlan_eth.index,
                y=data_wlan_eth['entrada_pacotes_wlan0'],
                name="PPS wlan0",
                mode="lines",
                line_color='orange',
                #fill='tonexty',
                opacity=0.8), row=1, col=1)

fig.add_trace(go.Scatter(
                x=data_wlan_eth.index,
                y=data_wlan_eth['saida_pacotes_eth0'],
                name="PPS eth0",
                mode="lines",
                line_color='green',
                #fill='tozeroy',
                opacity=0.8), row=1, col=1)


for index, row in data_wlan_eth.iterrows():

    fig.add_shape(
        type="line",
        x0=index,
        y0=0,
        x1=index,
        y1=row['saida_pacotes_eth0'],
        opacity=0.6,
        line=dict(
            color="LightGreen",
            width=1,
            dash="dot",
        ), row=1, col=1)

for index, row in data_wlan_eth.iterrows():

    fig.add_shape(
        type="line",
        x0=index,
        y0=0,
        x1=index,
        y1=row['entrada_pacotes_wlan0'],
        opacity=0.6,
        line=dict(
            color="orange",
            width=1,
            dash="dot",
        ), row=1, col=1)


for indexat, rowat in data_attack0.iterrows():
    print(indexat, rowat)

    fig.add_shape(
        type="line",
        x0=indexat,
        y0=0,
        x1=indexat,
        y1=rowat['attack'],
        opacity=1.0,
        line=dict(
            color="red",
            width=2,
        ), row=2, col=1)

data_attack.dropna(inplace=True)

fig.add_trace(go.Scatter(
                x=data_attack.index,
                y=data_attack['ataque'],
                name="Ataques",
                mode="markers",
                line_color='red',
                #fill='tonexty',
                opacity=0.8), row=2, col=1)


# fig.add_trace(go.Scatter(
#                 x=data_attack.index,
#                 y=data_attack['ataque'],
#                 name="Ataques",
#                 mode="lines",
#                 line_color='red',
#                 #fill='tonexty',
#                 opacity=0.8), row=2, col=1)

fig.update_xaxes(nticks=9, type='date', tickformat='%H:%M', title_text="Tempo real", row=1, col=1)
fig.update_yaxes(title_text="Pacotes por segundo (PPS)", row=1, col=1)
fig.update_xaxes(nticks=9, type='date', tickformat='%H:%M', title_text="Tempo real", row=2, col=1)
fig.update_yaxes(title_text="Q. de Classificações", row=2, col=1)
#fig.update_layout(width=840, height=420, legend=dict(orientation="h"))
fig.update_layout(legend=dict(orientation="h"))
fig.layout.template = 'plotly_white'

fig.show()

