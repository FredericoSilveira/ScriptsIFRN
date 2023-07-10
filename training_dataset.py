import os.path
import time

import pandas as pd
from joblib import dump
from sklearn.linear_model import LogisticRegression

#import joblib


start = time.time()

data = pd.read_csv("/usr/local/smartdetection-iot/smartdetection/modeldata/descritores_balanced_250_50.csv")
path = "/usr/local/smartdetection-iot/smartdetection/modeldata/"


features_col = ['ip_len_std', 'ip_len_entropy', 'ip_len_cv', 'ip_len_cvq', 'ip_len_rte', 'sport_rte', 'dport_cv',
                'dport_cvq', 'dport_rte', 'tcp_flags_mean', 'tcp_flags_median', 'tcp_flags_var', 'tcp_flags_std',
                'tcp_flags_cv', 'tcp_flags_cvq']

features = data[features_col]
label = data['Label2']

model = LogisticRegression(C=1, max_iter=1000, penalty='l2', solver='newton-cg')
model.fit(features, label)
filename = 'lr_250_50.sav'

with open(path + filename, 'wb') as f:
    dump(model, f)

raw_dump_duration = time.time() - start
print("Raw dump duration: %0.3fs" % raw_dump_duration)

raw_file_size = os.stat(path + filename).st_size / 1e6
print("Raw dump file size: %0.3fMB" % raw_file_size)
#dump(model, open(path + filename))
#joblib.dump(model, open(path + filename, 'wb'))

