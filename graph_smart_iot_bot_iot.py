import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data_attack = pd.read_csv("/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/Experimentos_dataset_iot/Alertas de ataque-data-as-seriestocolumns-2020-08-20 16_42_43.csv", sep=',', index_col=0, parse_dates=True, infer_datetime_format=True)
data_attack = data_attack.iloc[:,0:3]
data_attack0 = data_attack.fillna(0)
print(data_attack)
print(data_attack0)

data_attack.rename(columns={"Time": "tempo", "attack": "ataque"},inplace=True)

mask = (data_attack.index > '2020-08-20 00:00:00') & (data_attack.index <= '2020-08-20 23:59:59')

data_attack = data_attack.loc[mask]

mask = (data_attack.index > '2020-08-20 00:00:00') & (data_attack.index <= '2020-08-20 23:59:59')

data_attack0 = data_attack0.loc[mask]


fig = make_subplots(rows=1, cols=1, subplot_titles=("Ataques detectados"))

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
        ), row=1, col=1)

data_attack.dropna(inplace=True)

fig.add_trace(go.Scatter(
                x=data_attack.index,
                y=data_attack['ataque'],
                name="Ataques",
                mode="markers",
                line_color='red',
                #fill='tonexty',
                opacity=0.8), row=1, col=1)


fig.update_layout(width=700, height=350, legend=dict(orientation="h"))
fig.layout.template = 'plotly_white'

fig.show()

