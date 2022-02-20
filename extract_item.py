import pandas as pd

base_pth = './'

lab_item = pd.read_csv(base_pth + 'item/lab_item.csv', index_col=0)


# # LAB csv file 에서 필요한 item 전부 추출
# var_list = ['FIO2', 'pO2', 'pCO2', 'pO2/FIO2', 'Potassium', 'pH', 'BUN', 'Creatinine']
# contain_list = '|'.join(var_list)


# result = lab_item[lab_item['item'].str.contains(contain_list)].reset_index(drop=True).drop_duplicates(['item'])
# result.to_csv('./lab_var.csv')


# # observation csv file 에서 필요한 item 전부 추출
# observation_item = pd.read_csv(base_pth + 'origin_data/220217/observation.csv', index_col=0, encoding='cp949')
# result = observation_item[['임상관찰코드(코드명)']].dropna()
# result.columns = ['item']

# var_list = ['SpO2', 'SPO2', 'Foley', 'Urine', 'UO']
# contain_list = '|'.join(var_list)

# result = result[result['item'].str.contains(contain_list)].reset_index(drop=True).drop_duplicates(['item'])
# result.to_csv('./observation_var.csv', encoding='cp949')


# prescription csv file 에서 필요한 item 전부 추출
# prescription_item = pd.read_csv(base_pth + 'origin_data/220217/prescription.csv', index_col=0, encoding='cp949')
# result = prescription_item[['처방코드(코드명)']].dropna()

# var_list = ['Ventilator care', 'Extubation', 'Intubation', 'dialysis', 'Hemodialysis', ]
# contain_list = '|'.join(var_list)

# result = result[result['처방코드(코드명)'].str.contains(contain_list)]
# result.columns = ['item']
# result = result.drop_duplicates(['item'])
# result.to_csv('./prescription_var.csv')



# diagnosis csv file 에서 필요한 item 전부 추출
prescription_item = pd.read_csv(base_pth + 'origin_data/220217/diagnosis.csv', index_col=0, encoding='cp949')
result = prescription_item[['진단코드', '진단코드(코드명)']].dropna()
result.columns = ['item_code', 'item']

var_list = ['renal failure', 'kidney disease']
contain_list = '|'.join(var_list)

result = result[result['item'].str.contains(contain_list)]
result = result.drop_duplicates(['item'])
result.to_csv('./diagnosis_var.csv')




# observation_item = pd.read_csv(base_pth + 'origin_data/220217/observation.csv', index_col=0, encoding='cp949')

# result = observation_item[['임상관찰코드(코드명)', '측정값']].dropna()

# var_list = ['SPO2', 'SpO2']
# contain_list = '|'.join(var_list)

# result = result[result['임상관찰코드(코드명)'].str.contains(contain_list)].reset_index(drop=True)
# result.to_csv('./test.csv', encoding='cp949')
# print(result)
# lab.csv & lab2.csv & labtime.csv



# base_dir = 'C:/Users/User5/Desktop/github/YS_labelling/'


# lab_df = pd.read_csv(base_pth + 'origin_data/220217/lab.csv', index_col=0, encoding='cp949')
# lab2_df = pd.read_csv(base_pth + 'origin_data/220217/lab2.csv', index_col=0, encoding='cp949')


# lab_df = lab_df[['real', 'not', '연구등록번호', '처방코드', '처방코드(코드명)', '수치결과(수치)', '검체번호' ]]
# lab2_df = lab2_df[['real', 'not', '연구등록번호', '처방코드', '처방코드(코드명)', '수치결과(수치)', '검체번호']]



# result = lab_df[lab_df['처방코드(코드명)']=='Creatinine (2hr)[Serum]']
# result2 = lab_df[lab_df['처방코드(코드명)']=='Creatinine (2hr)[Serum]']

# result.to_csv('./test.csv', encoding='cp949')
# result2.to_csv('./test2.csv', encoding='cp949')







# # diagnosis csv file 에서 필요한 item 전부 추출
# diagnosis = pd.read_csv(base_pth + 'origin_data/220217/diagnosis.csv', index_col=0, encoding='cp949')
# result = diagnosis[['진단코드', '진단코드(코드명)']].dropna()
# print(result)

# result = result[result['진단코드(코드명)'].str.contains('신부전을 동반한 고혈압성 신장병')]
# result = result.drop_duplicates(['진단코드(코드명)'])
# # result.to_csv('./prescription_var.csv')
# print(result)

