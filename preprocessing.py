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
icu_info = icustays_df[['real','not', '전입일시', '전출일시', '성별', '생년월']].reset_index(drop=True)
icu_info.columns = ['pat_id', 'study_id', 'intime', 'outtime', 'sex', 'birth']

# Observation csv file
observation_df = pd.read_csv(base_dir + 'origin_data/' + date + 'observation.csv', index_col=0, encoding='cp949')
obs_result = observation_df[['real','not', '임상관찰코드', '임상관찰코드(코드명)', '기록실시일시', '측정값']]
obs_result.columns = ['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value']

# lab.csv & lab2.csv & labtime.csv
labtime_df = pd.read_csv(base_dir + 'origin_data/' + date + 'labtime.csv', index_col=0, encoding='cp949')
labtime_df = labtime_df[['real', 'not', '검체번호',  '검체채취일시']]
labtime_df.columns = ['pat_id', 'study_id', 'sample_number', 'charttime']

# original LAB results data input
lab_df = pd.read_csv(base_dir + 'origin_data/' + date +  'lab.csv', index_col=0, encoding='cp949')
lab_df = lab_df[['real', 'not', '처방코드', '처방코드(코드명)', '수치결과(수치)', '검체번호' ]]
lab_df.columns = ['pat_id', 'study_id', 'item_code', 'item_name', 'value', 'sample_number']

lab2_df = pd.read_csv(base_dir + 'origin_data/' + date + 'lab2.csv', index_col=0, encoding='cp949')
lab2_df = lab2_df[['real', 'not', '처방코드', '처방코드(코드명)', '수치결과(수치)', '검체번호']]
lab2_df.columns = ['pat_id', 'study_id', 'item_code', 'item_name', 'value', 'sample_number']

# LAB + lab_charttime merge
lab1 = pd.merge(lab_df, labtime_df, on=['sample_number', 'pat_id', 'study_id'])
lab2 = pd.merge(lab2_df, labtime_df, on=['sample_number', 'pat_id', 'study_id'])
# LAB1 + LAB2 concat
lab_result = pd.concat([lab1, lab2], axis=0).sort_values(by=['pat_id', 'charttime'])
lab_result = lab_result[['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value']]

# Prescription csv file
prescription_df = pd.read_csv(base_dir + 'origin_data/' + date + 'prescription.csv', index_col=0, encoding='cp949')
pres_result = prescription_df[['real','not', '처방코드', '처방코드(코드명)', '시행일시']]
pres_result.columns = ['pat_id', 'study_id',  'item_code', 'item_name', 'charttime']

# Diagnosis csv file
diagnosis_df = pd.read_csv(base_dir + 'origin_data/' + date + 'diagnosis.csv', index_col=0, encoding='cp949')
diag_result = diagnosis_df[['real','not', '진료일자', '진단코드', '진단코드(코드명)', 'ICD-10 코드']]
diag_result.columns = ['pat_id', 'study_id', 'diag_date', 'diag_code', 'diag_name', 'ICD10']

surgery_df = pd.read_csv(base_dir + 'origin_data/' + date + 'surgery.csv', index_col=0, encoding='cp949')
surg_result = surgery_df[['real','not', '수술시작일시', '수술코드', '수술코드(코드명)', 'ICD-9CM 코드']]
surg_result.columns = ['pat_id', 'study_id', 'starttime', 'surgery_code', 'surgery_name', 'ICD9']

''' ========================================================================================================= '''



''' =================================== Search Variables for Renal Failure =================================== '''

# Creatinine (lab.csv : 처방코드)
Cr = lab_result[lab_result['item_name'].isin(['Creatinine[Serum]', 'Creatinine (2hr)[Serum]', 'Serum Creatini-ne for CCr[Serum]' ])].drop_duplicates()
Cr['item'] = 'Creatinine'
Cr.to_csv(dst_dir + 'variables/Cr.csv', encoding='cp949')
# print('========== Cr ==========')
# print(Cr)

# pH (lab.csv : 처방코드)
pH = lab_result[lab_result['item_name'].isin(['pH[Arterial Whole blood]', 'pH[Venous Whole blood]', 'pH[Capillary blood]', 'pH[Arterial Whole blood]'])].drop_duplicates()
pH['item'] = 'pH'
pH.to_csv(dst_dir + 'variables/pH.csv', encoding='cp949')
# print('========== pH ==========')
# print(pH)

# potassium (lab.csv : 처방코드)
potassium = lab_result[lab_result['item_name'].isin(['K (Potassium)[Serum]'])].drop_duplicates()
potassium['item'] = 'potassium'
potassium.to_csv(dst_dir + 'variables/potassium.csv', encoding='cp949')
# print('========== potassium ==========')
# print(potassium)

# bun (lab.csv : 처방코드)
bun = lab_result[lab_result['item_name'].isin(['BUN[Serum]'])].drop_duplicates()
bun['item'] = 'BUN'
bun.to_csv(dst_dir + 'variables/bun.csv', encoding='cp949')
# print('========== bun ==========')
# print(bun)

# U/O (observation.csv : 임상관찰코드)
uo = obs_result[obs_result['item_name'].isin(['소변/Foley'])].drop_duplicates()
uo['item'] = 'Urineoutput'
uo.to_csv(dst_dir + 'variables/uo.csv', encoding='cp949')
# print('========== Urine Output ==========')
# print(uo)

# Hemodialysis (prescription.csv : 처방코드)
hemodialysis = pres_result[pres_result['item_name'].isin([
    'Hemodialysis', 'V10P0021 : Hemodialysis Cath 414002-JUGULAR 11.5FR 16CM (5EA/BOX)-30414-002 DUAL CVD/EA-COVIDIEN-(주)라온',
    'Hemodialysis Cath 794009-JUGULAR 11.5FR 19.5CM (5EA/BOX-13794-009 DUAL CVD./EA-COVIDIEN-(주)라온', 'Hemodialysis G/W/EA-BARD REYNOSA',
    'Hemodialysis Cath-6.5FR(1EA/1BOX)-소아용/EA-GAMBRO-박스터', 'Hemodialysis Cath-SUBCLAVIAN 20CM-DUAL STR./EA-BARD REYNOSA',
    'Hemodialysis G/W 231001-J-TYPE (10EA/BOX)-13796-001/EA-COVIDIEN-(주)라온', 'Hemodialysis G/W-GDK-115J/EA-한국갬브로-박스터'])].drop_duplicates()
hemodialysis['value'] = np.nan
hemodialysis['item'] = 'hemodialysis'
hemodialysis.to_csv(dst_dir + 'variables/hemodialysis.csv', encoding='cp949')
# print('========== Hemodialysis ==========')
# print(hemodialysis)

# ESRD + CKD (diagnosis.csv : 진단코드)
esrd_ckd = diag_result[diag_result['diag_name'].isin([
    'End stage renal disease (Hemodialysis)(혈액투석중인 말기신장병)', 'Chronic renal failure(만성 신장부전)', 'Chronic kidney disease  stage 1(만성 신장병(1기))',
    'Chronic kidney disease  stage 2(만성 신장병(2기))', 'Chronic kidney disease  stage 3(만성 신장병(3기))', 'Chronic kidney disease  stage 4(만성 신장병(4기))',
    'Chronic kidney disease  stage 5(만성 신장병(5기))', 'Chronic renal failure with exacerbation(만성신부전 악화)', 'Acute renal failure(급성 신부전)',
    'Chronic kidney disease  unspecified(상세불명의 만성 신장병)', 'Other chronic renal failure(기타 만성 콩팥(신장)기능상실)',
    'Chronic renal failure and hypertension(만성 신부전과 고혈압)'])].drop_duplicates()
esrd_ckd['item'] = 'ESRD_CKD'
esrd_ckd.to_csv(dst_dir + 'variables/esrd_result.csv', encoding='cp949')
# print('========== ESRD + CKD ==========')
# print(esrd_ckd)

''' ================ Variables for Respiratory Failure ============'''

# O2 saturation - SpO2 (observation.csv : 관찰코드)
spo2 = obs_result[obs_result['item_name'].isin(['Monitoring/SpO2'])].drop_duplicates()
spo2 = spo2[['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value']]
spo2['item'] = 'spo2'
spo2.to_csv(dst_dir + 'variables/spo2.csv', encoding='cp949')
# print('========== SpO2 ==========')
# print(spo2)

# pO2 (lab.csv : 처방코드)
pO2 = lab_result[lab_result['item_name'].isin(['pO2[Arterial Whole blood]'])].drop_duplicates()
pO2 = pO2[['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value']]
pO2['item'] = 'pO2'
pO2.to_csv(dst_dir + 'variables/pO2.csv', encoding='cp949')
# print('========== pO2 ==========')
# print(pO2)

# pCO2 (lab.csv : 처방코드)
pCO2 = lab_result[lab_result['item_name'].isin(['pCO2[Arterial Whole blood]'])].drop_duplicates()
pCO2 = pCO2[['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value']]
pCO2['item'] = 'pCO2'
pCO2.to_csv(dst_dir + 'variables/pCO2.csv', encoding='cp949')
# print('========== pCO2 ==========')
# print(pCO2)

# PF_ratio (lab.csv : 처방코드)
pf_ratio = lab_result[lab_result['item_name'].isin(['pO2/FIO2[Arterial Whole blood]'])].drop_duplicates()
pf_ratio = pf_ratio[['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value']]
pf_ratio['item'] = 'PF_ratio'
pf_ratio.to_csv(dst_dir + 'variables/pf_ratio.csv', encoding='cp949')
# print('========== PF_ratio ==========')
# print(pf_ratio)

# Intubation (prescription.csv: 처방코드)
intubation = pres_result[pres_result['item_name'].isin(['Intubation', 'Intubation by Bronchoscopy'])].drop_duplicates()
intubation = intubation[['pat_id', 'study_id', 'item_code', 'item_name', 'charttime']]
intubation['value'] = np.nan
intubation['item'] = 'intubation'
intubation.to_csv(dst_dir + 'variables/intubation.csv', encoding='cp949')
# print('========== Intubation ==========')
# print(intubation)

# Mechanical Ventilator (Observation.csv: 임상관찰코드)
ventilator = obs_result[obs_result['item_name'].isin([
    'Respiratory management/Ventilator 설정', 'Respiratory management/Ventilator_PSV(Setting)', 'Respiratory management/Ventilator_RR(Pt)',
    'Respiratory management/Ventilator_PEEP', 'Respiratory management/Ventilator_PIP(Pt)', 'Respiratory management/Ventilator_Mv(Pt)',
    'Respiratory management/Ventilator_Vt(Pt)', 'Respiratory management/Ventilator_Vt(setting)','Respiratory management/Ventilator_RR(Setting)',
    'Respiratory management/Ventilator_IP(Setting)','Respiratory management/Ventilator_I:E(setting)', 'Respiratory management/Ventilator_Pressure Trigger',
    'Respiratory management/Ventilator_Flow Trigger', 'Respiratory management/Ventilator_Mv(Setting)','Respiratory management/Ventilator_Plateau Pressure',
    'Respiratory management/Ventilator_Stroke volume', 'Respiratory management/Ventilator 설정(Home)','Respiratory management/Ventilator_EPAP',
    'Respiratory management/Ventilator_IPAP', 'Respiratory management/Ventilator 설정(NIV)','Respiratory management/Ventilator_MAP',
    'Respiratory management/Ventilator_Mv(Setting: %)','Respiratory management/Ventilator 설정(Home NIV)'])].drop_duplicates()
ventilator = ventilator[['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value']]
ventilator['item'] = 'ventilator'
ventilator.to_csv(dst_dir + 'variables/ventilator.csv', encoding='cp949')
# print('========== Ventilator ==========')
# print(ventilator)

# Extubatoin (prescription.csv : 처방코드)
extubation = pres_result[pres_result['item_name'].isin(['Extubation'])].drop_duplicates()
extubation = extubation[['pat_id', 'study_id', 'item_code', 'item_name', 'charttime']]
extubation['value'] = np.nan
extubation['item'] = 'extubation'
extubation.to_csv(dst_dir + 'variables/extubation.csv', encoding='cp949')
# print('========== Extubation ==========')
# print(extubation)

print('===============================  Variables Extraction Completed... ===============================')

# ================================================= 추출된 변수 DataFrame 으로 합치기 =================================================
# DataFrame 1: Observation + LAB   ['pat_id', 'study_id', 'item_code', 'item_name', 'charttime', 'value', 'item']
#              (Cr, pH, potassium, bun, U/O, SpO2, pO2, pCO2, PF_ratio, Intubation, Extubation, Ventilator_setting)
# DataFrame 2: Hemodialysis    ['pat_id', 'study_id', 'diag_code', 'diag_name', 'diag_date', 'ICD10', 'item']
# DataFrame 3: Surgery    ['pat_id', 'study_id',  'surgery_code', 'surgery_name', 'starttime', 'ICD9', 'item']
# DataFrame 4: ICU info 
# =====================================================================================================================================

# DataFrame 1 : observation & LAB results value information

df1 = pd.concat([Cr, pH, potassium, bun, uo, hemodialysis, spo2, pO2, pCO2, pf_ratio, intubation, extubation, ventilator], axis=0)
df1.to_csv(dst_dir + 'total_result.csv', encoding='cp949')

# Dataframe 2 : Diagnosis information
esrd_ckd.to_csv(dst_dir + 'esrd_result.csv', encoding='cp949')

# DataFrame 3 : Surgery information
surg_result.to_csv(dst_dir + 'surg_result.csv', encoding='cp949')

# DataFrame 4: ICU information 
icu_info.to_csv(dst_dir + 'icu_info.csv', encoding='cp949')
