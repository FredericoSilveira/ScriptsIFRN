import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = pd.read_csv("/Users/fred/Downloads/dados.csv", sep=';', index_col=0, parse_dates=True, infer_datetime_format=True)
data = data.iloc[:,0:3]
print(data)

data.rename(columns={"Tempo": "tempo", "Attack": "attack","CPU user time": "cpu_user", "CPU system time": "cpu_system"},inplace=True)

mask = (data.index >= '2019-07-17 00:00:00-03:00') & (data.index <= '2019-07-17 12:00:00-03:00')

data = data.loc[mask]

#plt.plot(data.index, 'cpu_user', data=data, color='orange', marker='o', markersize=3)
#plt.plot(data.index, 'cpu_system', data=data, color='green', marker='o', markersize=3)

#plt.show()

fig = make_subplots(rows=2, cols=1, subplot_titles=("(a) CPU Usage", "(b) Attack Detection"))

#fig.add_scatter(x=data.index, y=data['cpu_user'], mode="lines",
#                marker=dict(color="Orange"),
#                name="a", row=1, col=1)

fig.add_trace(go.Scatter(
                x=data.index,
                y=data['cpu_user'],
                name="User CPU",
                mode="lines",
                line_color='orange',
                opacity=0.8), row=1, col=1)

fig.add_trace(go.Scatter(
                x=data.index,
                y=data['cpu_system'],
                name="System CPU",
                mode="lines",
                line_color='green',
                opacity=0.8), row=1, col=1)

fig.add_trace(go.Scatter(
                x=data.index,
                y=data['attack'],
                name="Attacks",
                mode="lines",
                line_color='red',
                opacity=0.8), row=2, col=1)


fig.update_layout(width=700, height=700, legend=dict(orientation="h"))
fig.layout.template = 'plotly_white'

# Use date string to set xaxis range
#fig.update_layout(xaxis_range=['2016-07-01','2016-12-31'],
#                  title_text="Manually Set Date Range")

#fig = px.line(data, x=data.index, y='cpu_user')
#xaxis_range=['2019-07-17 00:00:00-03:00','2019-07-17 12:00:00-03:00'],

fig.show()

