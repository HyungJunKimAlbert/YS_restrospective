from doctest import DONT_ACCEPT_TRUE_FOR_1
import pandas as pd
import numpy as np
from sklearn.manifold import locally_linear_embedding
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
dst_dir = base_dir + date + 'preprocessed_data/'


# icustays csv file
# icustays_df = pd.read_csv(base_dir + 'origin_data/' + date + 'icustays.csv', index_col=0, encoding='cp949')
# result = icustays_df[['real','not', '연구등록번호', '전입일시', '전출일시', '측정값', '성별', '생년월']
# result.to_csv(base_dir + 'preprocessed_data/' + date + 'icustays_preprocessd.csv')

''' =========================================== Read CSV files.... =========================================== '''

# Observation csv file
observation_df = pd.read_csv(base_dir + 'origin_data/' + date + 'observation.csv', index_col=0, encoding='cp949')
obs_result = observation_df[['real','not', '연구등록번호', '임상관찰코드', '임상관찰코드(코드명)', '기록실시일시', '측정값']]

# lab.csv & lab2.csv & labtime.csv
labtime_df = pd.read_csv(base_dir + 'origin_data/' + date + 'labtime.csv', index_col=0, encoding='cp949')
labtime_df = labtime_df[['real', 'not', '검체번호',  '검체채취일시']]
# original LAB results data input
lab_df = pd.read_csv(base_dir + 'origin_data/' + date +  'lab.csv', index_col=0, encoding='cp949')
lab_df = lab_df[['real', 'not', '연구등록번호', '처방코드', '처방코드(코드명)', '수치결과(수치)', '검체번호' ]]
lab2_df = pd.read_csv(base_dir + 'origin_data/' + date + 'lab2.csv', index_col=0, encoding='cp949')
lab2_df = lab2_df[['real', 'not', '연구등록번호', '처방코드', '처방코드(코드명)', '수치결과(수치)', '검체번호']]
# LAB + lab_charttime merge
lab1 = pd.merge(lab_df, labtime_df, on=['검체번호', 'real', 'not'])
lab2 = pd.merge(lab2_df, labtime_df, on=['검체번호', 'real', 'not'])
# LAB1 + LAB2 concat
lab_result = pd.concat([lab1, lab2], axis=0).sort_values(by=['real', '검체채취일시'])

# Prescription csv file
prescription_df = pd.read_csv(base_dir + 'origin_data/' + date + 'prescription.csv', index_col=0, encoding='cp949')
pres_result = prescription_df[['real','not', '연구등록번호', '처방코드', '처방코드(코드명)', '시행일자']]

# Diagnosis csv file
diagnosis_df = pd.read_csv(base_dir + 'origin_data/' + date + 'diagnosis.csv', index_col=0, encoding='cp949')
diag_result = diagnosis_df[['real','not', '연구등록번호', '진료일자', '진단코드', '진단코드(코드명)', 'ICD-10 코드']]

''' ========================================================================================================= '''




''' =================================== Search Variables for Renal Failure =================================== '''

# Creatinine (lab.csv : 처방코드)
Cr = lab_result[lab_result['처방코드'].isin(['C375002', '5B001_19', '5B00129' ])].drop_duplicates()
print('========== Cr ==========')
print(Cr)

# pO2 (lab.csv : 처방코드)
pO2 = lab_result[lab_result['처방코드'].isin(['L600103202'])].drop_duplicates()
print('========== pO2 ==========')
print(pO2)

# pO2 (lab.csv : 처방코드)
pCO2 = lab_result[lab_result['처방코드'].isin(['L000102202'])].drop_duplicates()
print('========== pCO2 ==========')
print(pCO2)

# PF_ratio (lab.csv : 처방코드)
pf_ratio = lab_result[lab_result['처방코드'].isin(['L600115202'])].drop_duplicates()
print('========== PF_ratio ==========')
print(pf_ratio)

# pH (lab.csv : 처방코드)
pH = lab_result[lab_result['처방코드'].isin(['L000101202', 'L008901201', 'L601007209', 'L600101202'])].drop_duplicates()
print('========== pH ==========')
print(pH)

# potassium (lab.csv : 처방코드)
potassium = lab_result[lab_result['처방코드'].isin(['C379204'])].drop_duplicates()
print('========== potassium ==========')
print(potassium)

# bun (lab.csv : 처방코드)
bun = lab_result[lab_result['처방코드'].isin(['C373001'])].drop_duplicates()
print('========== bun ==========')
print(bun)

# U/O (observation.csv : 임상관찰코드)
uo = obs_result[obs_result['임상관찰코드'].isin(['4001600011'])].drop_duplicates()
print('========== Urine Output ==========')
print(uo)

# Hemodialysis (prescription.csv : 처방코드)
hemodialysis = pres_result[pres_result['처방코드'].isin(['YO7020B_004', 'V10P0021', 'V10P0045', 'V10P0022', 'V10P0026', 'V09G0057', 'V09G0059', 'V09G0246'])].drop_duplicates()
print('========== Hemodialysis ==========')
print(hemodialysis)

# ESRD + CKD (diagnosis.csv : 진단코드)
esrd_ckd = diag_result[diag_result['진단코드'].isin(['DI024743', 'DI010115', 'DI050025', 'DI050026', 'DI050027', 'DI050028', 'DI050029', 'DI032358', 'DI045702', 'DI010107', 'DI010114', 'DI005316'])].drop_duplicates()
print('========== ESRD + CKD ==========')
print(esrd_ckd)




''' ================ Variables for Respiratory Failure ============'''














# diagnosis csv file
# diagnosis_df = pd.read_csv(base_dir + date + 'origin_data/diagnosis.csv', index_col=0, encoding='cp949')

# drugtime csv file
# drugtime_df = pd.read_csv(base_dir + date + 'origin_data/drugtime.csv', index_col=0, encoding='cp949')


# prescription csv file
# prescription_df = pd.read_csv(base_dir + date + 'origin_data/prescription.csv', index_col=0, encoding='cp949')


# surgery csv file
# surgery_df = pd.read_csv(base_dir + date + 'data/surgery.csv', index_col=0, encoding='cp949')



