import pandas as pd
import numpy as np
import warnings
import datetime
import tqdm
from datetime import timedelta
warnings.filterwarnings('ignore')

base_dir = 'C:/Users/User5/Desktop/github/YS_labelling/'
date = '220217/'
data_dir = base_dir + 'preprocessed_data/' + date


''' import data '''
data_df = pd.read_csv(data_dir + 'total_result.csv', encoding='cp949', index_col=0, parse_dates=['charttime'])
data_df = data_df[['pat_id', 'study_id', 'charttime', 'value', 'item']]
icuinfo_df = pd.read_csv(data_dir + 'icu_info.csv', encoding='cp949', index_col=0, parse_dates=['intime', 'outtime'])
surg_df = pd.read_csv(data_dir + 'surg_result.csv', encoding='cp949', index_col=0, parse_dates=['starttime'])
surg_df = surg_df[['pat_id', 'study_id', 'starttime', 'ICD9']]
esrd_df = pd.read_csv(data_dir + 'esrd_result.csv', encoding='cp949', index_col=0, parse_dates=['diag_date'])

''' data_df DataFrame
# keys : ['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value','item']
# items ['pCO2', 'hemodialysis', 'potassium', 'Urineoutput', 'ventilator', 'pH', 'spo2', 'intubation', 'Creatinine', 'extubation', 'PF_ratio', 'pO2', 'BUN']
'''



# Respiratory Failure
''' Define each variables... '''
# spo2
spo2 = data_df[data_df['item']=='spo2'].iloc[:, :-1]
spo2 = spo2.rename(columns={'value':'spo2'})

# po2
po2 = data_df[data_df['item']=='pO2'].iloc[:, :-1]
po2 = po2.rename(columns={'value':'po2'})

# pco2
pco2 = data_df[data_df['item']=='pCO2'].iloc[:, :-1]
pco2 = pco2.rename(columns={'value':'pco2'})

# pf_ratio
pf_ratio = data_df[data_df['item']=='PF_ratio'].iloc[:, :-1]
pf_ratio = pf_ratio.rename(columns={'value':'pf_ratio'})

# Mechanical ventilator
mv = data_df[data_df['item'].isin(['intubation', 'ventilator'])].iloc[:, :-1]
mv['resp_failure'] = 1
mv = mv[['pat_id','study_id', 'charttime', 'resp_failure']].drop_duplicates().sort_values(['pat_id', 'charttime'])
mv = mv.groupby('pat_id').head(1).reset_index(drop=True)

# extubation
extubation = data_df[data_df['item'].isin(['extubation'])].iloc[:, :-1]
extubation = extubation.rename(columns={'value':'extubation'})

# MERGE All data
lab = pd.merge(po2, pco2, on=['pat_id','study_id', 'charttime'],how='outer')                                                 # pO2 + pCO2
lab = pd.merge(lab, pf_ratio, on=['pat_id','study_id', 'charttime'],how='outer')                                             # + PF_ratio
lab = pd.merge(lab, spo2, on=['pat_id','study_id', 'charttime'],how='outer')                                                 # + SpO2

data = lab.copy()
data = data.astype({'po2' : 'float', 'pco2' : 'float', 'pf_ratio' : 'float','spo2' : 'float'})  # type casting

data['criteria1'] = data.pf_ratio<=300
data['criteria2'] = data.po2<60
data['criteria3'] = data.pco2>45
data['criteria4'] = data.spo2<88
data['criteria_1to4'] = data.criteria1|data.criteria2|data.criteria3|data.criteria4

label_1to4 = data[data.criteria_1to4]

result = label_1to4[['pat_id', 'study_id', 'charttime']].copy()
result['resp_failure'] = 1
result = result.sort_values(['pat_id', 'charttime']).reset_index(drop=True)

# ICU 입실기간 내에 존재하는 이벤트만 filtering
filtered_result = pd.DataFrame()

for idx in tqdm.tqdm(range(len(result))):

    pid = result['pat_id'][idx]
    ch_time = result['charttime'][idx]

    # exbubation 시작~48시간 이내에 있는 이벤트는 -1로 라벨링하여 제외함.
    tmp_extubation = extubation[extubation['pat_id']==pid].sort_values(['charttime']).reset_index(drop=True)
    if len(tmp_extubation) > 0:
        for ex in range(len(tmp_extubation)):       
            st_ex = tmp_extubation['charttime'][ex]
            end_ex = st_ex + timedelta(hours=48)

            if (ch_time >= st_ex) & (ch_time <= end_ex):    # event 시점이 extubation~48 hours 내에 존재하면
                result['resp_failure'][idx] == -1

    tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)   # icustays.csv 내에 존재하는 pat_id 데이터 전부 조회

    # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회하여 이벤트 발생시각이 존재하는 경우 최종 라벨(filtered_result)에 추가함.
    for k in range(len(tmp)):
        intime = tmp['intime'][k]
        outtime = tmp['outtime'][k]

        if (ch_time >= intime) & (ch_time <= outtime):
            filtered_result = filtered_result.append(result.iloc[idx])

filtered_result = filtered_result[['pat_id', 'study_id', 'charttime', 'resp_failure']]

# Ventilator  : Total patients 467
# Ventil starttime 이 ICU intime 과 outtime 내에 있는 경우만 조회
filtered_mv = pd.DataFrame()
intime_list = []
outtime_list = []

for idx in tqdm.tqdm(range(len(mv))):
    pid = mv['pat_id'][idx]
    ch_time = mv['charttime'][idx]

    if len(tmp_extubation) > 0:
        for ex in range(len(tmp_extubation)):       
            st_ex = tmp_extubation['charttime'][ex]
            end_ex = st_ex + timedelta(hours=48)

            if (ch_time >= st_ex) & (ch_time <= end_ex):    # event 시점이 extubation~48 hours 내에 존재하면
                result['resp_failure'][idx] == -1

    tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)   # icustays.csv 내에 존재하는 pat_id 데이터 전부 조회

    # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회하여 이벤트 발생시각이 존재하는 경우 최종 라벨(filtered_result)에 추가함.
    for k in range(len(tmp)):
        intime = tmp['intime'][k]
        outtime = tmp['outtime'][k]

        if (ch_time >= intime) & (ch_time <= outtime):
            filtered_mv = filtered_mv.append(mv.iloc[idx])
            intime_list.append(intime)
            outtime_list.append(outtime)

filtered_mv['intime'] = intime_list
filtered_mv['outtime'] = outtime_list
filtered_mv = filtered_mv[['pat_id', 'study_id', 'charttime', 'intime', 'outtime', 'resp_failure']]

# Add MV onset time column
filtered_mv['onset_time'] = (filtered_mv.charttime - filtered_mv.intime).dt.total_seconds() // 60
filtered_mv = filtered_mv[['pat_id', 'study_id', 'charttime', 'resp_failure', 'onset_time']]

# # 입실 후 30분 이내 MV 착용한 환자
under_30 = filtered_mv[filtered_mv['onset_time'] <= 30]   ## under 30 minutes : 122 

# 수술시작 -3시간 ~ + 1시간 이전에 MV 착용한 환자
filtered_surg = pd.DataFrame()
intime_list = []
outtime_list = []

for idx in tqdm.tqdm(range(len(surg_df))):
    pid = surg_df['pat_id'][idx]
    ch_time = surg_df['starttime'][idx]
    # print('pid: ',  pid, 'charttime: ', ch_time)
    tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)   # icustays.csv 내에 존재하는 pat_id 데이터 전부 조회

    # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회하여 이벤트 발생시각이 존재하는 경우 최종 라벨(filtered_result)에 추가함.
    for k in range(len(tmp)):
        intime = tmp['intime'][k]
        outtime = tmp['outtime'][k]

        if (ch_time >= intime) & (ch_time <= outtime):
            filtered_surg = filtered_surg.append(surg_df.iloc[idx])
            intime_list.append(intime)
            outtime_list.append(outtime)

filtered_surg['intime'] = intime_list
filtered_surg['outtime'] = outtime_list

filtered_surg = filtered_surg[['pat_id', 'study_id', 'starttime', 'intime', 'outtime']]
mv_list = list(set(filtered_mv['pat_id']))  # ventilator 착용환자 리스트
surg_tmp = surg_df[surg_df['pat_id'].isin(mv_list)]

surg_tmp = pd.merge(filtered_mv, surg_tmp, on=['pat_id', 'study_id'])
surg_tmp['mv_for_surg'] = (surg_tmp.charttime >= (surg_tmp.starttime - timedelta(hours=3))) & (surg_tmp.charttime <= (surg_tmp.starttime + timedelta(hours=1)))
surg_patient = surg_tmp[surg_tmp.mv_for_surg]
print(surg_patient)


# exclude mv
exclude_1 = list(set(under_30['pat_id']))           # 입실 30분 이내 mv 착용환자
exclude_2 =  list(set(surg_patient['pat_id']))      # 입실기간동안 수술로 인한 mv 착용환자
mv_ex = filtered_mv[filtered_mv['pat_id'].isin(exclude_1 + exclude_2)]
mv_ex['resp_failure'] = -1

# final mv
mv = filtered_mv[~filtered_mv['pat_id'].isin(exclude_1 + exclude_2)]
mv_final = pd.concat([mv, mv_ex], axis=0)
mv_final = mv_final[['pat_id', 'study_id', 'charttime', 'resp_failure']]
print(mv_final)

# LAB  +  Mechanical Ventilator
filtered_result = pd.concat([filtered_result, mv_final], axis=0).drop_duplicates()
filtered_result.to_csv('./resp_failure.csv')






# RENAL Failure


