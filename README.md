# 에너지 가격 변동이 모빌리티 시장에 미치는 영향 분석
> **전국 5개년 유가 흐름에 따른 하이브리드·전기차 등 5가지 연료 타입별 차량 등록 패턴 도출**

## 팀 소개
| <img src="image/3_idots_1.png"> | <img src="image/3_idots_2.png"> |<img src="image/3_idots_3.png">  | 
| :---: | :---: | :---: |
|한경찬|임준|우석현|

**개발 기간:** 2026.03.30 - 2026.03.31 (총 2일)

## 프로젝트 개요

### 1. 주제

### 2. 선정 배경

### 3. 프로젝트 목표

- ---

## 기술 스택 (Tech Stack)
- **Language:** `Python 3.10+`
- **Database:** `MySQL`
- **Web Framework:** `Streamlit`
- **Visualization:** `Plotly`

## 사용한 데이터
국도교통 통계누리 - 자동차등록현황보고 (Total Registered Motor Vehicles)
<br>https://stat.molit.go.kr/portal/cate/statMetaView.do?hRsId=58

한국석유공사(오피넷) - 년도별 주유소 평균판매유가
<br>https://www.opinet.co.kr/user/dopospdrg/dopOsPdrgSelect.do


## 파일구조

```text
SKN29-1st-6Team/
├── app/
│   ├── dashboard.py         # 데이터 시각화 대시보드 페이지
│   ├── db_connect.py        # 데이터베이스 연결 및 세션 관리
│   ├── introduce.py         # 프로젝트 소개 및 팀원 안내 페이지
│   ├── question.py          # 사용자 질문/답변(Q&A) 페이지
│   └── utils.py             # 공통 유틸리티 함수 모듈
├── data/
│   ├── crawling_genesis.py  # 제네시스 데이터 크롤링 스크립트
│   ├── crawling_hyundai.py  # 현대 데이터 크롤링 스크립트
│   ├── crawling_kgm.py      # KGM 데이터 크롤링 스크립트
│   ├── crawling_kia.py      # 기아 데이터 크롤링 스크립트
│   ├── data_upload.py       # 수집 데이터를 DB에 업로드하는 스크립트
│   ├── price_upload.py      # 유가 정보를 DB에 업로드하는 스크립트
│   └── xlsx/                # 월별 자동차 등록 통계 및 유가 데이터 (Raw Data)
├── image/
│   ├── main.png             # 메인 화면 내 사용 이미지
│   ├── img_ex2.png          # 앱 내 사용 예시 이미지 2
│   ├── img_ex3.jpg          # 앱 내 사용 예시 이미지 3
│   └── img_ex4.jpg          # 앱 내 사용 예시 이미지 4
├── output/
│   ├── 테이블명세서_데이터베이스설계문서.xlsx  # DB 테이블 명세서
│   └── ERD_수집데이터.png      # 데이터베이스 ERD 다이어그램
├── sql/
│   ├── faq_data.sql         # FAQ 초기 데이터 SQL
│   ├── faq_table.sql        # FAQ 테이블 생성 SQL
│   ├── tbl_fuel_price.sql   # 유가 테이블 생성 SQL
│   ├── tbl_fuel_reg_stat.sql # 자동차 등록 통계 테이블 생성 SQL
│   └── vehicle_stats.sql    # 차량 통계 테이블 생성 SQL
├── .gitignore               # Git에서 추적하지 않을 파일/폴더 목록
├── README.md                # 프로젝트 관련 상세 설명 문서
└── main.py                  # Streamlit 메인 실행 파일
```

## 데이터베이스 구조

<img src="output/ERD_수집데이터.png" alt="ERD 다이어그램" width="800">

- ---
### 4. 프로젝트 결과
- 
- 
- 