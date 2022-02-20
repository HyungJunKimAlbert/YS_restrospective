
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

- surgery.csv : 지역병원코드, 지역병원코드(코드명), 연구내원번호, 연구등록번호, 성별, 성별(코드명), 생년월, 수술일자, 수술시작일시, 주수술과주치의ID, 
                주수술과주치의ID(코드명), 수술코드, 수술코드(코드명), 수술명(입력), ICD-9CM 코드, ICD-9CM 코드(코드명), 수술일련번호, real, not
'''





# item Code

'''
### RESPIRATORY FAILURE

*** SpO2 (observation.csv: 임상관찰코드)
    2001100049 : Monitoring/SpO2

*** pO2 (lab.csv: 처방코드)
    L600103202 : pO2[Arterial Whole blood]

*** pCO2 (lab.csv: 처방코드)
    L000102202 : pCO2[Arterial Whole blood]

*** PF_ratio (lab.csv: 처방코드)
    L600115202 : pO2/FIO2[Arterial Whole blood]


*** Intubation (prescription.csv: 처방코드)
    
    - Intubation 먼저 조회 후, Intubation 내역 없으면 아래 code 사용)
    
    M5859_001 : Intubation
    LX001_002 : Intubation by Bronchoscopy

*** Ventilator (observation.csv: 임상관찰코드) 

    5003800023 : Respiratory management/Ventilator 설정
    5003800009 : Respiratory management/Ventilator_PSV(Setting)
    5003800010 : Respiratory management/Ventilator_RR(Pt)
    5003800006 : Respiratory management/Ventilator_PEEP
    5003800008 : Respiratory management/Ventilator_PIP(Pt)
    5003800005 : Respiratory management/Ventilator_Mv(Pt)
    5003800013 : Respiratory management/Ventilator_Vt(Pt)
    5003800014 : Respiratory management/Ventilator_Vt(setting)
    5003800011 : Respiratory management/Ventilator_RR(Setting)
    5003800001 : Respiratory management/Ventilator_IP(Setting)
    5003800004 : Respiratory management/Ventilator_I:E(setting)
    5003800028 : Respiratory management/Ventilator_Pressure Trigger
    5003800027 : Respiratory management/Ventilator_Flow Trigger
    5003800007 : Respiratory management/Ventilator_Mv(Setting)
    5003800026 : Respiratory management/Ventilator_Plateau Pressure
    5003800012 : Respiratory management/Ventilator_Stroke volume
    5003800025 : Respiratory management/Ventilator 설정(Home)
    5003800030 : Respiratory management/Ventilator_EPAP
    5003800029 : Respiratory management/Ventilator_IPAP
    5003800024 : Respiratory management/Ventilator 설정(NIV)
    5003800003 : Respiratory management/Ventilator_MAP
    5003800035 : Respiratory management/Ventilator_Mv(Setting: %)
    5003800037 : Respiratory management/Ventilator 설정(Home NIV)


*** Ventilator (prescrition.csv) 

    Ventilator care (3hrs ~ 8hrs) : 시점이 00:00:00 으로 되어있는게 많아서 사용 x
    Ventilator care (12hrs ~ 1일) : 시점이 00:00:00 으로 되어있는게 많아서 사용 x
    Ventilator care (~3hrs) : 시점이 00:00:00 으로 되어있는게 많아서 사용 x
    Ventilator care (8hrs ~ 12hrs) : 시점이 00:00:00 으로 되어있는게 많아서 사용 x
    Ventilator care maintenance : 시점이 00:00:00 으로 되어있는게 많아서 사용 x


*** Extubation (prescription.csv)

    5P002_036 : Extubation


*** Surgery (surgery.csv)



### RENAL FAILURE

*** Creatinine (lab.csv : 처방코드)
    C375002 : Creatinine[Serum]
    5B001_19 : Creatinine (2hr)[Serum]
    5B00129 : Serum Creatini-ne for CCr[Serum]

*** pH (lab.csv : 처방코드)
    L000101202 : pH[Arterial Whole blood]
    L008901201 : pH[Venous Whole blood]
    L601007209 : pH[Capillary blood]
    L600101202 : pH[Arterial Whole blood]

*** Potassium (lab.csv : 처방코드)
    C379204 : K (Potassium)[Serum]

*** BUN (lab.csv : 처방코드)
    C373001 : BUN[Serum]

*** Urine Output (observation.csv : 임상관찰코드)
    4001600011 : 소변/Foley

*** Hemodialysis (prescription.csv)

    YO7020B_004 : Hemodialysis
    V10P0021 : Hemodialysis Cath 414002-JUGULAR 11.5FR 16CM (5EA/BOX)-30414-002 DUAL CVD/EA-COVIDIEN-(주)라온
    V10P0045 : Hemodialysis Cath 794009-JUGULAR 11.5FR 19.5CM (5EA/BOX-13794-009 DUAL CVD./EA-COVIDIEN-(주)라온
    V10P0022 : Hemodialysis Cath-6.5FR(1EA/1BOX)-소아용/EA-GAMBRO-박스터
    V10P0026 : Hemodialysis Cath-SUBCLAVIAN 20CM-DUAL STR./EA-BARD REYNOSA
    V09G0057 : Hemodialysis G/W 231001-J-TYPE (10EA/BOX)-13796-001/EA-COVIDIEN-(주)라온
    V09G0059 : Hemodialysis G/W/EA-BARD REYNOSA
    V09G0246 : Hemodialysis G/W-GDK-115J/EA-한국갬브로-박스터

*** ESRD (diagnosis.csv : 진단코드)

    DI024743 : End stage renal disease (Hemodialysis)(혈액투석중인 말기신장병)

*** CKD (diagnosis.csv : 진단코드)
    DI010115 : Chronic renal failure(만성 신장부전)
    DI050025 : Chronic kidney disease  stage 1(만성 신장병(1기))
    DI050026 : Chronic kidney disease  stage 2(만성 신장병(2기))
    DI050027 : Chronic kidney disease  stage 3(만성 신장병(3기))
    DI050028 : Chronic kidney disease  stage 4(만성 신장병(4기))
    DI050029 : Chronic kidney disease  stage 5(만성 신장병(5기))
    DI032358 : Chronic renal failure with exacerbation(만성신부전 악화)
    DI045702 : Chronic kidney disease  unspecified(상세불명의 만성 신장병)
    DI010107 : Acute renal failure(급성 신부전)
    DI010114 : Other chronic renal failure(기타 만성 콩팥(신장)기능상실)
    DI005316 : Chronic renal failure and hypertension(만성 신부전과 고혈압)


'''
