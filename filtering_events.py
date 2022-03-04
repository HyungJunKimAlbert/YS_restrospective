import pandas as pd
import numpy as np
import warnings
import tqdm,re, datetime, warnings
from datetime import timedelta
warnings.filterwarnings('ignore')

base_dir = 'C:/Users/User5/Desktop/github/YS_labelling/'
date = '220217/'
data_dir = base_dir + 'preprocessed_data/' + date
label_dir = base_dir + 'label/'





# LOS 12시간 이상인 이벤트만 추출

# icu information
icuinfo_df = pd.read_csv(data_dir + 'icu_info_over12h.csv', index_col=0)

# label data
delirium_df = pd.read_csv(label_dir + 'delirium.csv', index_col=0).reset_index(drop=True)
renal_df = pd.read_csv(label_dir + 'renal_failure.csv', index_col=0).reset_index(drop=True)
resp_df = pd.read_csv(label_dir + 'resp_failure.csv', index_col=0).reset_index(drop=True)


filtered_delirium = pd.DataFrame()

for idx in tqdm.tqdm(range(len(delirium_df))):
    pid = delirium_df['pat_id'][idx]
    ch_time = delirium_df['starttime'][idx]
    # print('pid: ',  pid, 'charttime: ', ch_time)
    tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)   # icustays.csv 내에 존재하는 pat_id 데이터 전부 조회

    # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회하여 이벤트 발생시각이 존재하는 경우 최종 라벨(filtered_result)에 추가함.
    for k in range(len(tmp)):
        intime = tmp['intime'][k]
        outtime = tmp['outtime'][k]

        if (ch_time >= intime) & (ch_time <= outtime):
            filtered_delirium = filtered_delirium.append(delirium_df.iloc[idx])



filtered_renal = pd.DataFrame()

for idx in tqdm.tqdm(range(len(renal_df))):
    pid = renal_df['pat_id'][idx]
    ch_time = renal_df['starttime'][idx]
    # print('pid: ',  pid, 'charttime: ', ch_time)
    tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)   # icustays.csv 내에 존재하는 pat_id 데이터 전부 조회

    # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회하여 이벤트 발생시각이 존재하는 경우 최종 라벨(filtered_result)에 추가함.
    for k in range(len(tmp)):
        intime = tmp['intime'][k]
        outtime = tmp['outtime'][k]

        if (ch_time >= intime) & (ch_time <= outtime):
            filtered_renal = filtered_renal.append(renal_df.iloc[idx])


filtered_resp = pd.DataFrame()

for idx in tqdm.tqdm(range(len(resp_df))):
    pid = resp_df['pat_id'][idx]
    ch_time = resp_df['starttime'][idx]
    # print('pid: ',  pid, 'charttime: ', ch_time)
    tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)   # icustays.csv 내에 존재하는 pat_id 데이터 전부 조회

    # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회하여 이벤트 발생시각이 존재하는 경우 최종 라벨(filtered_result)에 추가함.
    for k in range(len(tmp)):
        intime = tmp['intime'][k]
        outtime = tmp['outtime'][k]

        if (ch_time >= intime) & (ch_time <= outtime):
            filtered_resp = filtered_resp.append(resp_df.iloc[idx])








filtered_delirium.to_csv('./filtered_delirium.csv')
filtered_renal.to_csv('./filtered_renal_failure.csv')
filtered_resp.to_csv('./filtered_resp_failure.csv')