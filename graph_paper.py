import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv("/Users/fred/Downloads/dados.csv", sep=';', index_col=0, parse_dates=True, infer_datetime_format=True)
data = data.iloc[:,0:3]
print(data)

data.rename(columns={"Tempo": "tempo", "Attack": "attack","CPU user time": "cpu_user", "CPU system time": "cpu_system"},inplace=True)

#plt.plot(data.index, 'cpu_user', data=data, color='orange', marker='o', markersize=3)
#plt.plot(data.index, 'cpu_system', data=data, color='green', marker='o', markersize=3)

#plt.show()

fig = go.Figure()


fig.add_trace(go.Scatter(
                x=data.index,
                y=data['cpu_user'],
                name="cpu_user",
                line_color='orange',
                opacity=0.8))

fig.add_trace(go.Scatter(
                x=data.index,
                y=data['cpu_system'],
                name="cpu_system",
                line_color='green',
                opacity=0.8))


fig.update_layout(title_text="CPU Usage")
fig.layout.template = 'plotly_white'

# Use date string to set xaxis range
#fig.update_layout(xaxis_range=['2016-07-01','2016-12-31'],
#                  title_text="Manually Set Date Range")

#fig = px.line(data, x=data.index, y='cpu_user')
fig.show()

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
                x=data.index,
                y=data['attack'],
                name="Attack",
                line_color='red',
                opacity=0.8))

fig2.update_layout(title_text="Attacks")
fig2.layout.template = 'plotly_white'

fig2.show()