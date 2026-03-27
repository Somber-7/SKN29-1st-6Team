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