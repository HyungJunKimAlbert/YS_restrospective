import pandas as pd
import numpy as np
import datetime, random, warnings, tqdm
from datetime import timedelta
import datetime

nowDate = datetime.datetime.now() .strftime('%Y-%m-%d')
warnings.filterwarnings(action='ignore')


base_dir = 'C:/Users/User5/Desktop/github/YS_labelling/'
date = '220217/'
data_dir = base_dir + 'preprocessed_data/' + date
label_dir = base_dir + 'label/'

''' 옵션값 '''
n = 3
prediction_time = 3         # 몇시간 이내 이벤트를 예측할건지 ? 3hour
observation_time = 12       # 몇시간동안의 input data를 사용할건지 ? (최소 observation time만큼의 데이터가 있는 이벤트만 추출하도록 함.)
input_col = 'timestamp'
label_col = 'starttime'
random.seed(0)


''' patient info df ''' 
# 전향적 데이터 라벨결과에서 환자만 distinct하게 추출
pros_label = pd.read_csv(data_dir + 'multi_label_2022-01-28.csv', index_col=0)
pros_plist = list(set(pros_label['pat_id']))
# print('전향적 환자: ', len(pros_plist))

# 후향적 데이터 환자 info dataframe  >>>>  p_df 안에 stay_id, pat_id, intime, outtime, los 정보 있음
p_df = pd.read_csv(data_dir + 'icu_info.csv', encoding='cp949', index_col=0, parse_dates=['intime', 'outtime'])
p_df = p_df.drop_duplicates(['pat_id', 'intime', 'outtime'])
p_df = p_df[p_df['LOS']>0]
p_df['intime'] = pd.to_datetime(p_df['intime'])
p_df['outtime'] = pd.to_datetime(p_df['outtime'])
p_df = p_df[~p_df['pat_id'].isin(pros_plist)].reset_index(drop=True)   # 전향적 라벨링 환자가 아닌 경우만 p_df 에 포함
# p_df.to_csv('./icuinfo_2519.csv')

result = pd.DataFrame()

pid_list = []
rs_list = []


for idx in tqdm.tqdm(range(len(p_df))):
    pat_id = p_df['pat_id'][idx]
    los_days = int(p_df['LOS'][idx])
    intime = p_df['intime'][idx]
    outtime = p_df['outtime'][idx]
    
    los_length = int((outtime - intime).total_seconds() / 60 / 60)  # los 기간동안 1시간 단위 time-window 몇개인지 파악

    for los_idx in range(0, los_length):
        if los_idx == 0:
            ts_tmp = intime + timedelta(hours=1)
        else:
            ts_tmp = ts_tmp + timedelta(hours=1)

        pid_list.append(pat_id)
        rs_list.append(ts_tmp)
        


result['pat_id'] = pid_list
result['timestamp'] = rs_list

result.to_csv('./test.csv')

print(result)