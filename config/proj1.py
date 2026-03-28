
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

load_dotenv()





st.set_page_config(page_title="앱 예제", layout="wide")

# -----------------------
# 상태 초기화
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "start"
if "detail_page" not in st.session_state:
    st.session_state.detail_page = None

# -----------------------
# 예시 데이터
# -----------------------
example_data = {
    "A": {"title": "세부 화면 A", "description": "예시 내용 A", "items": ["A1", "A2", "A3"]},
    "B": {"title": "세부 화면 B", "description": "예시 내용 B", "items": ["B1", "B2"]},
    "C": {"title": "세부 화면 C", "description": "예시 내용 C", "items": ["C1", "C2", "C3", "C4"]},
}

# -----------------------
# 네비게이션 헬퍼
# -----------------------
def go_to(page: str, detail: str | None = None):
    st.session_state.page = page
    st.session_state.detail_page = detail
    st.rerun()

# -----------------------
# 공통 네비게이션 (Home 버튼 통합)
# -----------------------
def render_top_nav():
    col1, col2, col3, _, home_col = st.columns([1, 1, 1, 5, 1])

    with col1:
        with st.popover("🏠 Home"):
            st.markdown("**홈 메뉴**")
            if st.button("📊 대시보드",  key="nav_home_1"): go_to("main")
            if st.button("🕐 최근 항목", key="nav_home_2"): go_to("main")
            if st.button("⭐ 즐겨찾기",  key="nav_home_3"): go_to("main")

    with col2:
        with st.popover("ℹ️ About"):
            st.markdown("**서비스 정보**")
            if st.button("📋 서비스 소개", key="nav_about_1"): st.info("서비스 소개 페이지")
            if st.button("👥 팀 소개",     key="nav_about_2"): st.info("팀 소개 페이지")
            if st.button("🔖 버전 정보",   key="nav_about_3"): st.info("v1.0.0")

    with col3:
        with st.popover("✉️ FAQ"):
            st.markdown("**문의하기**")
            if st.button("📧 이메일 문의", key="nav_contact_1"): st.info("contact@example.com")
            if st.button("📞 고객센터",    key="nav_contact_2"): st.info("02-1234-5678")
            if st.button("❓ FAQ",          key="nav_contact_3"): st.info("FAQ 페이지")

    with home_col:
        if st.button("🏠 Home", key="home_btn"):
            go_to("start")

# -----------------------
# 각 페이지 렌더링
# -----------------------
def page_start():
    st.markdown(
        "<h1 style='text-align:center; margin-top:150px;'>🚀 환영합니다!</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; font-size:20px; margin-bottom:50px;'>시작하려면 아래 버튼을 눌러주세요.</p>",
        unsafe_allow_html=True,
    )
    _, col, _ = st.columns([1, 2, 1])
    with col:
        if st.button("세부 화면으로 들어가기", use_container_width=True):
            go_to("main")

def page_main():
    render_top_nav()

    st.title("🏠 메인페이지")
    st.write("전국 자동차 등록 현황 대시보드의 메인 페이지입니다.")

    col1, col2 = st.columns(2)

    with col1:
        st.info("데이터 개요 및 프로젝트 소개 영역")
        if st.button("📊 분석페이지로 이동", use_container_width=True):
            go_to("analysis")

    with col2:
        st.info("자주 묻는 질문 및 사용 안내 영역")
        if st.button("❓ FAQ로 이동", use_container_width=True):
            go_to("faq")

# def page_main():
#     render_top_nav()  # ← 수정: render_home_button() + render_top_menu() → 통합

#     st.title("🏠 세부 화면 메인")
#     st.write("카드를 클릭해서 세부 내용을 확인하세요.")

#     col1, col2, col3 = st.columns(3)
#     if col1.button("세부 화면 A", use_container_width=True): go_to("detail", "A")
#     if col2.button("세부 화면 B", use_container_width=True): go_to("detail", "B")
#     if col3.button("세부 화면 C", use_container_width=True): go_to("detail", "C")

# ===== 분석 =====
def page_analysis():
    render_top_nav()

    with st.sidebar:
        st.header("분석 필터")

        selected_fuel = st.multiselect(
            "연료 선택",
            ["휘발유", "경유", "전기", "하이브리드(휘발유+전기)", "하이브리드(경유+전기)"]
        )

        selected_type = st.multiselect(
            "차종 선택",
            ["승용", "승합", "화물", "특수"]
        )

        selected_usage = st.multiselect(
            "용도 선택",
            ["비사업용", "사업용"]
        )

        selected_region = st.multiselect(
            "지역 선택",
            ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
             "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]
        )

    st.title("📊 분석페이지")
    st.write("선택한 조건에 따라 대시보드가 변경됩니다.")

    st.subheader("현재 선택 조건")
    st.write("연료:", selected_fuel if selected_fuel else "전체")
    st.write("차종:", selected_type if selected_type else "전체")
    st.write("용도:", selected_usage if selected_usage else "전체")
    st.write("지역:", selected_region if selected_region else "전체")

    st.container(border=True).write("KPI 카드 영역")
    st.container(border=True).write("차트 영역")
    st.container(border=True).write("상세 테이블 영역")

# def page_detail():
#     render_top_nav()  # ← 수정: 동일하게 통합

#     detail_key = st.session_state.detail_page
#     data = example_data.get(
#         detail_key,
#         {"title": "세부 화면", "description": "데이터 없음", "items": []},
#     )

#     with st.sidebar:
#         st.header(f"{data['title']} 메뉴")
#         menus = {
#             "A": ["A 메뉴 1", "A 메뉴 2"],
#             "B": ["B 메뉴 1", "B 메뉴 2"],
#             "C": ["C 메뉴 1", "C 메뉴 2", "C 메뉴 3"],
#         }
#         for i, label in enumerate(menus.get(detail_key, [])):
#             st.button(label, key=f"sidebar_{detail_key}_{i}")

#     st.title(f"📄 {data['title']}")
#     st.write(data["description"])

#     st.subheader("상품 목록")
#     for item in data["items"]:
#         st.write(f"- {item}")

#     if st.button("⬅️ 세부 화면 메인으로 돌아가기"):
#         go_to("main")


# -----------------------
# 라우터
# -----------------------
PAGE_MAP = {
    "start": page_start,
    "main": page_main,
    "analysis": page_analysis,
    #"faq": page_faq,
}

render_fn = PAGE_MAP.get(st.session_state.page)
if render_fn:
    render_fn()
else:
    st.error("알 수 없는 페이지입니다.")
    if st.button("홈으로"):
        go_to("start")







