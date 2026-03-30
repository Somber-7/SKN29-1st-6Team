"""
KGM FAQ 크롤링 후 DB 적재
- URL  : https://www.kg-mobility.com/sr/online-center/faq
- 테이블: tbl_kgm_faq (cat, subject, content)
- 아코디언: div.accordion-item — 클릭 후 콘텐츠 로드
- 페이지네이션: "다음 페이지" 버튼 display:none 여부로 마지막 페이지 판단
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
URL = "https://www.kg-mobility.com/sr/online-center/faq"

ITEM_SEL     = "div.accordion-wrap div.accordion-item"  # FAQ 개별 항목
PAGING_SEL   = "ul.pagnation > li > button"             # 페이지 번호 버튼 전체

PAGE_LOAD_WAIT = 10  # WebDriverWait 최대 대기(초)
CLICK_SLEEP    = 1   # 클릭 후 대기(초)


# ──────────────────────────────────────────────
# 헬퍼
# ──────────────────────────────────────────────
def _scrape_current_page(driver):
    """
    현재 페이지 FAQ 항목 수집
    - 항목별 클릭 → 즉시 파싱 → 다음 항목 처리
    """
    results = []
    items_el = driver.find_elements(By.CSS_SELECTOR, ITEM_SEL)

    for i in range(len(items_el)):
        try:
            # 매 반복마다 DOM 재조회 (클릭 후 DOM 변경 대응)
            items_el = driver.find_elements(By.CSS_SELECTOR, ITEM_SEL)
            item = items_el[i]

            btn = item.find_element(By.CSS_SELECTOR, "button.cursor-zoom")
            btn.click()
            time.sleep(0.4)

            # 클릭 직후 해당 항목만 파싱
            soup = BeautifulSoup(item.get_attribute("outerHTML"), 'lxml')

            cat_tag  = soup.select_one("span.label-sticker")
            p_tags   = soup.select("button.cursor-zoom > p")
            subj_tag = next((p for p in p_tags if not p.select_one(".label-sticker")), None)
            cont_tag = soup.select_one(".accordion-body")

            if cat_tag is None or subj_tag is None:
                continue

            results.append((
                cat_tag.text.strip(),
                subj_tag.text.strip(),
                cont_tag.get_text(separator=" ", strip=True) if cont_tag else "",
            ))
        except Exception as e:
            print(f"  항목 {i+1} 파싱 오류: {e}")
            continue

    return results


def _is_last_page(driver):
    """'다음 페이지' 버튼이 display:none 이면 마지막 페이지"""
    try:
        btns = driver.find_elements(By.CSS_SELECTOR, PAGING_SEL)
        for btn in btns:
            if "다음 페이지" in btn.text:
                style = btn.get_attribute("style") or ""
                return "display: none" in style
        return True  # 버튼 없으면 단일 페이지
    except Exception:
        return True


def _click_next_page(driver):
    """active 다음 번호 버튼 클릭, 없으면 '다음 페이지' 버튼 클릭"""
    btns = driver.find_elements(By.CSS_SELECTOR, PAGING_SEL)
    # 숫자 버튼만 필터 (텍스트가 숫자인 것)
    num_btns = [b for b in btns if b.text.strip().isdigit()]
    for i, b in enumerate(num_btns):
        if "active" in (b.get_attribute("class") or ""):
            if i + 1 < len(num_btns):
                num_btns[i + 1].click()
                return
            break
    # 현재 그룹 마지막 번호 → '다음 페이지' 버튼 클릭
    for btn in btns:
        if "다음 페이지" in btn.text:
            style = btn.get_attribute("style") or ""
            if "display: none" not in style:
                btn.click()
            return


# ──────────────────────────────────────────────
# 크롤링
# ──────────────────────────────────────────────
def crawl_faq():
    """KGM FAQ 전체 페이지를 크롤링하여 DataFrame 반환"""
    cat_list, subject_list, content_list = [], [], []

    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service)
    driver.set_window_size(1920, 1080)
    wait    = WebDriverWait(driver, PAGE_LOAD_WAIT)

    try:
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ITEM_SEL)))

        page = 1
        while True:
            items = _scrape_current_page(driver)
            for cat, subj, cont in items:
                cat_list.append(cat)
                subject_list.append(subj)
                content_list.append(cont)
            print(f"[page {page}] {len(items)}건 수집 (누적: {len(cat_list)}건)")

            if _is_last_page(driver):
                print("마지막 페이지 도달. 크롤링 종료.")
                break

            _click_next_page(driver)
            time.sleep(CLICK_SLEEP)
            page += 1

    finally:
        driver.quit()

    df = pd.DataFrame({
        "cat"    : cat_list,
        "subject": subject_list,
        "content": content_list,
    })
    print(f"\n총 {len(df)}건 수집 완료.")
    return df


# ──────────────────────────────────────────────
# DB 적재
# ──────────────────────────────────────────────
def upload_faq(df):
    """크롤링한 DataFrame을 tbl_kgm_faq 테이블에 일괄 INSERT"""
    if df.empty:
        print("적재할 데이터가 없습니다.")
        return

    query = "INSERT INTO tbl_kgm_faq (cat, subject, content) VALUES (%s, %s, %s)"
    params = [
        (row["cat"], row["subject"], row["content"])
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