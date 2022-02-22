import pandas as pd
import numpy as np
import warnings
import datetime
import tqdm, re
from datetime import timedelta
warnings.filterwarnings('ignore')

base_dir = 'C:/Users/User5/Desktop/github/YS_labelling/'
date = '220217/'
data_dir = base_dir + 'preprocessed_data/' + date


''' import data '''
data_df = pd.read_csv(data_dir + 'total_result.csv', encoding='cp949', index_col=0, parse_dates=['charttime'])
data_df = data_df[['pat_id', 'study_id', 'charttime', 'value', 'item']]
icuinfo_df = pd.read_csv(data_dir + 'icu_info.csv', encoding='cp949', index_col=0, parse_dates=['intime', 'outtime'])



'''    Creatinine    ''' 
# Cr = data_df[data_df['item']=='Creatinine'].iloc[:, :-1].sort_values(by=['pat_id', 'charttime']).reset_index(drop=True)
# Cr = Cr.rename(columns={'value':'Cr'})

# Cr_total = Cr['pat_id']
# Cr_plist = []
# Cr_baseline = []
# filtered_cr = pd.DataFrame()

# for pid in tqdm.tqdm(Cr_total):

#     # pat_id 별 Cr 결과값 (여기서 for문 돌면서 intime-outtime 내에 있는지 확인하고, 기간내에 있는 값만 추출해서 평균값으로 계산)
#     cr_tmp = Cr[Cr['pat_id']==pid].reset_index(drop=True)   
#     icu_tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)
#     if len(cr_tmp) == 0:
#         cr_avg = np.nan

#     else:
#         cr_avg = []
#         for cr_idx in range(len(cr_tmp)):
#             # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회
#             ch_time = cr_tmp['charttime'][cr_idx]
#             value = cr_tmp['Cr'][cr_idx]

#             for k in range(len(icu_tmp)):
#                 intime = icu_tmp['intime'][k]
#                 outtime = icu_tmp['outtime'][k]

#                 if (ch_time >= intime) & (ch_time <= outtime):
#                     cr_avg.append(value)

#     Cr_plist.append(pid)
#     Cr_baseline.append(round(np.mean(cr_avg),3))

# filtered_cr['pat_id'] = Cr_plist
# filtered_cr['Cr_base'] = Cr_baseline
# filtered_cr = filtered_cr.drop_duplicates().reset_index(drop=True)
# filtered_cr.to_csv(data_dir + 'Cr_baseline.csv', encoding='cp949')
# print(filtered_cr)



'''    Urine output Criteria    ''' 

# Urine output
# uo = data_df[data_df['item']=='Urineoutput'].iloc[:, :-1].sort_values(by=['pat_id', 'charttime']).reset_index(drop=True)
# uo = uo.rename(columns={'value':'uo'})


# uo_criteria = pd.DataFrame()
# total_6hours = []

# for idx, row in tqdm.tqdm(uo.iterrows()):
# # for uo_idx in tqdm.tqdm(range(0,10)):
#     pid = uo['pat_id'][idx]
#     ch_time = uo['charttime'][idx]
#     after_6hour = ch_time + timedelta(hours=6) 

#     if re.sub(r'[^0-9]', '', uo['uo'][idx]) == '':
#         continue

#     else:
#         uo_tmp = uo[(uo['pat_id']==pid) & (uo['charttime'] >= ch_time) & (uo['charttime'] < after_6hour)]
#         tmp_list = [re.sub(r'[^0-9]', '', x) for x in list(uo_tmp['uo'])]
#         tmp_list = [int(x) for x in tmp_list if x != '']

#         if sum(tmp_list) < 180:
#             uo_criteria = uo_criteria.append(uo.iloc[idx])
#             total_6hours.append(sum(tmp_list))

# uo_criteria['total_6hours'] = total_6hours
# uo_criteria = uo_criteria.reset_index(drop=True)
# uo_criteria.to_csv(data_dir + 'uo_criteria.csv', encoding='cp949')
# print(uo_criteria)


''' Diaylsis    '''

# Dialysis
dialysis = data_df[data_df['item']=='hemodialysis'].iloc[:, :-1].reset_index(drop=True)
dialysis = dialysis.rename(columns={'value':'hemodialysis', 'charttime': 'starttime'})
dialysis = dialysis.sort_values(['pat_id', 'starttime'])
dialysis = dialysis.groupby('pat_id').head(1).reset_index(drop=True)
print(dialysis)

dialysis.to_csv(data_dir + 'dialysis.csv', encoding='cp949')

# ICU 기간 내에 있는 경우만 포함 
# filtered_dialysis = pd.DataFrame()

# for idx in tqdm.tqdm(range(len(dialysis))):
#     pid = dialysis['pat_id'][idx]
#     ch_time = dialysis['starttime'][idx]
#     # print('pid: ',  pid, 'charttime: ', ch_time)
#     tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)   # icustays.csv 내에 존재하는 pat_id 데이터 전부 조회

#     # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회하여 이벤트 발생시각이 존재하는 경우 최종 라벨(filtered_result)에 추가함.
#     for k in range(len(tmp)):
#         intime = tmp['intime'][k]
#         outtime = tmp['outtime'][k]

#         if (ch_time >= intime) & (ch_time <= outtime):
#             filtered_dialysis = filtered_dialysis.append(dialysis.iloc[idx])

# filtered_dialysis = filtered_dialysis.sort_values(['pat_id', 'starttime'])
# filtered_dialysis = filtered_dialysis.groupby('pat_id').head(1).reset_index(drop=True)
# filtered_dialysis.to_csv(data_dir + 'dialysis.csv', encoding='cp949')
# print(filtered_dialysis)
