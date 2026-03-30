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
    
    def execute(self, query, params=None):
        try:
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
        try:
            df = pd.read_sql(query, self.conn, params=params)
            return df
        except Exception as e:
            print(f"데이터프레임 변환 오류: {e}")
            return pd.DataFrame()

    def get_analysis_current_month(self):
        """연료 가격과 자동차 등록 대수 간 당월 데이터 확인"""
        query = """
            SELECT
                p.STAT_YM AS PRICE_STAT_YM,
                p.REGION_CD,
                p.FUEL_CD AS PRICE_FUEL_CD,
                p.AVG_PRICE,
                s.STAT_YM AS REG_STAT_YM,
                s.TYPE_CD AS VHC_TYPE_CD,
                s.FUEL_CD AS REG_FUEL_CD,
                s.REG_CNT
            FROM TBL_FUEL_PRICE p
            JOIN TBL_FUEL_REG_STAT s
                ON p.REGION_CD = s.REGION_CD AND p.STAT_YM = s.STAT_YM
        """
        return self.get_query_data(query)

    def get_analysis_next_month(self):
        """연료 가격과 자동차 등록 대수 간 1달 후 데이터 확인"""
        query = """
            SELECT
                p.STAT_YM AS PRICE_STAT_YM,
                p.REGION_CD,
                p.FUEL_CD AS PRICE_FUEL_CD,
                p.AVG_PRICE,
                s.STAT_YM AS REG_STAT_YM,
                s.TYPE_CD AS VHC_TYPE_CD,
                s.FUEL_CD AS REG_FUEL_CD,
                s.REG_CNT
            FROM TBL_FUEL_PRICE p
            JOIN TBL_FUEL_REG_STAT s
                ON p.REGION_CD = s.REGION_CD AND p.STAT_YM = DATE_FORMAT(STR_TO_DATE(CONCAT(s.STAT_YM, '01'), '%Y%m%d') - INTERVAL 1 MONTH, '%Y%m')
        """
        return self.get_query_data(query)

    def get_analysis_month_after_next(self):
        """연료 가격과 자동차 등록 대수 간 2달 후 데이터 확인"""
        query = """
            SELECT
                p.STAT_YM AS PRICE_STAT_YM,
                p.REGION_CD,
                p.FUEL_CD AS PRICE_FUEL_CD,
                p.AVG_PRICE,
                s.STAT_YM AS REG_STAT_YM,
                s.TYPE_CD AS VHC_TYPE_CD,
                s.FUEL_CD AS REG_FUEL_CD,
                s.REG_CNT
            FROM TBL_FUEL_PRICE p
            JOIN TBL_FUEL_REG_STAT s
                ON p.REGION_CD = s.REGION_CD AND p.STAT_YM = DATE_FORMAT(STR_TO_DATE(CONCAT(s.STAT_YM, '01'), '%Y%m%d') - INTERVAL 2 MONTH, '%Y%m')
        """
        return self.get_query_data(query)

    def get_fuel_options(self):
        """공통 코드 테이블에서 연료 유형 검색"""
        query = "SELECT CODE, CODE_NAME FROM tb_common_code WHERE GROUP_CD = 'FUEL' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

    def get_type_options(self):
        """공통 코드 테이블에서 차종 유형 검색"""
        query = "SELECT CODE, CODE_NAME FROM tb_common_code WHERE GROUP_CD = 'TYPE' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

    def get_usage_options(self):
        """공통 코드 테이블에서 차량 용도 검색"""
        query = "SELECT CODE, CODE_NAME FROM tb_common_code WHERE GROUP_CD = 'USAGE' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)

    def get_region_options(self):
        """공통 코드 테이블에서 지역 검색"""
        query = "SELECT CODE, CODE_NAME FROM tb_common_code WHERE GROUP_CD = 'REGION' ORDER BY SORT_ORDER, CODE"
        return self.get_query_data(query)