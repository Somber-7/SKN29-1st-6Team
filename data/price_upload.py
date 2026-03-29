"""
주유소 지역별 월간 평균 판매가격 데이터를 TBL_FUEL_PRICE 테이블에 적재
- 대상 연료: 휘발유(F01), 경유(F02)
- 원천 파일: 휘발유_지역별_평균판매가격.xlsx, 경유_지역별_평균판매가격.xlsx
- 단위: 원/리터
- ON DUPLICATE KEY UPDATE 로 재실행 안전
"""

import os
import re
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import openpyxl

# ──────────────────────────────────────────────
# .env 로드 (conf/.env)
# ──────────────────────────────────────────────
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'conf', '.env'))

DB_CONFIG = {
    'host'     : os.getenv('DB_HOST'),
    'user'     : os.getenv('DB_USER'),
    'passwd'   : os.getenv('DB_PASSWORD'),
    'database' : os.getenv('DB_NAME'),
    'port'     : int(os.getenv('DB_PORT', 3306)),
}

# ──────────────────────────────────────────────
# 처리 대상 파일 정의
# ──────────────────────────────────────────────
XLSX_DIR = os.path.join(os.path.dirname(__file__), 'xlsx')

TARGET_FILES = [
    ('휘발유_지역별_평균판매가격.xlsx', 'F01'),
    ('경유_지역별_평균판매가격.xlsx',  'F02'),
]

BATCH_SIZE = 1000

# ──────────────────────────────────────────────
# 지역명 → 지역코드 매핑
# ──────────────────────────────────────────────
REGION_NM_MAP = {
    '서울': 'R01', '부산': 'R02', '대구': 'R03', '인천': 'R04',
    '광주': 'R05', '대전': 'R06', '울산': 'R07', '세종': 'R08',
    '경기': 'R09', '강원': 'R10', '충북': 'R11', '충남': 'R12',
    '전북': 'R13', '전남': 'R14', '경북': 'R15', '경남': 'R16',
    '제주': 'R17',
}


def parse_stat_ym(value: str) -> str | None:
    """
    날짜 문자열에서 YYYYMM 추출.
    '2021년01월' → '202101'
    '21년01월'   → '202101'  (2자리 연도는 2000년대로 처리)
    """
    # \xa0 (non-breaking space) 제거 후 처리
    s = str(value).replace('\xa0', '').strip()
    m = re.search(r'(\d{4})년(\d{2})월', s)
    if m:
        return m.group(1) + m.group(2)
    # 2자리 연도 (LPG 파일 형식)
    m2 = re.search(r'(\d{2})년(\d{2})월', s)
    if m2:
        return '20' + m2.group(1) + m2.group(2)
    return None


def parse_sheet(ws, fuel_cd: str) -> list[tuple]:
    """
    시트에서 데이터 행 파싱.
    - 헤더 행에서 지역명 → 컬럼 인덱스 매핑
    - 데이터 행: (STAT_YM, FUEL_CD, REGION_CD, AVG_PRICE)
    """
    records = []
    col_region_map = {}   # {col_index: REGION_CD}
    header_found = False

    for row in ws.iter_rows(values_only=True):
        if not row or row[0] is None:
            continue

        first = str(row[0]).replace('\xa0', '').strip()

        # 헤더 행 감지: 첫 셀이 '구분' 또는 '기간'
        if not header_found and first in ('구분', '기간'):
            for col_idx, cell in enumerate(row):
                if cell is None:
                    continue
                region_nm = str(cell).strip()
                if region_nm in REGION_NM_MAP:
                    col_region_map[col_idx] = REGION_NM_MAP[region_nm]
            header_found = True
            continue

        if not header_found:
            continue

        # 데이터 행: 첫 셀이 날짜 형식
        stat_ym = parse_stat_ym(first)
        if not stat_ym:
            continue

        for col_idx, region_cd in col_region_map.items():
            val = row[col_idx] if col_idx < len(row) else None
            if val is None:
                continue
            try:
                avg_price = round(float(val), 2)
            except (ValueError, TypeError):
                continue
            records.append((stat_ym, fuel_cd, region_cd, avg_price))

    return records


def ensure_table(cursor):
    """TBL_FUEL_PRICE 테이블이 없으면 생성"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_FUEL_PRICE (
            STAT_YM    CHAR(6)       NOT NULL COMMENT '통계년월 (YYYYMM)',
            FUEL_CD    VARCHAR(10)   NOT NULL COMMENT '연료코드 (F01:휘발유 / F02:경유)',
            REGION_CD  VARCHAR(10)   NOT NULL COMMENT '지역코드',
            AVG_PRICE  DECIMAL(8, 2) NOT NULL COMMENT '평균 판매가격 (원/리터)',
            CREATED_AT DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UPDATED_AT DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (STAT_YM, FUEL_CD, REGION_CD),
            INDEX IDX_FUELPRICE_YM     (STAT_YM),
            INDEX IDX_FUELPRICE_FUEL   (FUEL_CD),
            INDEX IDX_FUELPRICE_REGION (REGION_CD)
        ) ENGINE=InnoDB
          DEFAULT CHARSET=utf8mb4
          COLLATE=utf8mb4_unicode_ci
          COMMENT='주유소 지역별 월간 평균 판매가격 (원/리터)'
    """)


def batch_upsert(cursor, records: list[tuple]) -> int:
    """1000건 단위 배치 INSERT ... ON DUPLICATE KEY UPDATE"""
    sql = """
        INSERT INTO TBL_FUEL_PRICE
            (STAT_YM, FUEL_CD, REGION_CD, AVG_PRICE)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            AVG_PRICE  = VALUES(AVG_PRICE),
            UPDATED_AT = CURRENT_TIMESTAMP
    """
    total = 0
    for i in range(0, len(records), BATCH_SIZE):
        chunk = records[i:i + BATCH_SIZE]
        cursor.executemany(sql, chunk)
        total += len(chunk)
    return total


def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    conn.autocommit = False

    try:
        cursor = conn.cursor()
        ensure_table(cursor)
        conn.commit()
        cursor.close()

        total_inserted = 0
        for fname, fuel_cd in TARGET_FILES:
            fpath = os.path.join(XLSX_DIR, fname)
            if not os.path.exists(fpath):
                print(f'[SKIP] 파일 없음: {fname}')
                continue

            wb = openpyxl.load_workbook(fpath, read_only=True, data_only=True)
            ws = wb.active
            records = parse_sheet(ws, fuel_cd)
            wb.close()

            if not records:
                print(f'[SKIP] 유효 데이터 없음: {fname}')
                continue

            cursor = conn.cursor()
            cnt = batch_upsert(cursor, records)
            cursor.close()
            conn.commit()
            total_inserted += cnt
            print(f'[OK] {fname}  ({cnt}건 처리)')

        print(f'\n완료: 총 {total_inserted}건 처리')

    except Error as e:
        conn.rollback()
        print(f'[ERROR] {e}')
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    main()
