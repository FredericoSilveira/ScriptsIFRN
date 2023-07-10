import numpy as np
import pandas as pd
import plotly as py

data_mem_rasp4 = pd.read_csv("/Users/fred/Downloads/memoria_rasp4_sem_docker_18_20_03_2020.csv", sep=';', index_col=0, parse_dates=True, infer_datetime_format=True)
data_mem_rasp3 = pd.read_csv("/Users/fred/Downloads/memoria_rasp3_sem_docker_14_16_03_2020.csv", sep=';', index_col=0, parse_dates=True, infer_datetime_format=True)
data_mem_rasp3= data_mem_rasp3.iloc[:,0:3]
data_mem_rasp4= data_mem_rasp4.iloc[:,0:3]

data_mem_rasp3.rename(columns={"Time": "tempo", "Available memory": "memoria_disponivel"},inplace=True)
data_mem_rasp4.rename(columns={"Time": "tempo", "Available memory": "memoria_disponivel"},inplace=True)

#RASP4
data_mem_rasp4['memoria_disponivel'] = data_mem_rasp4['memoria_disponivel']/1000000
#RASP3
data_mem_rasp3['memoria_disponivel'] = data_mem_rasp3['memoria_disponivel']/1000000

mem_disp_rasp3_rel = data_mem_rasp3['memoria_disponivel']/1000
mem_disp_rasp4_rel = data_mem_rasp4['memoria_disponivel']/4000

print(mem_disp_rasp4_rel)

mean_mem_disp_rasp3 = np.mean(mem_disp_rasp3_rel)
mean_mem_disp_rasp4 = np.mean(mem_disp_rasp4_rel)

#RASP3
print(mean_mem_disp_rasp3)
#RASP4
print(mean_mem_disp_rasp4)

num_rasp3 = len(data_mem_rasp3['memoria_disponivel'])
num_rasp4 = len(data_mem_rasp4['memoria_disponivel'])


list_mean_mem_disp_raps3 = num_rasp3 * [mean_mem_disp_rasp3]
list_mean_mem_disp_raps4 = num_rasp4 * [mean_mem_disp_rasp4]


df = pd.DataFrame(np.transpose([mem_disp_rasp3_rel,mem_disp_rasp4_rel]), columns=['rasp3','rasp4'])

print(df)

rasp3 = df.rasp3
rasp4 = df.rasp4

fig = df.iplot(kind='histogram', histnorm='percent', barmode='overlay', xTitle='Percentual de memória livre',
     vline=[dict(x=df.rasp3.mean(),color='#5283AD'), dict(x=df.rasp4.mean(),color='#FDAB5A')],
     asFigure=True)

py.offline.plot(fig)
