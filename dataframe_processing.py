#import datetime
from datetime import datetime
import pandas as pd

# Input dataframe

df = pd.read_csv('/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-09-11-BOT-IOT-RASP4/original/Memory usage-data-as-seriestocolumns-2020-09-11 17_46_47.csv', delimiter=',')

# Set time range

# start_date = '2020-09-06 15:00:00'
# end_date = '2020-09-06 23:00:00'
#
# mask = (df['Time'] > start_date) & (df['Time'] <= end_date)
#
# df = df.loc[mask]


print(df.head())
print(df.tail())

df['Time'] = pd.to_datetime(df['Time'])

import datetime

df.Time = df.Time - datetime.timedelta(hours=4)


x = df.Time

df.Time = x.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

df.set_index('Time', inplace=True)

print(len(df))
#df = df.iloc[500:]
#
#df = df.iloc[:481]
#print(df.head())
print(df.tail())

df.to_csv('/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-09-11-BOT-IOT-RASP4/Memory usage-data-as-seriestocolumns-2020-09-11 17_46_47.csv', sep=',')