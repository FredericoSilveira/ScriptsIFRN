import argparse
import datetime
import glob
import sys
from datetime import datetime
# from influxdb import DataFrameClient
from os.path import isfile

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
from dateutil import tz


def input_validation():
    parser = argparse.ArgumentParser(description='Script to select feaures')
    parser.add_argument('-i', '--inputdir', help='Input Dir', required=True)
    parser.add_argument('-o', '--output', help='Output file', required=True)

    args = parser.parse_args()
    return args


def load_data(csv_file_path):
    return pd.read_csv(csv_file_path)


def load_classifications(log_path):
    header = ['log_time',
              'log_time_ms',
              'log_type',
              'log_level',
              'receive_time',
              'last_date_time',
              'flow_id',
              'src_host',
              'src_port',
              'dst_host',
              'dst_port',
              'protocol',
              'sampling_rate',
              'class_name',
              'prob_class',
              'prob_normal']

    files = glob.glob(log_path + '/class*.log*')
    result = None
    for f in files:
        if result is None:
            result = pd.read_csv(f, header=None, names=header)
        else:
            result = result.append(pd.read_csv(f, header=None, names=header))
    return result


def plot_barh(x, y, title, x_label, y_label, file_name):
    plt.rcParams['font.family'] = "Times New Roman"
    fig, ax = plt.subplots()
    width = 0.75  # the width of the bars
    ind = np.arange(len(y))  # the x locations for the groups
    ax.barh(ind, y, width)
    ax.set_yticks(ind + width / 2)
    ax.set_yticklabels(x, minor=False)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Wirite labels on bar top
    for i, v in enumerate(y):
        ax.text(v, i - 0.2, str(v), color='red', fontsize=8)

    plt.savefig(file_name, bbox_inches='tight')
    plt.gcf().clear()


def plot_boxplot(df, title, x_label, y_label, file_name):
    plt.rcParams['font.family'] = "Times New Roman"
    fig, ax = plt.subplots()
    data_plot = []
    for col in df.columns:
        data_plot.append(df[col])

    ax.boxplot(data_plot, labels=df.columns, showfliers=True, meanline=True, showmeans=True)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(file_name, bbox_inches='tight')
    plt.gcf().clear()
    # plt.show()


def plot_boxplot2(df, label_name, file_path='/Users/fred/PycharmProjects/smart-defender/data'):
    labels = list(df[label_name].unique())
    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.rcParams['font.family'] = "Times New Roman"
    for label in labels:
        data = df[df[label_name] == label]
        data = data[[var for var in list(data.columns) if var != label_name]]

        fig, ax = plt.subplots()
        data_plot = []
        for col in data.columns:
            data_plot.append(data[col])

        ax.boxplot(data_plot, labels=data.columns, showfliers=True, meanline=True, showmeans=True, vert=False)
        plt.title('Class = ' + label)
        # plt.xlabel(x_label)
        # plt.ylabel(data.columns)
        plt.savefig(file_path + '/' + 'boxplot_' + label + '.pdf', bbox_inches='tight')
        plt.gcf().clear()


def main():
    args = input_validation()
    if not isfile(args.dataset) \
            or len(args.inputdir) <= 0 \
            or len(args.output) <= 0:
        print('Error: You should inform the correct input parameters ')
        sys.exit(1)


def utc_timestamp_convert(list_datetime):
    from_zone = tz.tzlocal()
    to_zone = tz.tzutc()
    result = []
    for dt in list_datetime:
        t = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        local = t.replace(tzinfo=from_zone)
        utc = local.astimezone(to_zone)
        result.append(str(utc.timestamp()))

    return result


def extract_data_from_influx_db(host='localhost', port=8086):
    """Instantiate the connection to the InfluxDB client."""
    client = DataFrameClient('localhost', 8086, 'admin', 'lapps', 'smartdefender')
    measurements = client.get_list_measurements()
    df = None
    start_date_time = ['2018-11-01 00:00:00',
                       '2018-11-02 00:00:00',
                       '2018-11-03 00:00:00',
                       '2018-11-04 00:00:00',

                       '2018-11-05 00:00:00',
                       '2018-11-06 00:00:00',
                       '2018-11-07 00:00:00',
                       '2018-11-08 00:00:00',

                       '2018-11-09 00:00:00',
                       '2018-11-10 00:00:00',
                       '2018-11-11 00:00:00',
                       '2018-11-12 00:00:00'
                       ]

    end_date_time = ['2018-11-01 23:59:59',
                     '2018-11-02 23:59:59',
                     '2018-11-03 23:59:59',
                     '2018-11-04 23:59:59',

                     '2018-11-05 23:59:59',
                     '2018-11-06 23:59:59',
                     '2018-11-07 23:59:59',
                     '2018-11-08 23:59:59',

                     '2018-11-09 23:59:59',
                     '2018-11-10 23:59:59',
                     '2018-11-11 23:59:59',
                     '2018-11-12 23:59:59',
                     ]

    start_date_time = utc_timestamp_convert(start_date_time)
    end_date_time = utc_timestamp_convert(end_date_time)
    for i in range(len(start_date_time)):
        for m in measurements:
            measure = m['name']
            if measure in ['normal', 'http_flood', 'http_slow', 'tcp_flood', 'udp_flood']:
                q = 'SELECT * FROM ' + measure + ' WHERE time >= ' + start_date_time[i] \
                    + ' AND time <= ' + end_date_time[i]

                print('Reading [', measure, '] from: ', start_date_time[i], ' To: ', end_date_time[i])
                result = client.query(q)
                if len(result) > 0:
                    data = result[measure]
                    # print(result[measure].head())
                    if df is None:
                        print('First time')
                        print(measure)
                        df = result[measure]
                        df['label_class'] = [measure for x in range(df.shape[0])]
                        # df['date_time'] = df.index
                        # df = df.reset_index(0)
                    else:
                        print('Next time')
                        print(measure)
                        data['label_class'] = [measure for x in range(data.shape[0])]
                        print(df.shape, data.shape)
                        df = df.append(data, ignore_index=False, sort=False, )

    df.to_csv('extracted_data_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv')


def attack_detection(df_data, attack_plan):
    list_day_str = df_data['date'].unique()
    #print(list_day_str)
    result_df = None
    for day in list_day_str:
        for i in range(len(attack_plan)):
            block_size = df_data.loc['\'' + day + ' 00:01:00\'':'\'' + day + ' 23:58:00\'']['block_size'].unique()
            sampling_rate = df_data.loc['\'' + day + ' 00:01:00\'':'\'' + day + ' 23:58:00\'']['sampling_rate'].unique()
            df_tmp = df_data.loc[
                     '\'' + day + ' ' + attack_plan[i][0] + '\'':'\'' + day + ' ' + attack_plan[i][1] + '\''].copy()
            # print(df_tmp.columns)
            # print(df_tmp.src_host)
            # print(df_tmp.dst_host)
            # print(df_tmp.label_class)
            # print(df_tmp.date_time)
            print('Day:', day, 'BS:', block_size, 'SR:', sampling_rate)

            if df_tmp.shape[0] > 0:
                df_tmp = df_tmp[(df_tmp['src_host'].isin(attack_plan[i][2])) & (df_tmp['dst_host'] == attack_plan[i][3]) &
                                (df_tmp['label_class'] != 'normal')].copy()
                # print(df_tmp.src_host)
                # print(df_tmp.dst_host)
                # print(df_tmp.label_class)
                if df_tmp.shape[0] > 0:
                    if result_df is None:
                        result_df = pd.DataFrame({
                            'date': [day],
                            'block_size': block_size,
                            'sampling_rate': sampling_rate,
                            'is_attack': [1]})
                    else:
                        result_df = result_df.append(pd.DataFrame({
                            'date': [day],
                            'block_size': block_size,
                            'sampling_rate': sampling_rate,
                            'is_attack': [1]}))
                else:
                    if result_df is None:
                        result_df = pd.DataFrame({
                            'date': [day],
                            'block_size': block_size,
                            'sampling_rate': sampling_rate,
                            'is_attack': [0]})
                    else:
                        result_df = result_df.append(pd.DataFrame({
                            'date': [day],
                            'block_size': block_size,
                            'sampling_rate': sampling_rate,
                            'is_attack': [0]}))
            # print(result_df)
    return result_df


def metrics(df, attack_plan, attaker_hosts, target_hosts):

    tc = df.groupby(by=['date', 'block_size', 'sampling_rate']).agg({'value': 'sum'})
    tc.columns = ['tc']
    result = tc.copy()

    tp = df[((df['src_host'].isin(attaker_hosts)) &
             (df['dst_host'].isin(target_hosts))) &
            (df['label_class'] != 'normal')]
    tp = tp.groupby(by=['date', 'block_size', 'sampling_rate']).agg({'value': 'sum'})
    tp.columns = ['tp']
    result['tp'] = tp['tp']

    fp = df[((~df['src_host'].isin(attaker_hosts)) &
             (~df['dst_host'].isin(target_hosts)) &
             (~df['src_host'].isin(target_hosts))) &
            (df['label_class'] != 'normal')]
    # print('FP********************************************************************')
    # print(fp.date_time)
    # print(fp.src_host)
    # print(fp.dst_host)
    # print('FP********************************************************************')

    fp = fp.groupby(by=['date', 'block_size', 'sampling_rate']).agg({'value': 'sum'})

    fp.columns = ['fp']
    result['fp'] = fp['fp']

    fn = df[((df['src_host'].isin(attaker_hosts)) &
             (df['dst_host'].isin(target_hosts))) &
            (df['label_class'] == 'normal')]
    fn = fn.groupby(by=['date', 'block_size', 'sampling_rate']).agg({'value': 'sum'})
    fn.columns = ['fn']
    result['fn'] = fn['fn']

    tn = df[((~df['src_host'].isin(attaker_hosts)) &
             (~df['dst_host'].isin(target_hosts))) &
            (df['label_class'] == 'normal')]
    print('TN********************************************************************')
    print(tn.date_time)
    print(tn.src_host)
    print(tn.dst_host)
    print('TN********************************************************************')

    tn = tn.groupby(by=['date', 'block_size', 'sampling_rate']).agg({'value': 'sum'})
    tn.columns = ['tn']
    result['tn'] = tn['tn']
    result.fillna(0, inplace=True)
    #print('********************************************************************')
    #print('********************************************************************')
    #print(result['tn'])
    #print(result['tc'])
    #print(result['tp'])
    #print(result['fp'])
    #print(result['fn'])
    #print('********************************************************************')
    #print('********************************************************************')
    result['tn'] = result['tn'] + (result['tc'] -
                                   (result['tp']+
                                    result['fp']+
                                    result['tn']+
                                    result['fn']
                                    )
                                   )

    vr = df[((df['src_host'].isin(target_hosts)) &
             (df['dst_host'].isin(attaker_hosts))) &
            (df['label_class'] != 'normal')]
    vr = vr.groupby(by=['date', 'block_size', 'sampling_rate']).agg({'value': 'sum'})
    vr.columns = ['vr']
    result['vr'] = vr['vr']

    ad = attack_detection(df, attack_plan).groupby(by=['date', 'block_size', 'sampling_rate']).agg({'is_attack': 'sum'})
    ad.columns = ['ad']
    result['attack_detection'] = ad['ad']

    result.fillna(0, inplace=True)
    #result = result[1:result.shape[0]].copy()

    result['detection_rate'] = result['attack_detection'] / len(attack_plan)
    result['FAR'] = (result['fp']) / (result['fp'] + result['tn'])
    print('********************************************************************')
    print('********************************************************************')
    print(result['fp'])
    print(result['tn'])
    print('********************************************************************')
    print('********************************************************************')

    result['accuracy'] = (result['tp'] + result['tn']) / (result['tp'] + result['tn'] + result['fp'] + result['fn'])
    result['precision'] = (result['tp']) / (result['tp'] + result['fp'])
    result['recall'] = (result['tp']) / (result['tp'] + result['fn'])
    result['f1-score'] = 2 * ((result['precision'] * result['recall']) / (result['precision'] + result['recall']))
    result.fillna(0, inplace=True)

    return result

def plot_confusion_matrix(tp, fn, fp, tn, labels, output_filename):
    """Plot confusion matrix using heatmap.

    Args:
        data (list of list): List of lists with confusion matrix data.
        labels (list): Labels which will be plotted across x and y axis.
        output_filename (str): Path to output file.

    """
    seaborn.set(color_codes=True)
    #plt.figure(1, figsize=(18, 12))

    #plt.title("Matriz de Confusão")

    seaborn.set(font_scale=1.4)

    data = [[int(tp), int(fn)],
            [int(fp), int(tn)]]

    ax = seaborn.heatmap(data, annot=True, cmap="YlGnBu", fmt="d", cbar=False)

    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    ax.set(ylabel="Verdadeiro", xlabel="Previsto")

    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.close()


if __name__ == '__main__':
    # extract_data_from_influx_db()
    attack_plan = [('09:47:00', '10:13:00', ['172.16.0.1'], '192.168.10.50', 'attack'),
                        ('10:14:00', '10:42:00', ['172.16.0.1'], '192.168.10.50', 'attack'),

                        ('10:43:00', '11:09:00', ['172.16.0.1'], '192.168.10.50', 'attack'),
                        ('11:10:00', '11:33:00', ['172.16.0.1'], '192.168.10.50', 'attack'),

                        ('15:12:00', '15:42:00', ['172.16.0.10'], '192.168.10.51', 'attack')
                        ]

    target_hosts = ['192.168.10.50', '192.168.10.51']
    attacker_hosts = ['172.16.0.1']

    #df = pd.read_csv('/Users/salesfilho/PycharmProjects/smart-defender/data/logUFRN/extracted_data_2018-12-12.csv')
    #df = pd.read_csv('/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-08-25-RASP3/Overall traffic classifications-data-as-seriestocolumns-2020-08-26 09 38 43.csv', delimiter=',')
    df = pd.read_csv(
        '/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-09-09-ISCXIDS2017-RASP4/Overall traffic classifications-data-as-seriestocolumns-2020-09-09 19 15 50.csv',
        delimiter=',')
    df.rename(columns={'Time': 'date_time'}, inplace=True)

    print(df.columns)

    dfr = pd.DataFrame(columns=['date_time', 'sampling_rate', 'block_size', 'src_host', 'dst_host', 'label_class', 'value'])

    for col in df.columns:
        if col != 'date_time':
            cols = col.split()
            df_t = df[['date_time',col]].dropna()
            print(df_t)
            dx = pd.DataFrame({'date_time':df_t.date_time, 'sampling_rate': [20.0 for x in range(len(df_t))], 'block_size': [50 for x in range(len(df_t))], 'src_host': [cols[1].split('(')[1] for x in range(len(df_t))], 'dst_host': [cols[3].split(')')[0] for x in range(len(df_t))], 'label_class': [cols[0] for x in range(len(df_t))], 'value': df_t[col].values})
            dfr = dfr.append(dx)



    dfr.sort_index(inplace=True)

    dfr = dfr.groupby(
        by=['date_time', 'sampling_rate', 'block_size', 'src_host', 'dst_host', 'label_class']).agg(
        {'value': 'sum'})
    dfr.reset_index(inplace=True)
    dfr.set_index(pd.DatetimeIndex(dfr.date_time).floor('S'), inplace=True)
    #dfr.index = dfr.index.tz_convert('America/Recife')
    dfr['date'] = [str(x) for x in dfr.index.date]
    #df['sampling_rate'] = [int(100 / x) for x in df['sampling_rate']]

    df_result = metrics(dfr, attack_plan,attacker_hosts,target_hosts)
    #df_result = metrics(df, attack_plan_iscx,iscx_attaker_hosts,iscx_target_hosts)



day_of_experiments = ['2020-09-09',
                      ]

result = df_result.loc[day_of_experiments].copy()
result_plot = result.groupby( by=['block_size', 'sampling_rate']).agg('mean')
result_plot = result_plot[['recall', 'f1-score', 'detection_rate', 'precision', 'accuracy', 'FAR', 'attack_detection', 'tc', 'tp', 'fp', 'tn', 'fn']]
result_plot.columns = ['Recall', 'F1-Score', 'Detection Rate', 'Precision', 'Accuracy', 'FAR',
                       'Attack Detection', 'Total Classifications', 'True Positive', 'False Positive','True Negative', 'False Negative']
result_plot.index.names = ['Block Size', 'Sampling Rate']

plt.rcParams['font.family'] = "Times New Roman"
plt.rcParams.update({'font.size': 14})

result_plot[['Total Classifications', 'True Positive', 'False Positive', 'True Negative', 'False Negative']].plot(kind='bar')
result_plot[['Detection Rate']].sort_values(by=['Detection Rate']).plot(kind='barh').legend(ncol=1, fontsize=12)
result_plot[['FAR']].sort_values(by=['FAR']).plot(kind='barh').legend(ncol=1, fontsize=12)
result_plot[['F1-Score']].sort_values(by=['F1-Score']).plot(kind='barh').legend(ncol=1, fontsize=12)


#result_plot = result_plot[(result_plot['Detection Rate'] > 0.7) & (result_plot['F1-Score'] > 0.7)]
result_plot[['Detection Rate', 'Precision','F1-Score', 'FAR']].sort_values(by=['Detection Rate','Precision', 'F1-Score', 'FAR']).plot(kind='bar').legend(ncol=3, fontsize=11)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(result_plot[['Detection Rate', 'F1-Score', 'FAR', 'Precision', 'Recall']])
plt.savefig('/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/2020-08-23.pdf', bbox_inches='tight')
plt.gcf().clear()


labels = ['Ataque', 'Normal']

plot_confusion_matrix(result_plot['True Positive'].values[0], result_plot['False Negative'].values[0], result_plot['False Positive'].values[0], result_plot['True Negative'].values[0], labels, '/Users/fred/Documents/UFRN/projeto/Testes_Cenarios/matriz-2020--8-23.pdf')