"""
기아자동차 FAQ 크롤링 후 DB 적재
- URL   : https://www.kia.com/kr/customer-service/center/faq
- 테이블 : tbl_kia_faq (cat, subject, content)
- 시작   : "차량 구매" 카테고리부터 (TOP 10 / 전체 제외)
- 페이지 : paging-list li.is-active 기준으로 마지막 페이지 판단
            마지막 li + 다음 버튼 있음  → 다음 페이지 그룹 이동
            마지막 li + 다음 버튼 없음  → 다음 카테고리 이동
- 카테고리: is-active 다음 li 로 순차 이동, 없으면 종료
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
URL            = "https://www.kia.com/kr/customer-service/center/faq"
START_CATEGORY = "차량 구매"          # 크롤링 시작 카테고리

TAB_LIST_SEL   = "#tab-list > li"    # 카테고리 탭 li 목록
ACCORDION_SEL  = "#accordion-specification"
PAGING_SEL     = "ul.paging-list > li"
NEXT_BTN_SEL   = "button.pagigation-btn-next"

PAGE_LOAD_WAIT = 10   # WebDriverWait 최대 대기(초)
CLICK_SLEEP    = 2    # 클릭 후 로딩 대기(초)


# ──────────────────────────────────────────────
# 헬퍼
# ──────────────────────────────────────────────
def _scrape_current_page(driver):
    """현재 페이지의 FAQ 항목 (subject, content) 리스트 반환"""
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    accordion = soup.select_one(ACCORDION_SEL)
    if accordion is None:
        return []

    items = []
    for row in accordion.select("div.cmp-accordion__item"):
        subj_tag    = row.select_one("span.cmp-accordion__title")
        content_tag = row.select_one("div.cmp-accordion__panel")
        if subj_tag is None:
            continue
        items.append((
            subj_tag.text.strip(),
            content_tag.get_text(separator=" ", strip=True) if content_tag else "",
        ))
    return items


def _is_last_page(driver):
    """현재 활성 페이지 li 가 paging-list 의 마지막 li 인지 확인"""
    try:
        pages = driver.find_elements(By.CSS_SELECTOR, PAGING_SEL)
        if not pages:
            return True  # 페이지네이션 없음 → 단일 페이지
        active_indices = [i for i, p in enumerate(pages) if "is-active" in (p.get_attribute("class") or "")]
        if not active_indices:
            return True
        return active_indices[-1] == len(pages) - 1
    except Exception:
        return True


def _has_next_btn(driver):
    """다음 페이지 그룹 버튼 존재 여부 확인"""
    btns = driver.find_elements(By.CSS_SELECTOR, NEXT_BTN_SEL)
    return bool(btns)


def _click_next_page_item(driver):
    """paging-list 에서 is-active 다음 li 클릭"""
    pages = driver.find_elements(By.CSS_SELECTOR, PAGING_SEL)
    for i, p in enumerate(pages):
        if "is-active" in (p.get_attribute("class") or ""):
            if i + 1 < len(pages):
                pages[i + 1].find_element(By.TAG_NAME, "a").click()
            return


# ──────────────────────────────────────────────
# 크롤링
# ──────────────────────────────────────────────
def crawl_faq():
    """기아자동차 FAQ 전체 페이지를 크롤링하여 DataFrame 반환"""
    cat_list, subject_list, content_list = [], [], []

    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service)
    driver.set_window_size(1920, 1080)  # 반응형 탭 숨김 방지
    wait    = WebDriverWait(driver, PAGE_LOAD_WAIT)

    try:
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, TAB_LIST_SEL)))

        # ── 카테고리 탭 이름 수집 (BeautifulSoup) ──
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tab_names = [
            li.select_one("span.name").text.strip()
            for li in soup.select("#tab-list > li")
            if li.select_one("span.name")
        ]
        tab_els = driver.find_elements(By.CSS_SELECTOR, TAB_LIST_SEL)

        start_idx = next(
            (i for i, name in enumerate(tab_names) if name == START_CATEGORY),
            None
        )
        if start_idx is None:
            print(f"'{START_CATEGORY}' 카테고리를 찾을 수 없습니다.")
            return pd.DataFrame()

        cat_idx = start_idx
        while cat_idx < len(tab_names):
            # ── 카테고리 클릭 ──
            tab_els = driver.find_elements(By.CSS_SELECTOR, TAB_LIST_SEL)  # DOM 갱신 후 재조회
            cat_name = tab_names[cat_idx]
            btn = tab_els[cat_idx].find_element(By.CSS_SELECTOR, "button")
            btn.click()
            time.sleep(CLICK_SLEEP)
            print(f"\n[카테고리: {cat_name}] 시작")

            # ── 페이지 순회 ──
            page = 1
            while True:
                items = _scrape_current_page(driver)
                for subj, cont in items:
                    cat_list.append(cat_name)
                    subject_list.append(subj)
                    content_list.append(cont)
                print(f"  [page {page}] {len(items)}건 수집 (누적: {len(cat_list)}건)")

                last = _is_last_page(driver)

                if last:
                    if _has_next_btn(driver):
                        # 다음 페이지 그룹(예: 1~5 → 6~10)으로 이동
                        driver.find_element(By.CSS_SELECTOR, NEXT_BTN_SEL).click()
                        time.sleep(CLICK_SLEEP)
                        page += 1
                    else:
                        # 이 카테고리의 마지막 페이지 → 다음 카테고리
                        break
                else:
                    # 현재 그룹 내 다음 페이지 li 클릭
                    _click_next_page_item(driver)
                    time.sleep(CLICK_SLEEP)
                    page += 1

            cat_idx += 1  # 다음 카테고리

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
    """크롤링한 DataFrame을 tbl_kia_faq 테이블에 일괄 INSERT"""
    if df.empty:
        print("적재할 데이터가 없습니다.")
        return

    query = "INSERT INTO tbl_kia_faq (cat, subject, content) VALUES (%s, %s, %s)"
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
