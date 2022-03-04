# YS_restrospective data labelling

----

* extract_item.py : 각 테이블에서 어떤 item(변수) 있는지 조회 하는 코드

* itemid_code.py : item 조회한 결과를 주석으로 저장해놓은 코드

* preprocessing.py : 사용할 item_code 만 선택해서 필요한 데이터만 추출하고, 통일된 column(key)의 DataFrame으로 추출하는 코드

* labelling.py : 전처리된 데이터 활용해서 각 질환별 라벨링 추출하는 코드 
  - 2/22 기준 호흡부전 라벨링 완료

      - Case 환자 : 1036명 (10,322건)

  - 2/22 기준 신부전 라벨링 완료

      - Case 환자 : 216명 (216건)


  - 2/28 기준 섬망 라벨링 완료
  
      - Case 환자: 887명(10,218건)
      - Control 환자: 1,711명 (11,362건)
      - UTA: 2,863건
      - ICU 입실기간 외에 측정 : 512건 (Pos 153건(18명), Neg 361건(15명))
      - RASS <= -4 : 14,611건

* Cr_baseline.py : Creatinine 의 baseline 추출하는 코드 (+ U/O Criteria, Dialysis 추출 코드 포함)

* Multi_label.py : 이벤트 시점을 기준으로 랜덤하게 3개의 시점 추출한 뒤, 임의로 추출된 Timepoints를 활용하여 멀티라벨링을 추출하는 코드

  - 3/4 기준 Random_Timestamp 추출 완료
  
      - Total Timepoints : 97,092
      
  - 3/4 기준 Multi-labelling 추출 완료

      - Total Events : Delirium (Pos 32,447, Neg 35,380) , Renal Failue (Pos 1,286, Neg 95,548), RESP Failure (Pos 33,878, Neg 62,522)
      - Excluded Events : Delirium (UTA 29,265) , Renal Failue (258), RESP Failure (692)
