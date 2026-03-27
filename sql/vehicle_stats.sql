-- ============================================================
-- DATABASE 생성
-- DB명  : vehicle_stats
-- 용도  : 차량 등록 통계 및 유가 데이터 관리
-- 문자셋: utf8mb4 (한글 및 이모지 완전 지원)
-- ============================================================
 
CREATE DATABASE IF NOT EXISTS vehicle_stats
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
 
USE vehicle_stats;

-- ============================================================
-- 공통코드 테이블 (TB_COMMON_CODE)
-- 대상: 연료(FUEL) / 차종(TYPE) / 용도(USAGE) / 지역(REGION)
-- 기준: 소계·집계·계 항목 제외 / 코드 약어 제외
-- ============================================================

-- ------------------------------------------------------------
-- 1. CREATE TABLE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS TB_COMMON_CODE (
    CODE_GROUP  VARCHAR(10)  NOT NULL COMMENT '대분류 그룹 (FUEL / TYPE / USAGE / REGION)',
    CODE        VARCHAR(10)  NOT NULL COMMENT '중분류 코드',
    PARENT_CODE VARCHAR(10)      NULL COMMENT '상위 코드 (대분류 그룹 코드)',
    CODE_NM     VARCHAR(100) NOT NULL COMMENT '코드명 (한글)',
    SORT_ORDER  INT          NOT NULL DEFAULT 0 COMMENT '정렬 순서',
    USE_YN      CHAR(1)      NOT NULL DEFAULT 'Y' COMMENT '사용 여부 (Y/N)',
    REMARK      VARCHAR(200)     NULL COMMENT '비고',
    CREATED_AT  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    UPDATED_AT  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    PRIMARY KEY (CODE_GROUP, CODE)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='공통코드 (연료/차종/용도/지역)';


-- ------------------------------------------------------------
-- 2. INSERT — 연료 (FUEL)
--    F01 휘발유 / F02 경유 / F03 전기
--    F04 하이브리드(휘발유+전기) / F05 하이브리드(경유+전기)
-- ------------------------------------------------------------
INSERT INTO TB_COMMON_CODE
    (CODE_GROUP, CODE, PARENT_CODE, CODE_NM, SORT_ORDER, USE_YN, REMARK)
VALUES
    ('FUEL', 'G_FUEL', NULL,     '연료',                   0, 'Y', '연료 대분류'),
    ('FUEL', 'F01',    'G_FUEL', '휘발유',                  1, 'Y', NULL),
    ('FUEL', 'F02',    'G_FUEL', '경유',                    2, 'Y', NULL),
    ('FUEL', 'F03',    'G_FUEL', '전기',                    3, 'Y', NULL),
    ('FUEL', 'F04',    'G_FUEL', '하이브리드(휘발유+전기)',  4, 'Y', '휘발유+전기 하이브리드'),
    ('FUEL', 'F05',    'G_FUEL', '하이브리드(경유+전기)',    5, 'Y', '경유+전기 하이브리드');


-- ------------------------------------------------------------
-- 3. INSERT — 차종 (TYPE)
--    T01 승용 / T02 승합 / T03 화물 / T04 특수
-- ------------------------------------------------------------
INSERT INTO TB_COMMON_CODE
    (CODE_GROUP, CODE, PARENT_CODE, CODE_NM, SORT_ORDER, USE_YN, REMARK)
VALUES
    ('TYPE', 'G_TYPE', NULL,     '차종', 0, 'Y', '차종 대분류'),
    ('TYPE', 'T01',    'G_TYPE', '승용', 1, 'Y', NULL),
    ('TYPE', 'T02',    'G_TYPE', '승합', 2, 'Y', NULL),
    ('TYPE', 'T03',    'G_TYPE', '화물', 3, 'Y', NULL),
    ('TYPE', 'T04',    'G_TYPE', '특수', 4, 'Y', NULL);


-- ------------------------------------------------------------
-- 4. INSERT — 용도 (USAGE)
--    U01 비사업용 / U02 사업용
-- ------------------------------------------------------------
INSERT INTO TB_COMMON_CODE
    (CODE_GROUP, CODE, PARENT_CODE, CODE_NM, SORT_ORDER, USE_YN, REMARK)
VALUES
    ('USAGE', 'G_USAGE', NULL,      '용도',    0, 'Y', '용도 대분류'),
    ('USAGE', 'U01',     'G_USAGE', '비사업용', 1, 'Y', NULL),
    ('USAGE', 'U02',     'G_USAGE', '사업용',   2, 'Y', NULL);


-- ------------------------------------------------------------
-- 5. INSERT — 지역 (REGION)
--    R01 서울 ~ R17 제주 (17개 시도, 합계 제외)
-- ------------------------------------------------------------
INSERT INTO TB_COMMON_CODE
    (CODE_GROUP, CODE, PARENT_CODE, CODE_NM, SORT_ORDER, USE_YN, REMARK)
VALUES
    ('REGION', 'G_REGION', NULL,       '전국', 0,  'Y', '지역 대분류'),
    ('REGION', 'R01',      'G_REGION', '서울', 1,  'Y', '서울특별시'),
    ('REGION', 'R02',      'G_REGION', '부산', 2,  'Y', '부산광역시'),
    ('REGION', 'R03',      'G_REGION', '대구', 3,  'Y', '대구광역시'),
    ('REGION', 'R04',      'G_REGION', '인천', 4,  'Y', '인천광역시'),
    ('REGION', 'R05',      'G_REGION', '광주', 5,  'Y', '광주광역시'),
    ('REGION', 'R06',      'G_REGION', '대전', 6,  'Y', '대전광역시'),
    ('REGION', 'R07',      'G_REGION', '울산', 7,  'Y', '울산광역시'),
    ('REGION', 'R08',      'G_REGION', '세종', 8,  'Y', '세종특별자치시'),
    ('REGION', 'R09',      'G_REGION', '경기', 9,  'Y', '경기도'),
    ('REGION', 'R10',      'G_REGION', '강원', 10, 'Y', '강원특별자치도'),
    ('REGION', 'R11',      'G_REGION', '충북', 11, 'Y', '충청북도'),
    ('REGION', 'R12',      'G_REGION', '충남', 12, 'Y', '충청남도'),
    ('REGION', 'R13',      'G_REGION', '전북', 13, 'Y', '전북특별자치도'),
    ('REGION', 'R14',      'G_REGION', '전남', 14, 'Y', '전라남도'),
    ('REGION', 'R15',      'G_REGION', '경북', 15, 'Y', '경상북도'),
    ('REGION', 'R16',      'G_REGION', '경남', 16, 'Y', '경상남도'),
    ('REGION', 'R17',      'G_REGION', '제주', 17, 'Y', '제주특별자치도');


-- ------------------------------------------------------------
-- 확인용 조회
-- ------------------------------------------------------------
-- SELECT CODE_GROUP, CODE, PARENT_CODE, CODE_NM, SORT_ORDER
-- FROM   TB_COMMON_CODE
-- ORDER  BY CODE_GROUP, SORT_ORDER;

