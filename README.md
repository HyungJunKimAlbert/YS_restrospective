# YS_restrospective data labelling

----

* extract_item.py : 각 테이블에서 어떤 item(변수) 있는지 조회 하는 코드

* itemid_code.py : item 조회한 결과를 주석으로 저장해놓은 코드

* preprocessing.py : 사용할 item_code 만 선택해서 필요한 데이터만 추출하고, 통일된 column(key)의 DataFrame으로 추출하는 코드

* labelling.py : 전처리된 데이터 활용해서 각 질환별 라벨링 추출하는 코드 
  - 2/22 기준 호흡부전, 신부전 이벤트 추출 가능
  - 2/28 섬망 라벨링 추가하였음. (Case 환자: 905명(10,371건), Control 환자: 1,726명 (11,722건), UTA: 2,863, RASS <= -4 : 14,611)

* Cr_baseline.py : Creatinine 의 baseline 추출하는 코드 (+ U/O Criteria, Dialysis 추출 코드 포함)

* Random_timestamp.py : 실제 이벤트 발생한 시점을 기준으로 직전 3시간 내의 시점 3개를 임의로 추출하는 코드

* Multi_label.py : 임의로 추출된 Timepoints를 활용하여 멀티라벨링을 추출하는 코드
