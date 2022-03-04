import pandas as pd
import numpy as np
import warnings
import tqdm,re, datetime, warnings
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
cam_df = pd.read_csv(data_dir + 'camicu_result.csv', encoding='utf-8', index_col=0, parse_dates=['time'])

''' data_df DataFrame
# keys : ['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value','item']
# items ['pCO2', 'hemodialysis', 'potassium', 'Urineoutput', 'ventilator', 'pH', 'spo2', 'intubation', 'Creatinine', 'extubation', 'PF_ratio', 'pO2', 'BUN']
'''


def resp_failure():
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
    filtered_mv = filtered_mv[['pat_id', 'study_id', 'charttime', 'resp_failure', 'intime', 'outtime', 'onset_time']]

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

    # LAB  +  Mechanical Ventilator
    filtered_result = pd.concat([filtered_result, mv_final], axis=0).drop_duplicates().sort_values(by=['pat_id', 'charttime'])
    filtered_result = filtered_result.rename(columns={'charttime':'starttime'}).reset_index(drop=True)

    # 수술로 인한 Ventilator 인 경우 전부 -1로 & ICU 입실후 30분 이내에 MV 착용한 환자들의 입실 30분 이내 모든 라벨을 -1로 변경
    for idx in tqdm.tqdm(range(len(filtered_result))):
        pid = filtered_result['pat_id'][idx]
        ch_time = filtered_result['starttime'][idx]

        # print('pid: ',  pid, 'charttime: ', ch_time)
        tmp = under_30[under_30['pat_id']==pid].reset_index(drop=True)   # icustays.csv 내에 존재하는 pat_id 데이터 전부 조회
        if len(tmp) > 0:
            # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회하여 이벤트 발생시각이 존재하는 경우 최종 라벨(filtered_result)에 추가함.
            for k in range(len(tmp)):
                intime = tmp['intime'][k]
                intime_plus30 = intime + timedelta(minutes=30)

                if (ch_time >= intime) & (ch_time <= intime_plus30):
                    filtered_result['resp_failure'][idx] = -1
        else:
            continue

    

    filtered_result.to_csv('./resp_failure.csv')




# RENAL Failure
def renal_failure():
    ''' Define LAB variables... '''

    # Creatinine
    Cr = data_df[data_df['item']=='Creatinine'].iloc[:, :-1].sort_values(by=['pat_id', 'charttime']).reset_index(drop=True)
    Cr = Cr.rename(columns={'value':'Cr'})

    # CR baseline
    Cr_base = pd.read_csv(data_dir + 'Cr_baseline.csv', index_col=0, encoding='cp949')

    # pH
    pH = data_df[data_df['item']=='pH'].iloc[:, :-1].sort_values(by=['pat_id', 'charttime']).reset_index(drop=True)
    pH = pH.rename(columns={'value':'pH'})

    # BUN
    bun = data_df[data_df['item']=='bun'].iloc[:, :-1].sort_values(by=['pat_id', 'charttime']).reset_index(drop=True)
    bun = bun.rename(columns={'value':'bun'})

    # Potassium
    potassium = data_df[data_df['item']=='potassium'].iloc[:, :-1].sort_values(by=['pat_id', 'charttime']).reset_index(drop=True)
    potassium = potassium.rename(columns={'value':'potassium'})

    lab = pd.merge(Cr, pH, on=['pat_id','study_id', 'charttime'],how='outer')
    lab = pd.merge(lab, bun, on=['pat_id','study_id', 'charttime'],how='outer')
    lab = pd.merge(lab, potassium, on=['pat_id','study_id', 'charttime'],how='outer')

    data = lab.copy()

    # Add sCr baseline column
    sCr_list = []
    for idx in tqdm.tqdm(range(len(data))):
        pid = data['pat_id'][idx]
        
        cr_bs = Cr_base[Cr_base['pat_id']==pid]['Cr_base'].iloc[0]

        sCr_list.append(cr_bs)
    data['sCr'] = sCr_list


    # data = data.astype({'po2' : 'float', 'pco2' : 'float', 'pf_ratio' : 'float','spo2' : 'float'})  # type casting

    data['criteria_cr'] = data.Cr >= data.sCr*2
    data['criteria_po'] = data.potassium >= 6
    data['criteria_bun'] = data.bun > 60
    data['criteria_ph'] = data.pH < 7.2
    data['criteria_1to4'] = data.criteria_cr|data.criteria_po|data.criteria_bun|data.criteria_ph

    lab_criteria = data[data.criteria_1to4]
    lab_criteria = lab_criteria.iloc[:, :-5]

    '''  Urine output criteria  '''
    # Urine output Criteria (추출 코드는 Cr_baseline.py 내에 있음.)

    uo_criteria = pd.read_csv(data_dir + 'uo_criteria.csv', index_col=0, parse_dates=['charttime']).reset_index(drop=True)
    uo_criteria = uo_criteria.rename(columns={'charttime':'starttime'})

    final_criteria = pd.DataFrame() # Urine output + 앞뒤 x 시간 이내 랩조건 만족하는 경우

    for idx, value in tqdm.tqdm(uo_criteria.iterrows()):
        pid = uo_criteria['pat_id'][idx]
        ch_time = uo_criteria['starttime'][idx]    # Urine output 6시간동안 180 미만인 경우를 만족하는 경우임

        before_3h = ch_time - timedelta(hours=3)
        after_3h = ch_time + timedelta(hours=3)

        lab_tmp = lab_criteria[(lab_criteria['pat_id']==pid) & 
                                (lab_criteria['charttime'] >= before_3h) & 
                                (lab_criteria['charttime'] <= after_3h)]
        if len(lab_tmp) > 0:
            final_criteria = final_criteria.append(uo_criteria.iloc[idx])

    final_criteria = final_criteria.reset_index(drop=True)


    # ICU 입실기간내에 발생한 이벤트인지 Check
    filtered_rf = pd.DataFrame()
    intime_list = []
    outtime_list = []

    for idx in tqdm.tqdm(range(len(final_criteria))):
        pid = final_criteria['pat_id'][idx]
        ch_time = final_criteria['starttime'][idx]
        # print('pid: ',  pid, 'charttime: ', ch_time)
        tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)   # icustays.csv 내에 존재하는 pat_id 데이터 전부 조회

        # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회하여 이벤트 발생시각이 존재하는 경우 최종 라벨(filtered_result)에 추가함.
        for k in range(len(tmp)):
            intime = tmp['intime'][k]
            outtime = tmp['outtime'][k]

            if (ch_time >= intime) & (ch_time <= outtime):
                filtered_rf = filtered_rf.append(final_criteria.iloc[idx])
                intime_list.append(intime)
                outtime_list.append(outtime)

    # 조건 만족한 이벤트 첫시점만 추출
    filtered_rf = filtered_rf.sort_values(['pat_id', 'starttime'])
    filtered_rf['intime'] = intime_list
    filtered_rf = filtered_rf.groupby('pat_id').head(1).reset_index(drop=True)
    filtered_rf = filtered_rf[['pat_id', 'starttime', 'intime']]
    filtered_rf['renal_failure'] = 1

    # filtered_rf.to_csv('./renal_failure.csv', encoding='cp949')


    # Dialysis
    dialysis = data_df[data_df['item']=='hemodialysis'].iloc[:, :-1].reset_index(drop=True)
    dialysis = dialysis.rename(columns={'value':'hemodialysis', 'charttime': 'starttime'})
    dialysis = dialysis.sort_values(['pat_id', 'starttime'])
    dialysis = dialysis.groupby('pat_id').head(1).reset_index(drop=True)
    esrd_list = []

    for idx in tqdm.tqdm(range(len(filtered_rf))):
        pid = filtered_rf['pat_id'][idx]
        st_time = filtered_rf['starttime'][idx]
        in_time = filtered_rf['intime'][idx]
        tmp_dialysis = dialysis[dialysis['pat_id']==pid].reset_index(drop=True)

        if len(tmp_dialysis) == 0:
            continue    
        else:
            dialysis_time = tmp_dialysis['starttime'][0]

            if dialysis_time < in_time:
                filtered_rf['renal_failure'][idx] == -1
            elif dialysis_time < st_time:
                filtered_rf['starttime'][idx] = dialysis_time
            else:
                continue

        # ERSD + CKD 환자가 신부전 Starttime 이전에 진단받은 경우는 제외
        tmp_esrd = esrd_df[esrd_df['pat_id']==pid].sort_values(['pat_id', 'diag_date']).reset_index(drop=True)
        if len(tmp_esrd) > 0:
            diag_date = tmp_esrd['diag_date'][0]

            if diag_date < st_time: # esrd 진단시점이 renal failure 첫시점보다 이전인 경우 -1로 라벨링
                esrd_list.append(pid)
                filtered_rf['renal_failure'][idx] == -1

    filtered_rf.to_csv('./renal_failure.csv', encoding='cp949')
    print(len(esrd_list))



def delirium():

    # CAM Tatal patients : 2,335
    # Total 39,567
    cam_tmp = cam_df[['pid', 'time', 'rass', '1', '2', '3', '4']]
    cam_tmp = cam_tmp.rename(columns={'pid':'pat_id', 'time': 'starttime'})
    
    # Total 24,956 (Rass > -4)
    data_df = cam_tmp[cam_tmp['rass']>-4].copy().reset_index(drop=True)
    data_df['idx'] = range(0, len(data_df))

    # CAM-ICU Encoding (positive=1, Negative=0)
    cam_123_pos = data_df[(data_df['1'].str.slice(stop=2)=='양성') & (data_df['2'].str.slice(stop=2)=='양성') & (data_df['3'].str.slice(stop=2)=='양성')].copy()
    cam_124_pos = data_df[(data_df['1'].str.slice(stop=2)=='양성') & (data_df['2'].str.slice(stop=2)=='양성') & (data_df['4'].str.slice(stop=2)=='양성')].copy()
    cam_124_neg = data_df[(data_df['1'].str.slice(stop=2)=='음성') | (data_df['2'].str.slice(stop=2)=='음성') | (data_df['4'].str.slice(stop=2)=='음성')].copy()

    # Pos : 10,371
    case = pd.concat([cam_123_pos,cam_124_pos], axis=0).drop_duplicates()   # 특성 1,2,3,4가 모두 양성인 경우가 있어서 중복되는 경우가 발생함. (2072건)
    case = case[['pat_id', 'starttime', 'idx']]
    case['delirium'] = 1

    # Neg : 11,722
    control = cam_124_neg
    control = control[['pat_id', 'starttime', 'idx']]
    control = control[~control['idx'].isin(case['idx'])]    # 일부 환자에서 특성 1,2,3 에서 양성인데, 특성 4에서 음성인 경우가 있어서 이 경우 control에서 제외해야 함. (170건)
    control['delirium'] = 0

    # Total 22,093
    final_result = pd.concat([case, control], axis=0)
#     final_result.to_csv('./test.csv')

    final_result = final_result[['pat_id', 'starttime', 'delirium']].reset_index(drop=True)

    # ICU 입실기간내에 발생한 이벤트인지 Check
    filtered_delirium= pd.DataFrame()
    intime_list = []
    outtime_list = []

    for idx in tqdm.tqdm(range(len(final_result))):
        pid = final_result['pat_id'][idx]
        ch_time = final_result['starttime'][idx]
        # print('pid: ',  pid, 'charttime: ', ch_time)
        tmp = icuinfo_df[icuinfo_df['pat_id']==pid].reset_index(drop=True)   # icustays.csv 내에 존재하는 pat_id 데이터 전부 조회

        # 1개의 pat_id 에 여러 icu 입실기간이 있으므로, 모든 icu 입실기간의 intime & outtime 조회하여 이벤트 발생시각이 존재하는 경우 최종 라벨(filtered_result)에 추가함.
        for k in range(len(tmp)):
            intime = tmp['intime'][k]
            outtime = tmp['outtime'][k]

            if (ch_time >= intime) & (ch_time <= outtime):
                filtered_delirium = filtered_delirium.append(final_result.iloc[idx])
                intime_list.append(intime)
                outtime_list.append(outtime)


    filtered_delirium.to_csv('./delirium.csv', encoding='cp949')

resp_failure()
# renal_failure()
# delirium()    
