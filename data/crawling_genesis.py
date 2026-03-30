"""
제네시스 FAQ 크롤링 후 DB 적재
- 테이블 : tbl_genesis_faq (cat1, cat2, subject, content)
- 구조   : 카테고리별 URL을 순회하여 각 페이지에서 전체 항목 수집
- cat1/2 : accordion-label "[차량 구매/일반]" 에서 파싱
"""

import os
import sys
import time
import re

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# ──────────────────────────────────────────────
# 환경 변수 로드
# ──────────────────────────────────────────────
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'conf', '.env'))

DB_CONFIG = {
    'host'    : os.getenv('DB_HOST'),
    'user'    : os.getenv('DB_USER'),
    'passwd'  : os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port'    : int(os.getenv('DB_PORT', 3306)),
}

# ──────────────────────────────────────────────
# 상수
# ──────────────────────────────────────────────
URL            = "https://www.genesis.com/kr/ko/support/faq/vehicle-purchase/faq_tab.html"
TAB_LIST_SEL   = ".cp-faq__tab-list > .cp-faq__tab-item"  # 서브탭 목록
ACCORDION_ITEM_SEL = "div.cp-faq__accordion-item"          # 개별 FAQ 항목

PAGE_LOAD_WAIT = 10  # WebDriverWait 최대 대기(초)
CLICK_SLEEP    = 2   # 클릭 후 로딩 대기(초)

# [차량 구매/일반] 또는 [정비예약] 패턴
CAT_PATTERN_2 = re.compile(r"^\[(.+?)/(.+?)\]$")  # cat1/cat2
CAT_PATTERN_1 = re.compile(r"^\[(.+?)\]$")         # cat1만


# ──────────────────────────────────────────────
# 헬퍼
# ──────────────────────────────────────────────
def _scrape_page(driver):
    """현재 페이지의 FAQ 항목 (cat1, cat2, subject, content) 리스트 반환"""
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    items = []
    for row in soup.select(ACCORDION_ITEM_SEL):
        label_tag   = row.select_one("strong.accordion-label")
        subj_tag    = row.select_one("p.accordion-title")
        content_tag = row.select_one("div.accordion-panel-inner")

        if label_tag is None or subj_tag is None:
            continue

        label_text = label_tag.get_text(strip=True)  # "[차량 구매/일반]" 또는 "[정비예약]"
        m2 = CAT_PATTERN_2.match(label_text)
        m1 = CAT_PATTERN_1.match(label_text)
        if m2:
            cat1 = m2.group(1).strip()
            cat2 = m2.group(2).strip()
        elif m1:
            cat1 = m1.group(1).strip()
            cat2 = ""
        else:
            cat1, cat2 = "", ""

        subject = subj_tag.get_text(strip=True)
        content = content_tag.get_text(separator=" ", strip=True) if content_tag else ""

        if subject:
            items.append((cat1, cat2, subject, content))
    return items


# ──────────────────────────────────────────────
# 크롤링
# ──────────────────────────────────────────────
def crawl_faq():
    """제네시스 FAQ 전체 카테고리를 크롤링하여 DataFrame 반환"""
    cat1_list, cat2_list, subject_list, content_list = [], [], [], []

    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service)
    driver.set_window_size(1920, 1080)
    wait    = WebDriverWait(driver, PAGE_LOAD_WAIT)

    try:
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, TAB_LIST_SEL)))

        # ── 서브탭 이름 수집 (BeautifulSoup) ──
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tab_names = [
            li.get_text(strip=True)
            for li in soup.select(TAB_LIST_SEL)
        ]
        print(f"서브탭 목록: {tab_names}")

        # ALL 제외한 서브탭 순회
        target_tabs = [(i, name) for i, name in enumerate(tab_names) if name.upper() != "ALL"]

        for tab_idx, cat_name in target_tabs:
            # 탭 내부 버튼 직접 클릭 (기아 크롤링 방식 동일)
            tab_els = driver.find_elements(By.CSS_SELECTOR, TAB_LIST_SEL)
            btn = tab_els[tab_idx].find_element(By.CSS_SELECTOR, "button, a")
            btn.click()
            time.sleep(CLICK_SLEEP)

            items = _scrape_page(driver)
            for c1, c2, subj, cont in items:
                cat1_list.append(c1)
                cat2_list.append(c2)
                subject_list.append(subj)
                content_list.append(cont)
            print(f"[{cat_name}] {len(items)}건 수집 (누적: {len(cat1_list)}건)")

    finally:
        driver.quit()

    df = pd.DataFrame({
        "cat1"   : cat1_list,
        "cat2"   : cat2_list,
        "subject": subject_list,
        "content": content_list,
    })
    print(f"\n총 {len(df)}건 수집 완료.")
    return df


# ──────────────────────────────────────────────
# DB 적재
# ──────────────────────────────────────────────
def upload_faq(df):
    """크롤링한 DataFrame을 tbl_genesis_faq 테이블에 일괄 INSERT"""
    if df.empty:
        print("적재할 데이터가 없습니다.")
        return

    query = "INSERT INTO tbl_genesis_faq (cat1, cat2, subject, content) VALUES (%s, %s, %s, %s)"
    params = [
        (row["cat1"], row["cat2"], row["subject"], row["content"])
        for _, row in df.iterrows()
    ]

    try:
        conn   = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.executemany(query, params)
        conn.commit()
        print(f"{cursor.rowcount}건 DB 적재 완료.")
    except Error as e:
        print(f"DB 오류: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


# ──────────────────────────────────────────────
# 메인
# ──────────────────────────────────────────────
if __name__ == "__main__":
    faq_df = crawl_faq()
    print(faq_df.head())
    upload_faq(faq_df)