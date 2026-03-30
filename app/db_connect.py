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
        try:
            df = pd.read_sql(query, self.conn, params=params)
            return df
        except Exception as e:
            print(f"데이터프레임 변환 오류: {e}")
            return pd.DataFrame()

    def get_analysis_current_month(self, stat_ym):
        """선택한 기간의 연료 가격과 자동차 등록 대수 간 당월 데이터 확인"""
        query = """
            SELECT
                cr.CODE_NM AS REGION_NM,
                cf.CODE_NM AS FUEL_NM,
                ct.CODE_NM AS TYPE_NM,
                cu.CODE_NM AS USAGE_NM,
                s.REG_CNT,
                p.AVG_PRICE
            FROM TBL_FUEL_REG_STAT s
            LEFT JOIN TBL_FUEL_PRICE p
                ON s.REGION_CD = p.REGION_CD 
               AND s.FUEL_CD = p.FUEL_CD
               AND p.STAT_YM = %s
            LEFT JOIN TB_COMMON_CODE cr 
                ON s.REGION_CD = cr.CODE AND cr.CODE_GROUP = 'REGION'
            LEFT JOIN TB_COMMON_CODE cf 
                ON s.FUEL_CD = cf.CODE AND cf.CODE_GROUP = 'FUEL'
            LEFT JOIN TB_COMMON_CODE ct 
                ON s.TYPE_CD = ct.CODE AND ct.CODE_GROUP = 'TYPE'
            LEFT JOIN TB_COMMON_CODE cu 
                ON s.USAGE_CD = cu.CODE AND cu.CODE_GROUP = 'USAGE'
            WHERE s.STAT_YM = %s
        """
        return self.get_query_data(query, (stat_ym, stat_ym))

    def get_analysis_next_month(self, stat_ym):
        """선택한 기간의 연료 가격과 1달 후 자동차 등록 대수 데이터 확인"""
        query = """
            SELECT
                cr.CODE_NM AS REGION_NM,
                cf.CODE_NM AS FUEL_NM,
                ct.CODE_NM AS TYPE_NM,
                cu.CODE_NM AS USAGE_NM,
                s.REG_CNT,
                p.AVG_PRICE
            FROM TBL_FUEL_REG_STAT s
            LEFT JOIN TBL_FUEL_PRICE p
                ON s.REGION_CD = p.REGION_CD 
               AND s.FUEL_CD = p.FUEL_CD
               AND p.STAT_YM = %s
            LEFT JOIN TB_COMMON_CODE cr 
                ON s.REGION_CD = cr.CODE AND cr.CODE_GROUP = 'REGION'
            LEFT JOIN TB_COMMON_CODE cf 
                ON s.FUEL_CD = cf.CODE AND cf.CODE_GROUP = 'FUEL'
            LEFT JOIN TB_COMMON_CODE ct 
                ON s.TYPE_CD = ct.CODE AND ct.CODE_GROUP = 'TYPE'
            LEFT JOIN TB_COMMON_CODE cu 
                ON s.USAGE_CD = cu.CODE AND cu.CODE_GROUP = 'USAGE'
            WHERE s.STAT_YM = DATE_FORMAT(STR_TO_DATE(CONCAT(%s, '01'), '%Y%m%d') + INTERVAL 1 MONTH, '%Y%m')
        """
        return self.get_query_data(query, (stat_ym, stat_ym))

    def get_analysis_month_after_next(self, stat_ym):
        """선택한 기간의 연료 가격과 2달 후 자동차 등록 대수 데이터 확인"""
        query = """
            SELECT
                cr.CODE_NM AS REGION_NM,
                cf.CODE_NM AS FUEL_NM,
                ct.CODE_NM AS TYPE_NM,
                cu.CODE_NM AS USAGE_NM,
                s.REG_CNT,
                p.AVG_PRICE
            FROM TBL_FUEL_REG_STAT s
            LEFT JOIN TBL_FUEL_PRICE p
                ON s.REGION_CD = p.REGION_CD 
               AND s.FUEL_CD = p.FUEL_CD
               AND p.STAT_YM = %s
            LEFT JOIN TB_COMMON_CODE cr 
                ON s.REGION_CD = cr.CODE AND cr.CODE_GROUP = 'REGION'
            LEFT JOIN TB_COMMON_CODE cf 
                ON s.FUEL_CD = cf.CODE AND cf.CODE_GROUP = 'FUEL'
            LEFT JOIN TB_COMMON_CODE ct 
                ON s.TYPE_CD = ct.CODE AND ct.CODE_GROUP = 'TYPE'
            LEFT JOIN TB_COMMON_CODE cu 
                ON s.USAGE_CD = cu.CODE AND cu.CODE_GROUP = 'USAGE'
            WHERE s.STAT_YM = DATE_FORMAT(STR_TO_DATE(CONCAT(%s, '01'), '%Y%m%d') + INTERVAL 2 MONTH, '%Y%m')
        """
        return self.get_query_data(query, (stat_ym, stat_ym))

    def get_period_options(self):
        """통계 연월(기간) 검색"""
        query = "SELECT DISTINCT STAT_YM FROM TBL_FUEL_PRICE ORDER BY STAT_YM DESC"
        return self.get_query_data(query)

    def get_fuel_options(self):
        """공통 코드 테이블에서 연료 유형 검색"""
        query = "SELECT CODE, CODE_NM AS CODE_NAME FROM TB_COMMON_CODE WHERE CODE_GROUP = 'FUEL' AND CODE NOT LIKE 'G_%' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

    def get_type_options(self):
        """공통 코드 테이블에서 차종 유형 검색"""
        query = "SELECT CODE, CODE_NM AS CODE_NAME FROM TB_COMMON_CODE WHERE CODE_GROUP = 'TYPE' AND CODE NOT LIKE 'G_%' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

    def get_usage_options(self):
        """공통 코드 테이블에서 차량 용도 검색"""
        query = "SELECT CODE, CODE_NM AS CODE_NAME FROM TB_COMMON_CODE WHERE CODE_GROUP = 'USAGE' AND CODE NOT LIKE 'G_%' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

    def get_region_options(self):
        """공통 코드 테이블에서 지역 검색"""
        query = "SELECT CODE, CODE_NM AS CODE_NAME FROM TB_COMMON_CODE WHERE CODE_GROUP = 'REGION' AND CODE NOT LIKE 'G_%' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)