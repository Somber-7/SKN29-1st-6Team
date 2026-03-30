import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv(dotenv_path='conf/.env')

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
}

class DB_connect:
    """데이터베이스 관리"""
    
    def __init__(self, config):
        self.config  = config
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """데이터베이스 연결"""
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print(f"{self.config['database']} 연결")
            return True
        
        except Error as e:
            print(f"연결 실패: {e}")
            return False
    
    def close(self):
        """연결 종료"""
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("연결 종료")
    
    def ensure_connection(self):
        """연결이 끊어졌는지 확인하고 끊어졌다면 재연결"""
        if self.conn is None or not self.conn.is_connected():
            self.connect()

    def execute(self, query, params=None):
        try:
            self.ensure_connection()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return True
        except Error as e:
            print(f"쿼리 오류: {e}")
            return False
            
    def commit(self):
        if self.conn:
            self.conn.commit()
            
    def get_query_data(self, query, params=None):
        """For SELECT"""
        self.ensure_connection()
        if self.cursor is None:
            print("데이터베이스 연결/커서가 없습니다.")
            return pd.DataFrame()
            
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
                
            rows = self.cursor.fetchall()
            cols = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
            df = pd.DataFrame(rows, columns=cols)
            return df
        except Exception as e:
            print(f"데이터 조회 및 변환 오류: {e}")
            return pd.DataFrame()

    def get_trend_analysis_data(self):
        """유가(휘발유/경유 기준선)와 전체 차량 등록 대수의 시계열 추세 조회"""
        query = """
            SELECT 
                s.STAT_YM,
                cr.CODE_NM AS REGION_NM,
                cf.CODE_NM AS FUEL_NM,
                ct.CODE_NM AS TYPE_NM,
                cu.CODE_NM AS USAGE_NM,
                s.REG_CNT,
                p_gas.AVG_PRICE AS GASOLINE_PRICE,
                p_diesel.AVG_PRICE AS DIESEL_PRICE
            FROM TBL_FUEL_REG_STAT s
            LEFT JOIN TBL_FUEL_PRICE p_gas 
                ON s.STAT_YM = p_gas.STAT_YM AND s.REGION_CD = p_gas.REGION_CD AND p_gas.FUEL_CD = 'F01'
            LEFT JOIN TBL_FUEL_PRICE p_diesel 
                ON s.STAT_YM = p_diesel.STAT_YM AND s.REGION_CD = p_diesel.REGION_CD AND p_diesel.FUEL_CD = 'F02'
            LEFT JOIN TBL_COMMON_CODE cr ON s.REGION_CD = cr.CODE AND cr.CODE_GROUP = 'REGION'
            LEFT JOIN TBL_COMMON_CODE cf ON s.FUEL_CD = cf.CODE AND cf.CODE_GROUP = 'FUEL'
            LEFT JOIN TBL_COMMON_CODE ct ON s.TYPE_CD = ct.CODE AND ct.CODE_GROUP = 'TYPE'
            LEFT JOIN TBL_COMMON_CODE cu ON s.USAGE_CD = cu.CODE AND cu.CODE_GROUP = 'USAGE'
            ORDER BY s.STAT_YM ASC
        """
        return self.get_query_data(query)

    def get_fuel_price_trend(self):
        """유가 추이 시각화를 위한 전체 유가 조회"""
        query = """
            SELECT 
                p.STAT_YM,
                cr.CODE_NM AS REGION_NM,
                cf.CODE_NM AS FUEL_NM,
                p.AVG_PRICE
            FROM TBL_FUEL_PRICE p
            LEFT JOIN TBL_COMMON_CODE cr ON p.REGION_CD = cr.CODE AND cr.CODE_GROUP = 'REGION'
            LEFT JOIN TBL_COMMON_CODE cf ON p.FUEL_CD = cf.CODE AND cf.CODE_GROUP = 'FUEL'
            ORDER BY p.STAT_YM ASC
        """
        return self.get_query_data(query)

    def get_period_options(self):
        """통계 연월(기간) 검색"""
        query = "SELECT DISTINCT STAT_YM FROM TBL_FUEL_PRICE ORDER BY STAT_YM DESC"
        return self.get_query_data(query)

    def get_fuel_price_options(self):
        """유가 데이터가 있는 연료 유형 검색 (휘발유, 경유)"""
        query = "SELECT CODE, CODE_NM AS CODE_NAME FROM TBL_COMMON_CODE WHERE CODE IN ('F01', 'F02') ORDER BY SORT_ORDER"
        return self.get_query_data(query)

    def get_fuel_options(self):
        """공통 코드 테이블에서 연료 유형 검색"""
        query = "SELECT CODE, CODE_NM AS CODE_NAME FROM TBL_COMMON_CODE WHERE CODE_GROUP = 'FUEL' AND CODE NOT LIKE 'G_%' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

    def get_type_options(self):
        """공통 코드 테이블에서 차종 유형 검색"""
        query = "SELECT CODE, CODE_NM AS CODE_NAME FROM TBL_COMMON_CODE WHERE CODE_GROUP = 'TYPE' AND CODE NOT LIKE 'G_%' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

    def get_usage_options(self):
        """공통 코드 테이블에서 차량 용도 검색"""
        query = "SELECT CODE, CODE_NM AS CODE_NAME FROM TBL_COMMON_CODE WHERE CODE_GROUP = 'USAGE' AND CODE NOT LIKE 'G_%' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

    def get_region_options(self):
        """공통 코드 테이블에서 지역 검색"""
        query = "SELECT CODE, CODE_NM AS CODE_NAME FROM TBL_COMMON_CODE WHERE CODE_GROUP = 'REGION' AND CODE NOT LIKE 'G_%' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

    def get_dashboard_tabs(self):
        """공통 코드 테이블에서 대시보드 탭 검색"""
        query = "SELECT CODE_NM AS CODE_NAME FROM TBL_COMMON_CODE WHERE CODE_GROUP = 'DASHBOARD' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

def get_fuel_registration_data(stat_ym):
    """지정된 연월의 연료별 차량 등록 현황 데이터를 조회."""
    query = """
        SELECT
            tcc.CODE_NM AS 연료,
            SUM(tfrs.REG_CNT) AS 등록대수
        FROM TBL_FUEL_REG_STAT tfrs
        JOIN TBL_COMMON_CODE tcc
            ON tfrs.FUEL_CD = tcc.CODE
        WHERE tcc.CODE_GROUP = 'FUEL' AND tfrs.STAT_YM = %s
        GROUP BY tfrs.FUEL_CD, tcc.CODE_NM
        ORDER BY 등록대수 DESC;
    """
    with DB_connect(DB_CONFIG) as db:
        df = db.get_query_data(query, (stat_ym,))
    return df

def get_type_registration_data(stat_ym):
    """지정된 연월의 차종별 차량 등록 현황 데이터를 조회합니다."""
    query = """
        SELECT
            tcc.CODE_NM AS 차종,
            SUM(tfrs.REG_CNT) AS 등록대수
        FROM TBL_FUEL_REG_STAT tfrs
        JOIN TBL_COMMON_CODE tcc
            ON tfrs.TYPE_CD = tcc.CODE
        WHERE tcc.CODE_GROUP = 'TYPE' AND tfrs.STAT_YM = %s
        GROUP BY tfrs.TYPE_CD, tcc.CODE_NM
        ORDER BY 등록대수 DESC;
    """
    with DB_connect(DB_CONFIG) as db:
        df = db.get_query_data(query, (stat_ym,))
    return df

def get_national_average_fuel_price_trend():
    """전국 월별 평균 유가(휘발유, 경유) 추이 데이터 조회"""
    query = """
        SELECT
            p.STAT_YM,
            cf.CODE_NM AS FUEL_NM,
            AVG(p.AVG_PRICE) AS AVG_PRICE
        FROM TBL_FUEL_PRICE p
        JOIN TBL_COMMON_CODE cf
            ON p.FUEL_CD = cf.CODE AND cf.CODE_GROUP = 'FUEL'
        WHERE cf.CODE_NM IN ('휘발유', '경유')
        GROUP BY p.STAT_YM, cf.CODE_NM
        ORDER BY p.STAT_YM ASC;
    """
    with DB_connect(DB_CONFIG) as db:
        df = db.get_query_data(query)
    return df


# ─────────────────────────────────────────────
# FAQ 조회 함수
# ─────────────────────────────────────────────

def get_faq_cat1_options(table: str) -> list:
    """대분류(cat1) 목록 조회 — cat1/cat2 구조 테이블용 (현대, 제네시스)"""
    query = f"SELECT DISTINCT cat1 FROM `{table}` ORDER BY cat1"
    with DB_connect(DB_CONFIG) as db:
        df = db.get_query_data(query)
    return df['cat1'].tolist() if not df.empty else []


def get_faq_cat2_options(table: str, cat1: str) -> list:
    """소분류(cat2) 목록 조회 — 선택된 cat1 기준, 빈 값 제외"""
    query = f"SELECT DISTINCT cat2 FROM `{table}` WHERE cat1 = %s AND cat2 != '' ORDER BY cat2"
    with DB_connect(DB_CONFIG) as db:
        df = db.get_query_data(query, (cat1,))
    return df['cat2'].tolist() if not df.empty else []


def get_faq_cat_options(table: str) -> list:
    """단일 카테고리(cat) 목록 조회 — cat 구조 테이블용 (기아, KGM)"""
    query = f"SELECT DISTINCT cat FROM `{table}` ORDER BY cat"
    with DB_connect(DB_CONFIG) as db:
        df = db.get_query_data(query)
    return df['cat'].tolist() if not df.empty else []


def get_faq_list_dual(
    table: str,
    cat1: str = None,
    cat2: str = None,
    keyword: str = '',
) -> list:
    """cat1/cat2 구조 테이블 FAQ 조회 (현대, 제네시스)"""
    conditions, params = [], []
    if cat1:
        conditions.append("cat1 = %s")
        params.append(cat1)
    if cat2:
        conditions.append("cat2 = %s")
        params.append(cat2)
    kw = keyword.strip()
    if kw:
        conditions.append("(subject LIKE %s OR content LIKE %s)")
        params.extend([f"%{kw}%", f"%{kw}%"])
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"SELECT cat1, cat2, subject, content FROM `{table}` {where} ORDER BY id"
    with DB_connect(DB_CONFIG) as db:
        df = db.get_query_data(query, tuple(params) if params else None)
    return df.to_dict('records') if not df.empty else []


def get_faq_list_single(
    table: str,
    cat: str = None,
    keyword: str = '',
) -> list:
    """단일 cat 구조 테이블 FAQ 조회 (기아, KGM)"""
    conditions, params = [], []
    if cat:
        conditions.append("cat = %s")
        params.append(cat)
    kw = keyword.strip()
    if kw:
        conditions.append("(subject LIKE %s OR content LIKE %s)")
        params.extend([f"%{kw}%", f"%{kw}%"])
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"SELECT cat, subject, content FROM `{table}` {where} ORDER BY id"
    with DB_connect(DB_CONFIG) as db:
        df = db.get_query_data(query, tuple(params) if params else None)
    return df.to_dict('records') if not df.empty else []