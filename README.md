# YS_restrospective data labelling

----

* extract_item.py : 각 테이블에서 어떤 item(변수) 있는지 조회 하는 코드

* itemid_code.py : item 조회한 결과를 주석으로 저장해놓은 코드

* preprocessing.py : 사용할 item_code 만 선택해서 필요한 데이터만 추출하고, 통일된 column(key)의 DataFrame으로 추출하는 코드

* labelling.py : 전처리된 데이터 활용해서 각 질환별 라벨링 추출하는 코드 
  - 2/22 기준 호흡부전, 신부전 이벤트 추출 가능

* Cr_baseline.py : Creatinine 의 baseline 추출하는 코드 (+ U/O Criteria, Dialysis 추출 코드 포함)
