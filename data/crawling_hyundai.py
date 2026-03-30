"""
현대자동차 FAQ 크롤링 후 DB 적재
- URL  : https://www.hyundai.com/kr/ko/faq.html
- 테이블: tbl_hyundai_faq (cat1, cat2, subject, content)
- 페이지네이션: 다음 버튼 비활성화(class=disabled) 감지 시 종료
"""

import os
import sys
import time

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
load_dotenv(dotenv_path = "../conf/.env")

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
URL = "https://www.hyundai.com/kr/ko/faq.html"

ACCORDION_SEL = (
    "#contents > div.faq > div > div.section_white > div "
    "> div.result_area > div.ui_accordion.acc_01"
)
NEXT_BTN_SEL = (
    "#contents > div.faq > div > div.section_white > div "
    "> div.result_area > div.ui_paging.plugin-paging-apply "
    "> nav > button.navi.next"
)

PAGE_LOAD_WAIT = 10   # WebDriverWait 최대 대기(초)
CLICK_SLEEP    = 2    # 다음 페이지 클릭 후 대기(초)


# ──────────────────────────────────────────────
# 크롤링
# ──────────────────────────────────────────────
def crawl_faq() -> pd.DataFrame:
    """현대자동차 FAQ 전체 페이지를 크롤링하여 DataFrame 반환"""
    cat1_list, cat2_list, subject_list, content_list = [], [], [], []

    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service)

    try:
        driver.get(URL)

        # 첫 FAQ 항목이 로드될 때까지 명시적 대기
        wait = WebDriverWait(driver, PAGE_LOAD_WAIT)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui_accordion.acc_01")))

        page = 1
        while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            accordion = soup.select_one(ACCORDION_SEL)
            if accordion is None:
                print(f"[page {page}] FAQ 섹션을 찾을 수 없습니다. 선택자를 확인하세요.")
                break

            rows = accordion.select("dl")
            for row in rows:
                category_tag = row.select_one("b.title > i")
                if category_tag is None:
                    continue

                parts = category_tag.text.split(" > ")
                c1 = parts[0].replace("[", "").strip() if len(parts) > 0 else ""
                c2 = parts[1].replace("]", "").strip() if len(parts) > 1 else ""

                subj_tag    = row.select_one("b.title > .brief")
                content_tag = row.select_one(".exp")

                cat1_list.append(c1)
                cat2_list.append(c2)
                subject_list.append(subj_tag.text.strip()    if subj_tag    else "")
                content_list.append(content_tag.text.strip() if content_tag else "")

            print(f"[page {page}] {len(rows)}건 수집 (누적: {len(cat1_list)}건)")

            # 다음 버튼 비활성화 여부 — class 속성으로 판단 (is_enabled()는 JS disabled 미감지)
            next_btn = driver.find_element(By.CSS_SELECTOR, NEXT_BTN_SEL)
            btn_class = next_btn.get_attribute("class") or ""
            if "disabled" in btn_class:
                print("마지막 페이지 도달. 크롤링 종료.")
                break

            next_btn.click()
            time.sleep(CLICK_SLEEP)
            page += 1

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
def upload_faq(df: pd.DataFrame) -> None:
    """크롤링한 DataFrame을 faq 테이블에 일괄 INSERT"""
    if df.empty:
        print("적재할 데이터가 없습니다.")
        return

    query = "INSERT INTO tbl_hyundai_faq (cat1, cat2, subject, content) VALUES (%s, %s, %s, %s)"
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
