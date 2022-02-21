import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


''' Table mapping
icustays = 환자 입실정보, lab=검사결과,   lab2=검사결과2,     labtime=검사결과채혈시간,   diagnosis=상병,     drugtime=약주사시행,   
observation=임상관찰,   prescription=처방,      surgery=수술
'''



# 전체 환자수 조회 (Total patientid : 2558)
# plist1 = list(set(lab_df['real']))
# plist2 = list(set(lab2_df['real']))
# plist3 = list(set(labtime_df['real']))
# plist4 = list(set(diagnosis_df['real']))
# plist5 = list(set(drugtime_df['real']))
# plist6 = list(set(observation_df['real']))
# plist7 = list(set(prescription_df['real']))
# plist8 = list(set(surgery_df['real']))

# final_plist = list(set(plist1 + plist2 + plist3 + plist4 + plist5 + plist6 + plist7))

# print(len(final_plist))




# 아래 코드는 필요한 변수만 추출하는 코드

''' Columns...

- icustays.csv : 지역병원코드, 지역병원코드(코드명), 연구내원번호, 연구등록번호, 전입일자, 전입일시, 전입시간, 전출일자, 전출일시, 전출시간, 원병원코드, 병동
                병동(코드명), 병실, 병상, 현재환자위치, 이중점유병동, 이중점유병실, 이중점유병상, 작업코드, 작업코드(코드명), 성별, 성별(코드명), 생년월, real, not

- observation.csv :  지역병원코드, 지역병원코드(코드명), 순번, 연구내원번호, 기록실시일시, 임상관찰코드, 임상관찰코드(코드명), 분류구분, 연구등록번호, 내원구분,
                    내원구분(코드명), 총량, 측정값, 잔류량, 처방번호, 측정종료여부, 측정종료여부(코드명), 공통여부, 작성부서, 작성부서(코드명), 간호기록키,
                    성별, 성별(코드명), 생년월, 서식기록키, 작성구분, real, not

- lab.csv : 지역병원코드, 지역병원코드(코드명), 연구등록번호, 연구내원번호, 처방일련번호, 시행일자, 처방코드, 처방코드(코드명), 참고치, 검사비고, 수치결과(수치), 
            일반결과, 결과값, 검체번호, real, not
- lab2.csv : 지역병원코드, 지역병원코드(코드명), 연구등록번호, 연구내원번호, 처방코드, 처방코드(코드명), 수치결과, 수치결과(수치), 문자결과, 서식키, 그룹처방코드
            그룹처방코드(코드명), 결과입력일시, 서식일자, 검체번호, 검사시작일시, real, not

- labtime.csv : 지역병원코드, 연구등록번호, 연구내원번호, 내원구분, 성별, 나이, 검체번호, 검체코드, 검체용기코드, 검체발생구분, 처방일자, 처방일시, 접수일자,
                접수일시, 접수자ID, 검사실접수일자, 검사실접수일시, 검사실접수자ID, 검사장소코드, 검사진행상태, 검체채취일자, 검체채취일시, 검체채취자ID, 
                처방채취장소구분, 채취장소코드, 검체확인일자, 검체확인일시, 검체불가일시, 검체확인자ID, 외주검사여부, 외주검사확인일자, 외주검사확인일시, 
                외주검사확인자ID, 접종일자, 접종일시, 접종자ID, 진료과, 주치의ID, 센터코드, 병동, 병실, 병상, 미생물작업그룹코드, Slip코드, SMS전송일시, 
                취소사유코드, 작업일련번호, 연속검사일련번호, 특이사항, 연속검사분, 응급검사구분, 공복여부, 미수납접수구분, 수탁검사여부, ROBO일련번호, 
                바코드출력일시, 바코드출력일련번호, 바코드출력자ID, 이전바코드번호, SMS전송여부, real, not

- prescription.csv : 지역병원코드, 지역병원코드(코드명), 연구등록번호, 연구내원번호, 처방일자, 처방코드, 처방코드(코드명), 성별, 성별(코드명), 처방시나이,
                    시행일자, 시행일시, 처방명, 용량, 횟수, 일수, 검체코드, 검체코드(코드명), T용량, real, not

- diagnosis.csv : 지역병원코드, 지역병원코드(코드명), 연구등록번호, 연구내원번호, 내원구분, 내원구분(코드명), 진료일자, 진료과, 진료과(코드명), 진료의Id, 
                    진료의Id(코드명), 진단코드, 진단코드(코드명), 진단일자, ICD-10 코드, ICD-10 코드(코드명), 성별, 성별(코드명), 진단시점나이, real, not


- surgery.csv : 지역병원코드, 지역병원코드(코드명), 연구내원번호, 연구등록번호, 성별, 성별(코드명), 생년월, 수술일자, 수술시작일시, 주수술과주치의ID, 
                주수술과주치의ID(코드명), 수술코드, 수술코드(코드명), 수술명(입력), ICD-9CM 코드, ICD-9CM 코드(코드명), 수술일련번호, real, not


'''


base_dir = 'C:/Users/User5/Desktop/github/YS_labelling/'
date = '220217/'
dst_dir = base_dir + 'preprocessed_data/' + date




''' =========================================== Read CSV files.... =========================================== '''
# icustays csv file
icustays_df = pd.read_csv(base_dir + 'origin_data/' + date + 'icustays.csv', index_col=0, encoding='cp949')
icu_info = icustays_df[['real','not', '연구등록번호', '전입일시', '전출일시', '성별', '생년월']]
icu_info.columns = ['pat_id', 'study_id', 'study_number', 'intime', 'outtime', 'sex', 'birth']

# Observation csv file
observation_df = pd.read_csv(base_dir + 'origin_data/' + date + 'observation.csv', index_col=0, encoding='cp949')
obs_result = observation_df[['real','not', '연구등록번호', '임상관찰코드', '임상관찰코드(코드명)', '기록실시일시', '측정값']]
obs_result.columns = ['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'charttime', 'value']

# lab.csv & lab2.csv & labtime.csv
labtime_df = pd.read_csv(base_dir + 'origin_data/' + date + 'labtime.csv', index_col=0, encoding='cp949')
labtime_df = labtime_df[['real', 'not', '검체번호',  '검체채취일시']]
labtime_df.columns = ['pat_id', 'study_id', 'sample_number', 'charttime']

# original LAB results data input
lab_df = pd.read_csv(base_dir + 'origin_data/' + date +  'lab.csv', index_col=0, encoding='cp949')
lab_df = lab_df[['real', 'not', '연구등록번호', '처방코드', '처방코드(코드명)', '수치결과(수치)', '검체번호' ]]
lab_df.columns = ['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'value', 'sample_number']

lab2_df = pd.read_csv(base_dir + 'origin_data/' + date + 'lab2.csv', index_col=0, encoding='cp949')
lab2_df = lab2_df[['real', 'not', '연구등록번호', '처방코드', '처방코드(코드명)', '수치결과(수치)', '검체번호']]
lab2_df.columns = ['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'value', 'sample_number']

# LAB + lab_charttime merge
lab1 = pd.merge(lab_df, labtime_df, on=['sample_number', 'pat_id', 'study_id'])
lab2 = pd.merge(lab2_df, labtime_df, on=['sample_number', 'pat_id', 'study_id'])
# LAB1 + LAB2 concat
lab_result = pd.concat([lab1, lab2], axis=0).sort_values(by=['pat_id', 'charttime'])
lab_result.iloc[:5,:].to_csv('./test.csv', encoding='cp949')
lab_result = lab_result[['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'charttime', 'value']]

# Prescription csv file
prescription_df = pd.read_csv(base_dir + 'origin_data/' + date + 'prescription.csv', index_col=0, encoding='cp949')
pres_result = prescription_df[['real','not', '연구등록번호', '처방코드', '처방코드(코드명)', '시행일시']]
pres_result.columns = ['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'charttime']

# Diagnosis csv file
diagnosis_df = pd.read_csv(base_dir + 'origin_data/' + date + 'diagnosis.csv', index_col=0, encoding='cp949')
diag_result = diagnosis_df[['real','not', '연구등록번호', '진료일자', '진단코드', '진단코드(코드명)', 'ICD-10 코드']]
diag_result.columns = ['pat_id', 'study_id', 'study_number', 'diag_date', 'diag_code', 'diag_name', 'ICD10']


surgery_df = pd.read_csv(base_dir + 'origin_data/' + date + 'surgery.csv', index_col=0, encoding='cp949')
surg_result = surgery_df[['real','not', '연구등록번호', '수술시작일시', '수술코드', '수술코드(코드명)', 'ICD-9CM 코드']]
surg_result.columns = ['pat_id', 'study_id', 'study_number', 'starttime', 'surgery_code', 'surgery_name', 'ICD9']

''' ========================================================================================================= '''



''' =================================== Search Variables for Renal Failure =================================== '''

# Creatinine (lab.csv : 처방코드)
Cr = lab_result[lab_result['item_code'].isin(['C375002', '5B001_19', '5B00129' ])].drop_duplicates()
Cr['item'] = 'Creatinine'
Cr.to_csv(dst_dir + 'variables/Cr.csv', encoding='cp949')
print('========== Cr ==========')
print(Cr)

# pH (lab.csv : 처방코드)
pH = lab_result[lab_result['item_code'].isin(['L000101202', 'L008901201', 'L601007209', 'L600101202'])].drop_duplicates()
pH['item'] = 'pH'
pH.to_csv(dst_dir + 'variables/pH.csv', encoding='cp949')
print('========== pH ==========')
print(pH)

# potassium (lab.csv : 처방코드)
potassium = lab_result[lab_result['item_code'].isin(['C379204'])].drop_duplicates()
potassium['item'] = 'potassium'
potassium.to_csv(dst_dir + 'variables/potassium.csv', encoding='cp949')
print('========== potassium ==========')
print(potassium)

# bun (lab.csv : 처방코드)
bun = lab_result[lab_result['item_code'].isin(['C373001'])].drop_duplicates()
bun['item'] = 'BUN'
bun.to_csv(dst_dir + 'variables/bun.csv', encoding='cp949')
print('========== bun ==========')
print(bun)

# U/O (observation.csv : 임상관찰코드)
uo = obs_result[obs_result['item_code'].isin(['4001600011'])].drop_duplicates()
uo['item'] = 'Urineoutput'
uo.to_csv(dst_dir + 'variables/uo.csv', encoding='cp949')
print('========== Urine Output ==========')
print(uo)

# Hemodialysis (prescription.csv : 처방코드)
hemodialysis = pres_result[pres_result['item_code'].isin(['YO7020B_004', 'V10P0021', 'V10P0045', 'V10P0022', 'V10P0026', 'V09G0057', 'V09G0059', 'V09G0246'])].drop_duplicates()
hemodialysis['value'] = np.nan
hemodialysis['item'] = 'hemodialysis'
hemodialysis.to_csv(dst_dir + 'variables/hemodialysis.csv', encoding='cp949')
print('========== Hemodialysis ==========')
print(hemodialysis)

# ESRD + CKD (diagnosis.csv : 진단코드)
esrd_ckd = diag_result[diag_result['diag_code'].isin(['DI024743', 'DI010115', 'DI050025', 'DI050026', 'DI050027', 'DI050028', 'DI050029', 'DI032358', 'DI045702', 'DI010107', 'DI010114', 'DI005316'])].drop_duplicates()
esrd_ckd['item'] = 'ESRD_CKD'
esrd_ckd.to_csv(dst_dir + 'variables/hemodialysis.csv', encoding='cp949')
print('========== ESRD + CKD ==========')
print(esrd_ckd)





''' ================ Variables for Respiratory Failure ============'''

# O2 saturation - SpO2 (observation.csv : 관찰코드)
spo2 = obs_result[obs_result['item_code'].isin(['2001100049'])].drop_duplicates()
spo2 = spo2[['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'charttime', 'value']]
spo2['item'] = 'spo2'
spo2.to_csv(dst_dir + 'variables/spo2.csv', encoding='cp949')
print('========== SpO2 ==========')
print(spo2)

# pO2 (lab.csv : 처방코드)
pO2 = lab_result[lab_result['item_code'].isin(['L600103202'])].drop_duplicates()
pO2 = pO2[['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'charttime', 'value']]
pO2['item'] = 'pO2'
pO2.to_csv(dst_dir + 'variables/pO2.csv', encoding='cp949')
print('========== pO2 ==========')
print(pO2)

# pO2 (lab.csv : 처방코드)
pCO2 = lab_result[lab_result['item_code'].isin(['L000102202'])].drop_duplicates()
pCO2 = pCO2[['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'charttime', 'value']]
pCO2['item'] = 'pCO2'
pCO2.to_csv(dst_dir + 'variables/pCO2.csv', encoding='cp949')
print('========== pCO2 ==========')
print(pCO2)

# PF_ratio (lab.csv : 처방코드)
pf_ratio = lab_result[lab_result['item_code'].isin(['L600115202'])].drop_duplicates()
pf_ratio = pf_ratio[['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'charttime', 'value']]
pf_ratio['item'] = 'PF_ratio'
pf_ratio.to_csv(dst_dir + 'variables/pf_ratio.csv', encoding='cp949')
print('========== PF_ratio ==========')
print(pf_ratio)

# Intubation (prescription.csv: 처방코드)
intubation = pres_result[pres_result['item_code'].isin(['M5859_001', 'LX001_002'])].drop_duplicates()
intubation = intubation[['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'charttime']]
intubation['value'] = np.nan
intubation['item'] = 'intubation'
intubation.to_csv(dst_dir + 'variables/intubation.csv', encoding='cp949')
print('========== Intubation ==========')
print(intubation)

# Mechanical Ventilator (Observation.csv: 임상관찰코드)
ventilator = obs_result[obs_result['item_code'].isin(['5003800023', '5003800009', '5003800010', '5003800006', '5003800008', '5003800005',
                                                    '5003800013', '5003800014', '5003800011', '5003800001', '5003800004', '5003800028', 
                                                    '5003800027', '5003800007', '5003800026', '5003800012', '5003800025', '5003800030',
                                                    '5003800029', '5003800024', '5003800003', '5003800035', '5003800037'])].drop_duplicates()
ventilator = ventilator[['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value']]
ventilator['item'] = 'ventilator'
ventilator.to_csv(dst_dir + 'variables/ventilator.csv', encoding='cp949')
print('========== Ventilator ==========')
print(ventilator)

# Extubatoin (prescription.csv : 처방코드)
extubation = pres_result[pres_result['item_code'].isin(['5P002_036'])].drop_duplicates()
extubation = extubation[['pat_id', 'study_id', 'study_number', 'item_code', 'item_name', 'charttime']]
extubation['value'] = np.nan
extubation['item'] = 'extubation'
extubation.to_csv(dst_dir + 'variables/extubation.csv', encoding='cp949')
print('========== Extubation ==========')
print(extubation)

# ================================================= 추출된 변수 DataFrame 으로 합치기 =================================================
# DataFrame 1: Observation + LAB   ['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value', 'item']
#              (Cr, pH, potassium, bun, U/O, SpO2, pO2, pCO2, PF_ratio, Intubation, Extubation, Ventilator_setting)
# DataFrame 2: Hemodialysis    ['pat_id', 'study_id', 'diag_code', 'diag_name', 'diag_date', 'ICD10', 'item']
# DataFrame 3: Surgery    ['pat_id', 'study_id',  'surgery_code', 'surgery_name', 'starttime', 'ICD9', 'item']
# =====================================================================================================================================

# DataFrame 1

df1 = pd.concat([Cr, pH, potassium, bun, uo, hemodialysis, spo2, pO2, pCO2, pf_ratio, intubation, extubation, ventilator], axis=0)
df1 = pd.merge(df1, icu_info, on=['pat_id', 'study_id'])
df1.to_csv(dst_dir + 'total_result.csv', encoding='cp949')


# Dataframe 2
df2 = esrd_ckd.to_csv(dst_dir + 'esrd_result.csv', encoding='cp949')

# DataFrame 3
df3 = surg_result.to_csv(dst_dir + 'surg_result.csv', encoding='cp949')
