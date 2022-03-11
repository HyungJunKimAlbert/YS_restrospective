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
p_df.to_csv('./icuinfo_2519.csv')

'''    label data input   '''
# 이벤트 존재하는 경우만 질환별로 분리해서 df에 저장 (입실 후 12시간 이내 이벤트는 제외한 경우)
# delirium_df = pd.read_csv(label_dir + 'filtered_delirium.csv', index_col=0).reset_index(drop=True)
# renal_failure_df = pd.read_csv(label_dir + 'filtered_renal_failure.csv', index_col=0).reset_index(drop=True)
# resp_failure_df = pd.read_csv(label_dir + 'filtered_resp_failure.csv', index_col=0).reset_index(drop=True)

# 이벤트 존재하는 경우만 질환별로 분리해서 df에 저장
delirium_df = pd.read_csv(label_dir + 'delirium.csv', index_col=0).reset_index(drop=True)
renal_failure_df = pd.read_csv(label_dir + 'renal_failure.csv', index_col=0).reset_index(drop=True)
resp_failure_df = pd.read_csv(label_dir + 'resp_failure.csv', index_col=0).reset_index(drop=True)

delirium_df = delirium_df[['pat_id',  'starttime', 'delirium']]
renal_failure_df = renal_failure_df[['pat_id', 'starttime', 'renal_failure']]
resp_failure_df = resp_failure_df[['pat_id', 'starttime', 'resp_failure']]

# convert datetime type
delirium_df['starttime'] = pd.to_datetime(delirium_df['starttime'])
renal_failure_df['starttime'] = pd.to_datetime(renal_failure_df['starttime'])
resp_failure_df['starttime'] = pd.to_datetime(resp_failure_df['starttime'])


# *** 여기에 후향적 데이터 환자 전부 넣고, 전향적 환자 id 전부 제외
# ***   이벤트 발생시각이 ICU intime 에서 12시간 이후인 이벤트만 포함
# patients = set(list(delirium_df['pat_id']) + list(renal_failure_df['pat_id']) + list(resp_failure_df['pat_id']))        
patients = list(set(p_df['pat_id']))

# 전향적 라벨링 환자 제외한, 후향적 데이터 전체 환자 (event 없는 환자도 포함되어 있음.)
print('Total pat_ids: ', len(patients))

# 환자별로 LOS 기간내 하루 1개씩 random sampling
pid_list = []
rs_list = []

for idx in range(len(p_df)):
    pat_id = p_df['pat_id'][idx]
    los_days = int(p_df['LOS'][idx])
    intime = p_df['intime'][idx]
    outtime = p_df['outtime'][idx]
    

    for c in range(0, los_days):
        
        if c == 0:
            st_time = intime + timedelta(hours=12)  # intime 기준 12시간 이후부터 시작
            ran_min = random.randint(1,1440)

        elif c == los_days-1:
            st_time = st_time + timedelta(hours=24)  # intime 기준 12시간 이후부터 시작
            interval_min = ((outtime - st_time).total_seconds() // 60)
            ran_min = random.randint(1,interval_min)        

        else:
            st_time = st_time + timedelta(hours=24) # LOS 하루마다 24시간씩 추가
            ran_min = random.randint(1,1440)
            
        rs_timestamp = st_time + timedelta(minutes=ran_min)
        
        pid_list.append(pat_id)
        rs_list.append(rs_timestamp)
        
los_rs = pd.DataFrame()
los_rs['pat_id'] = pid_list
los_rs['timestamp'] = rs_list
los_rs.to_csv(label_dir + 'sampling_1days.csv')


# event 발생한 경우로만 random-sampling
l = []
for i in [delirium_df, renal_failure_df, resp_failure_df]:
    i.dropna(inplace=True)
    # print(i.loc[i.icustay_id.isnull()])
    a = i.pat_id.astype(int).values
    l.extend(a)

patients = set(l)

print('이벤트발생 patients: ' , len(patients))

id_total, timestamps_total = [], []

for i in tqdm.tqdm(patients):
    # if c > 10: break
    # c+=1
    # print(i)

    for j in [delirium_df, renal_failure_df, resp_failure_df]:
    # for j in [resp_failure_df]:
        origin_timestamps = []
        target_timestamps = []
        timestamps = j.loc[j.pat_id==i].iloc[:,1].array
        
        if len(timestamps) == 0: 
            # print('no label')
            continue

        origin_timestamps.extend(timestamps)
    
        # origin_timestamps = 모든 이벤트 발생시각 list
        for k in origin_timestamps:
            # time = datetime.datetime.strptime(k, '%Y-%m-%d %H:%M')
            time = k

            # sample_n 갯수만큼 3시간 이내 random시점 추출 (1~10800 초 내에서 난수 추출)
            for sn in range(n):  # 3개 시점만 1시간 단위로 랜덤하게 추출 (너무 많이하면 시점이 몰림...)  # 10,800 seconds = 3hour
                if sn == 0: # 0~60 분 내에서 랜덤하게 난수 추출되도록 제한
                    ransec = random.randint(1,60)
                if sn == 1: # 60~120 분 내에서 랜덤하게 난수 추출되도록 제한
                    ransec = random.randint(60,120)
                if sn == 2: # 120~180 분 내에서 랜덤하게 난수 추출되도록 제한
                    ransec = random.randint(120,180)                
                target_time = time - timedelta(minutes=ransec)
                target_timestamps.append(target_time)

        id_iter = [i for x in range(0,len(target_timestamps))]

        id_total.extend(id_iter)
        timestamps_total.extend(target_timestamps)

random_ts_df = pd.DataFrame(zip(id_total, timestamps_total), columns=['pat_id', 'timestamp'])
random_ts_df = random_ts_df.drop_duplicates().reset_index(drop=True)
random_ts_df.sort_values(by=['pat_id', 'timestamp'])
random_ts_df = random_ts_df.reset_index(drop=True)
random_ts_df.to_csv(label_dir + 'random_timestamp.csv')

result = pd.concat([random_ts_df, los_rs], axis=0)
result.sort_values(['pat_id', 'timestamp'], ascending=False)
result.reset_index(inplace=True, drop=True)

input_data = result

for labeling_df in [delirium_df, renal_failure_df, resp_failure_df]:
    disease_name = list(labeling_df.keys())[-1]
    labeling_df.dropna(inplace=True)

    print(disease_name)
    if disease_name == 'delirium':
        tmp_list = [-1]*len(input_data)

        for i_id in tqdm.tqdm(range(len(input_data))):
            input_id = int(input_data.pat_id[i_id])
            # input_id = str(input_id)[:-2]
            
            try:
                input_id = int(input_id)
            except:
                continue
            charttime = input_data[input_col][i_id]
            if type(charttime) == str:
                charttime = datetime.datetime.strptime(charttime, '%Y-%m-%d %H:%M:%S')
            else:
                pass
            is_sameid = labeling_df.pat_id == input_id
            is_sameid_valuecount = is_sameid.value_counts()

            if is_sameid_valuecount.values[0] == len(input_data):
                continue        
            else:
                del_check_list = []
                is_sameid_df = pd.DataFrame()
                is_sameid_df = labeling_df[is_sameid]
                tmp1 = is_sameid_df.loc[(is_sameid_df[label_col] > charttime) & (is_sameid_df[label_col] < charttime + timedelta(hours=prediction_time))]
                tmp1 = tmp1.reset_index()
                
            for t_k in range(len(tmp1)):

                label_id = tmp1.pat_id[t_k]
                labeling_time = tmp1[label_col][t_k]

                td = labeling_time - charttime
                td = td.total_seconds() / 60.0   
                del_check_list.append(tmp1[disease_name][t_k])

                if input_id == label_id:
                    if td > 0 and td < 60 * prediction_time:
                        if sum(del_check_list) > 0:
                            tmp_list[i_id] = 1
                        else:
                            tmp_list[i_id]= 0                                        
                        continue
                else:
                    continue   

    else:
        tmp_list = [0]*len(input_data)

        for i_id in tqdm.tqdm(range(len(input_data))):
            input_id = int(input_data.pat_id[i_id])

            try:
                input_id = int(input_id)
            except:
                continue
            charttime = input_data[input_col][i_id]
            if type(charttime) == str:
                charttime = datetime.datetime.strptime(charttime, '%Y-%m-%d %H:%M:%S')
            else:
                pass
            is_sameid = labeling_df.pat_id == input_id
            is_sameid_valuecount = is_sameid.value_counts()

            if is_sameid_valuecount.values[0] == len(input_data):
                continue        
            else:
                is_sameid_df = pd.DataFrame()
                is_sameid_df = labeling_df[is_sameid]
                is_sameid_df = is_sameid_df.reset_index()

            for t_k in range(len(is_sameid_df)):
                label_id = is_sameid_df.pat_id[t_k]
                labeling_time = is_sameid_df[label_col][t_k]
                label_value = is_sameid_df[disease_name][t_k]

                td = labeling_time - charttime
                td = td.total_seconds() / 60.0   

                if input_id == label_id:
                    if td > 0 and td < 60 * prediction_time:                                        
                        tmp_list[i_id] = label_value
                        continue
                else:
                    continue

    input_data[disease_name] = tmp_list

input_data.to_csv(label_dir + 'multi_label.csv')
