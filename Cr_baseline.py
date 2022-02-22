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



# Creatinine
Cr = data_df[data_df['item']=='Creatinine'].iloc[:, :-1].sort_values(by=['pat_id', 'charttime']).reset_index(drop=True)
Cr = Cr.rename(columns={'value':'Cr'})

Cr_total = Cr['pat_id']
Cr_plist = []
Cr_baseline = []
filtered_cr = pd.DataFrame()

for pid in tqdm.tqdm(Cr_total):

    # pat_id 별 Cr 결과값 (여기서 for문 돌면서 intime-outtime 내에 있는지 확인하고, 기간내에 있는 값만 추출해서 평균값으로 계산)
    cr_tmp = Cr[Cr['pat_id']==pid].reset_index(drop=True)   
    icu_tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)
    if len(cr_tmp) == 0:
        cr_avg = np.nan

    else:
        cr_avg = []
        for cr_idx in range(len(cr_tmp)):
            # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회
            ch_time = cr_tmp['charttime'][cr_idx]
            value = cr_tmp['Cr'][cr_idx]

            for k in range(len(icu_tmp)):
                intime = icu_tmp['intime'][k]
                outtime = icu_tmp['outtime'][k]

                if (ch_time >= intime) & (ch_time <= outtime):
                    cr_avg.append(value)

    Cr_plist.append(pid)
    Cr_baseline.append(round(np.mean(cr_avg),3))

filtered_cr['pat_id'] = Cr_plist
filtered_cr['Cr_base'] = Cr_baseline
filtered_cr = filtered_cr.drop_duplicates().reset_index(drop=True)
filtered_cr.to_csv(data_dir + 'Cr_baseline.csv', encoding='cp949')
print(filtered_cr)
