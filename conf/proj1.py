
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

import streamlit as st

import streamlit as st

st.set_page_config(page_title="Team 6", layout="wide")

# -----------------------
# 전역 CSS (1회만 주입)
# -----------------------
def inject_global_css():
    st.markdown("""
    <style>
    /* 앱 전체 배경 */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #E3E7EB;
        color: #1f2937;          /* ← #E4E8EC → #1f2937 : 배경이 밝아서 텍스트 안 보이던 문제 수정 */
    }

    /* ── 헤더 ── */
    .custom-header {
        background: linear-gradient(180deg, #161A1F 0%, #24282D 55%, #4B5158 100%);
        padding: 24px 30px;
        border-radius: 16px;
        margin-bottom: 12px;
        color: white;
    }
    .custom-header h1 { margin: 0; font-size: 30px; }
    .custom-header p  { margin: 8px 0 0 0; font-size: 15px; opacity: 0.92; }

    /* ── 네비게이션 버튼 텍스트 ── */
    /* st-key- 방식으로 각 popover 안 버튼 타겟 */
    .st-key-nav_home_1 button, .st-key-nav_home_2 button, .st-key-nav_home_3 button,
    .st-key-nav_dash_1 button, .st-key-nav_dash_2 button,
    .st-key-nav_contact_1 button,
    .st-key-logo_to_main button {
        color: #1f3a5f !important;
        font-weight: 600;
    }

    /* ── 성공 메시지 ── */
    .custom-success {
        background: linear-gradient(90deg, #edf9f0, #e3f5e8);
        color: #1d4f38;
        padding: 16px 20px;
        border-radius: 14px;
        border: 1px solid #cfe9d8;
        font-size: 15px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 18px;
    }

    /* ── 메인 카드 ── */
    .st-key-main_card_1, .st-key-main_card_2, .st-key-main_card_3 {
        background: white;
        border: 1px solid #e8edf3;
        border-radius: 16px;
        padding: 18px 18px 12px 18px;
        box-shadow: 4px 4px 1px rgba(31,59,91,0.55);
        margin-bottom: 10px;
    }
    .card-title { font-size: 1.05rem; font-weight: 700; color: #1f3b5b; margin-bottom: 6px; }
    .card-desc  { color: #5f6b7a; font-size: 0.94rem; margin-bottom: 12px; }

    /* ── 세부 페이지 공통 ── */
    .page-hero {
        background: linear-gradient(180deg, #161A1F 0%, #24282D 55%, #4B5158 100%);
        color: white;
        padding: 32px 36px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 8px 20px rgba(31,59,91,0.10);
    }
    .page-hero-title { font-size: 2rem; font-weight: 800; margin-bottom: 8px; }
    .page-hero-desc  { font-size: 1rem; opacity: 0.95; line-height: 1.7; }

    .page-card {
        background: white;
        border: 1px solid #e6edf5;
        border-radius: 18px;
        padding: 22px 24px 18px 24px;
        box-shadow: 5px 5px 4px rgba(31,59,91,0.06);
        margin-bottom: 16px;
        height: 100%;
    }
    .page-card-title { font-size: 1.15rem; font-weight: 800; color: #1f3b5b; margin-bottom: 10px; }
    .page-card-body  { color: #4f5d6b; font-size: 0.97rem; line-height: 1.8; }

    .page-section {
        background: #f8fbfe;
        border: 1px solid #e6edf5;
        border-radius: 18px;
        padding: 22px 24px 18px 24px;
        box-shadow: 5px 5px 4px rgba(31,59,91,0.04);
        margin-bottom: 18px;
    }
    .page-section-title { font-size: 1.1rem; font-weight: 800; color: #1f3b5b; margin-bottom: 10px; }
    .page-section-body  { color: #556474; font-size: 0.96rem; line-height: 1.8; }

    .page-chip {
        display: inline-block;
        background: #eef4fb;
        color: #1f3b5b;
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------
# 상태 초기화
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "main"
if "detail_page" not in st.session_state:
    st.session_state.detail_page = None

inject_global_css()

# -----------------------
# 네비게이션 헬퍼
# -----------------------
def go_to(page: str, detail: str | None = None):
    st.session_state.page = page
    st.session_state.detail_page = detail
    st.rerun()

# -----------------------
# 공통 컴포넌트
# -----------------------
def custom_success(message: str):
    st.markdown(
        f'<div class="custom-success">✅ {message}</div>',
        unsafe_allow_html=True,
    )

def render_header():
    st.markdown("""
        <div class="custom-header">
            <h1>전국 자동차 등록 현황과 유가 변동</h1>
            <p>자동차 등록 데이터와 유가 변동을 탐색하고 비교하는 서비스</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

def render_top_nav():
    with st.container(border=False):
        col1, col2, col3, _,_,_,_,_, col4 = st.columns(9)

        with col1:
            with st.popover("📌 소개", use_container_width=True):
                if st.button("📘 서비스 소개", key="nav_home_1", use_container_width=True): go_to("intro")
                if st.button("🗂️ 데이터 설명", key="nav_home_2", use_container_width=True): go_to("data_guide")
                if st.button("👥 팀 소개",     key="nav_home_3", use_container_width=True): go_to("team")

        with col2:
            with st.popover("ℹ️ 현황", use_container_width=True):
                if st.button("📊 대시보드", key="nav_dash_1", use_container_width=True): go_to("dashboard")
                if st.button("📈 분석",     key="nav_dash_2", use_container_width=True): go_to("analysis")

        with col3:
            with st.popover("🔔 문의", use_container_width=True):
                if st.button("❓ FAQ", key="nav_contact_1", use_container_width=True): go_to("faq")

        # with col4:
        #     if st.button("🏠 Main", key="logo_to_main2", use_container_width=True):
        #         go_to("main")

def render_top_btn():
    """🔚 버튼 — 각 페이지 상단에서 시작화면으로"""
    _, col1 = st.columns([9, 1])
    with col1:
        if st.button("🏠", use_container_width=True, key="logo_to_main_btn", type="tertiary"):
            go_to("main")

# -----------------------
# 페이지: 시작화면
# -----------------------
# def page_start():
#     st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

#     k1, _, k3 = st.columns([2, 0.5, 1.3], gap="xsmall")
#     with k1:
#         st.image("config/assets/image/img_ex2.png", width=700)
#     with k3:
#         st.markdown("""
#         <div class="page-hero">
#             <div class="page-hero-title">자동차 등록 현황<br>& 유가 변동</div>
#             <div class="page-hero-desc">메모</div>
#         </div>
#         """, unsafe_allow_html=True)
#         if st.button("🚀 서비스 시작하기", key="start_go_main", use_container_width=True):
#             go_to("main")

# -----------------------
# 페이지: 메인
# -----------------------
def page_main():
    render_top_btn()
    render_header()
    render_top_nav()

    st.title("🚗 서비스 소개")
    st.write("상단 메뉴를 통해 원하는 기능으로 이동할 수 있습니다.")

    render_page_header("""
    <div class="page-hero">
        <div class="page-hero-title">📘 서비스 소개</div>
        <div class="page-hero-desc">
            전국 자동차 등록 현황과 유가 변동 데이터를 현황을 파악하고,
            탐색할 수 있도록 설계한 데이터 기반 서비스입니다.
        </div>
    </div>
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">🎯 프로젝트 목표</div>
            <div class="page-card-body">
                자동차 등록 데이터는 다양한 기준으로 구성되어 있어 단순한 표 형태만으로는
                전체 구조를 파악하기 어렵습니다.<br><br>
                본 프로젝트는 자동차 등록현황 데이터와 유가 변동 데이터를 함께 활용하여,
                사용자가 전반적인 현황과 두 데이터 사이 관계를 보다 쉽게 이해할 수 있는 것을 목표로 합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">⚠️ 문제 정의</div>
            <div class="page-card-body">
                자동차 등록 현황 데이터는 항목 수가 많고 분류 기준이 다양해
                원하는 정보를 직관적으로 찾기 어렵습니다.<br><br>
                또한 유가 변동은 차량 선택과 등록 흐름에 영향을 줄 수 있는 요인이지만,
                이를 함께 비교하고 해석할 수 있는 서비스는 제한적입니다.<br><br>
                따라서 본 서비스는 자동차 등록현황과 유가 가격을 함께 탐색할 수 있도록
                돕는 사용자 친화적 정보 구조 시스템을 채택하고 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-card">
        <div class="page-card-title">🧭 서비스 방향성</div>
        <div class="page-card-body">
            본 서비스는 사용자가 원하는 조건을 선택하고, 그 결과를 직관적인 시각화와 함께 확인할 수 있도록 설계하였습니다.<br><br>
            또한 전체 현황을 빠르게 이해할 수 있는 대시보드와 세부 조건별 탐색 기능을 분리하여
            정보 접근성과 활용성을 높이는 데 초점을 두었습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, title, body in zip(
        [c1, c2, c3, c4],
        ["직관성", "탐색성", "비교 가능성", "확장성"],
        [
            "복잡한 데이터를 한눈에 이해할 수 있도록 시각화 중심으로 구성",
            "사용자가 원하는 기준을 선택해 필요한 정보를 직접 조회 가능",
            "연료, 차종, 용도, 지역 기준으로 데이터를 비교하며 구조를 파악",
            "향후 기능 추가와 세부 분석 확장을 고려한 페이지 구조 설계",
        ],
    ):
        col.markdown(
            f'<div class="page-card"><div class="page-card-title">{title}</div>'
            f'<div class="page-card-body">{body}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("###")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class="page-section">
            <div class="page-section-title">🛠️ 주요 기능</div>
            <div class="page-section-body">
                • 대시보드 기반 전체 현황 확인<br>
                • 연료, 차종, 용도, 지역별 시각화 제공<br>
                • 유가 변동 추이 및 등록 대수 변화 비교<br>
                • 조건 선택을 통한 조회 및 분석 기능<br>
                • FAQ 및 데이터 설명 페이지 제공
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="page-section">
            <div class="page-section-title">✨ 기대 효과</div>
            <div class="page-section-body">
                • 자동차 등록 현황 데이터의 이해도 향상<br>
                • 다양한 기준의 빠른 비교 및 탐색 가능<br>
                • 복잡한 공공데이터의 접근성과 활용성 향상<br>
                • 사용자 중심의 탐색형 정보 서비스 구현
            </div>
        </div>
        """, unsafe_allow_html=True)

    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     with st.container(key="main_card_1"):
    #         st.markdown('<div class="card-title">📌 홈</div>', unsafe_allow_html=True)
    #         st.markdown('<div class="card-desc">전반적인 서비스 개요와<br>데이터 및 팀 구성을 소개합니다.</div>', unsafe_allow_html=True)
    # with col2:
    #     with st.container(key="main_card_2"):
    #         st.markdown('<div class="card-title">ℹ️ 현황</div>', unsafe_allow_html=True)
    #         st.markdown('<div class="card-desc">조건에 대한 데이터 현황과<br>간단한 분석을 할 수 있습니다.</div>', unsafe_allow_html=True)
    # with col3:
    #     with st.container(key="main_card_3"):
    #         st.markdown('<div class="card-title">🔔 문의</div>', unsafe_allow_html=True)
    #         st.markdown('<div class="card-desc">자주 묻는 질문을<br>확인합니다.</div>', unsafe_allow_html=True)

# -----------------------
# 공통 페이지 헤더 렌더러
# -----------------------
def render_page_header(hero_html: str):
    """🔝 버튼 → hero → nav → divider 순서로 렌더링"""
    render_top_btn()
    st.markdown(hero_html, unsafe_allow_html=True)
    render_top_nav()
    st.divider()

# -----------------------
# 페이지: 서비스 소개
# -----------------------
def page_intro():
    render_page_header("""
    <div class="page-hero">
        <div class="page-hero-title">📘 서비스 소개</div>
        <div class="page-hero-desc">
            전국 자동차 등록 현황과 유가 변동 데이터를 현황을 파악하고,
            탐색할 수 있도록 설계한 데이터 기반 서비스입니다.
        </div>
    </div>
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">🎯 프로젝트 목표</div>
            <div class="page-card-body">
                자동차 등록 데이터는 다양한 기준으로 구성되어 있어 단순한 표 형태만으로는
                전체 구조를 파악하기 어렵습니다.<br><br>
                본 프로젝트는 자동차 등록현황 데이터와 유가 변동 데이터를 함께 활용하여,
                사용자가 전반적인 현황과 두 데이터 사이 관계를 보다 쉽게 이해할 수 있는 것을 목표로 합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">⚠️ 문제 정의</div>
            <div class="page-card-body">
                자동차 등록 현황 데이터는 항목 수가 많고 분류 기준이 다양해
                원하는 정보를 직관적으로 찾기 어렵습니다.<br><br>
                또한 유가 변동은 차량 선택과 등록 흐름에 영향을 줄 수 있는 요인이지만,
                이를 함께 비교하고 해석할 수 있는 서비스는 제한적입니다.<br><br>
                따라서 본 서비스는 자동차 등록현황과 유가 가격을 함께 탐색할 수 있도록
                돕는 사용자 친화적 정보 구조 시스템을 채택하고 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-card">
        <div class="page-card-title">🧭 서비스 방향성</div>
        <div class="page-card-body">
            본 서비스는 사용자가 원하는 조건을 선택하고, 그 결과를 직관적인 시각화와 함께 확인할 수 있도록 설계하였습니다.<br><br>
            또한 전체 현황을 빠르게 이해할 수 있는 대시보드와 세부 조건별 탐색 기능을 분리하여
            정보 접근성과 활용성을 높이는 데 초점을 두었습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, title, body in zip(
        [c1, c2, c3, c4],
        ["직관성", "탐색성", "비교 가능성", "확장성"],
        [
            "복잡한 데이터를 한눈에 이해할 수 있도록 시각화 중심으로 구성",
            "사용자가 원하는 기준을 선택해 필요한 정보를 직접 조회 가능",
            "연료, 차종, 용도, 지역 기준으로 데이터를 비교하며 구조를 파악",
            "향후 기능 추가와 세부 분석 확장을 고려한 페이지 구조 설계",
        ],
    ):
        col.markdown(
            f'<div class="page-card"><div class="page-card-title">{title}</div>'
            f'<div class="page-card-body">{body}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("###")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class="page-section">
            <div class="page-section-title">🛠️ 주요 기능</div>
            <div class="page-section-body">
                • 대시보드 기반 전체 현황 확인<br>
                • 연료, 차종, 용도, 지역별 시각화 제공<br>
                • 유가 변동 추이 및 등록 대수 변화 비교<br>
                • 조건 선택을 통한 조회 및 분석 기능<br>
                • FAQ 및 데이터 설명 페이지 제공
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="page-section">
            <div class="page-section-title">✨ 기대 효과</div>
            <div class="page-section-body">
                • 자동차 등록 현황 데이터의 이해도 향상<br>
                • 다양한 기준의 빠른 비교 및 탐색 가능<br>
                • 복잡한 공공데이터의 접근성과 활용성 향상<br>
                • 사용자 중심의 탐색형 정보 서비스 구현
            </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------
# 페이지: 데이터 설명
# -----------------------
def page_data_guide():
    render_page_header("""
    <div class="page-hero">
        <div class="page-hero-title">🗂️ 데이터 설명</div>
        <div class="page-hero-desc">
            본 페이지는 서비스에서 활용하는 자동차 등록 현황 데이터와<br>유가 변동 데이터의
            구성 항목 및 분류 기준을 안내하기 위한 페이지입니다.
        </div>
    </div>
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">⛽ 연료 기준</div>
            <div class="page-card-body">
                본 서비스에서는 차량을 연료 유형에 따라 분류하여 현황을 제공합니다.<br><br>
                • 휘발유 • 경유 • 전기<br>
                • 하이브리드(휘발유+전기)<br>
                • 하이브리드(경유+전기)<br><br>
                이를 통해 친환경차와 내연기관차의 구성 차이를 비교할 수 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">🚘 차종 기준</div>
            <div class="page-card-body">
                차량은 용도와 형태에 따라 차종별로 분류됩니다.<br><br>
                • 승용 • 승합 • 화물 • 특수<br><br>
                이를 통해 차량 유형별 등록 현황과 분포를 확인할 수 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">🏷️ 용도 기준</div>
            <div class="page-card-body">
                차량은 사용 목적에 따라 용도로도 구분됩니다.<br><br>
                • 비사업용 • 사업용<br><br>
                이를 통해 일반 개인 및 기업·운송 목적 차량의 구성을 비교할 수 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">🗺️ 지역 기준</div>
            <div class="page-card-body">
                지역 기준은 전국 17개 시도를 중심으로 구성됩니다.<br><br>
                • 시: 서울, 부산, 인천, 대구, 대전, 광주, 울산, 세종<br>
                • 도: 경기, 충북, 충남, 전남, 경북, 경남, 강원, 전북, 제주<br><br>
                이를 통해 지역별 자동차 등록 규모와 분포를 비교할 수 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("###")
    st.markdown("""
    <div class="page-section">
        <div class="page-section-title">📌 데이터 활용 방식</div>
        <div class="page-section-body">
            본 서비스는 위와 같은 연료, 차종, 용도, 지역 기준을 기반으로
            자동차 등록 현황을 시각화하고 비교할 수 있도록 구성되어 있습니다.<br><br>
            대시보드 페이지에서는 각 기준별 전체 흐름을 확인할 수 있으며,
            분석 페이지에서는 여러 조건을 조합하여 보다 구체적인 현황을 탐색할 수 있습니다.
        </div>
    </div>
    <div class="page-section">
        <div class="page-section-title">🔎 해석 시 참고사항</div>
        <div class="page-section-body">
            본 페이지의 설명은 서비스 내 데이터 탐색을 돕기 위한 기준 안내입니다.<br><br>
            실제 데이터 연동 단계에서는 데이터 원본의 구성 방식과 기준에 따라
            일부 분류 항목명 또는 해석 방식이 달라질 수 있습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------
# 페이지: 팀 소개
# -----------------------
def page_team():
    render_page_header("""
    <div class="page-hero">
        <div class="page-hero-title">👥 팀 소개</div>
        <div class="page-hero-desc">
            본 프로젝트는 3명의 팀원이 역할을 분담하여 기획, 데이터 구성,
            페이지 설계, 서비스 구현을 함께 수행하였습니다.
        </div>
    </div>
    """)

    st.markdown("""
    <div class="page-section">
        <div class="page-section-title">📌 팀 개요</div>
        <div class="page-section-body">
            우리 팀은 자동차 등록 현황 데이터를 보다 직관적으로 탐색할 수 있는 서비스를 목표로,
            데이터 이해, 화면 구성, 기능 구현을 중심으로 프로젝트를 진행하였습니다.<br><br>
            각 팀원은 기획, 데이터 처리, UI 구성, 페이지 설계 등 서로 다른 역할을 맡아
            프로젝트의 완성도를 높이는 방향으로 협업하였습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    for col, name, chip, body in zip(
        [col1, col2, col3],
        ["팀원 1", "팀원 2", "팀원 3"],
        ["기획 · DB설계", "페이지 개발 · 분석 지원", "UI 구현 · 디자인 구성"],
        [
            "프로젝트의 전체 방향성을 설정하고, 서비스 목적과 페이지 구조를 설계하였습니다.<br><br>"
            "사용자가 데이터를 직관적으로 탐색할 수 있도록 서비스 흐름과 주요 기능 구성을 담당하였습니다.",
            "자동차 등록 현황 데이터의 구조를 정리하고, 조회 및 시각화에 필요한 데이터 기준을 구성하였습니다.<br><br>"
            "또한 탭별 현황 페이지에 활용할 수 있는 분석 방향과 데이터 활용 방식을 함께 설계하였습니다.",
            "Streamlit 기반 화면 구현과 페이지 연결, 탭 구성, 사이드바 필터 등 서비스의 인터페이스를 개발하였습니다.<br><br>"
            "사용성과 가독성을 높이기 위해 카드형 레이아웃과 페이지 전반의 디자인 요소를 반영하였습니다.",
        ],
    ):
        col.markdown(
            f'<div class="page-card"><div class="page-card-title">{name}</div>'
            f'<div class="page-chip">{chip}</div>'
            f'<div class="page-card-body">{body}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("###")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="page-section">
            <div class="page-section-title">🤝 협업 방식</div>
            <div class="page-section-body">
                팀원들은 기획, 데이터, 구현 역할을 분담하되,
                전체 서비스 흐름과 핵심 기능은 함께 논의하며 결정하였습니다.<br><br>
                이를 통해 기능 구현과 페이지 구성이 단절되지 않고,
                하나의 일관된 서비스 경험으로 이어질 수 있도록 구성했습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="page-section">
            <div class="page-section-title">✨ 팀의 강점</div>
            <div class="page-section-body">
                우리 팀은 사용자가 실제로 활용하기 쉬운 구조를 만드는 데 중점을 두었습니다.<br><br>
                유가와 자동차 등록 현황 데이터를 탐색하고,
                대시보드 시각화를 통해 이들의 관계성을 파악할 수 있다는 점이
                팀 프로젝트의 핵심 강점입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------
# 페이지: 대시보드
# -----------------------
DASHBOARD_TABS  = ["개요", "유가 추이", "연료별 현황", "차종·용도 현황", "지역별 현황"]  # ← 추가
FUEL_OPTIONS    = ["휘발유", "경유", "전기", "하이브리드(휘발유+전기)", "하이브리드(경유+전기)"]
TYPE_OPTIONS    = ["승용", "승합", "화물", "특수"]
USAGE_OPTIONS   = ["비사업용", "사업용"]
REGION_OPTIONS  = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
                   "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]

FUEL_PRICE_OPTIONS = ["휘발유", "경유", "LPG"]  # 유가 추이용 연료 옵션

def page_dashboard():
    render_page_header("""
    <div class="page-hero">
        <div class="page-hero-title">📊 대시보드</div>
        <div class="page-hero-desc">
            전국 시도별 자동차 등록 현황과 유가 변동 흐름을 다양한 관점에서 확인하고,
            주요 분포와 변화 추이를 직관적으로 볼 수 있는 대시보드 페이지입니다.
        </div>
    </div>
    """)

    selected_tab = st.segmented_control(None, DASHBOARD_TABS, default="개요")

    selected_fuels = selected_types = selected_usages = selected_regions = []
    selected_fuel_prices = []

    with st.sidebar:
        st.markdown("""
        <div style="color:#4b5563; font-size:15px; font-weight:800;
                    letter-spacing:1px; margin-bottom:14px;">
            Team<br>Project_1
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.markdown("##")
        st.header("📌 대시보드 필터")

        if selected_tab == "유가 추이":
            selected_fuel_prices = st.multiselect("연료 선택", FUEL_PRICE_OPTIONS, placeholder="연료를 선택하세요")
            st.divider()
            year_range = st.slider("기간 선택", min_value=2015, max_value=2024, value=(2020, 2024))
        elif selected_tab == "연료별 현황":
            selected_fuels   = st.multiselect("연료 선택", FUEL_OPTIONS,  placeholder="연료를 선택하세요")
        elif selected_tab == "차종·용도 현황":
            selected_types   = st.multiselect("차종 선택", TYPE_OPTIONS,   placeholder="차종을 선택하세요")
            selected_usages  = st.multiselect("용도 선택", USAGE_OPTIONS,  placeholder="용도를 선택하세요")
        elif selected_tab == "지역별 현황":
            selected_regions = st.multiselect("지역 선택", REGION_OPTIONS, placeholder="지역을 선택하세요")
        else:
            st.caption("개요 탭은 별도 필터 없이 전체 현황을 보여줍니다.")

    # ── 개요 ──
    if selected_tab == "개요":
        st.write("")
        st.subheader("⭐ 전체 현황 개요")

        a1, a2, a3, a4, a5, a6 = st.columns(6)
        for col, label, val in zip(
            [a1, a2, a3, a4, a5, a6],
            ["전체 등록 대수", "연료", "차종", "유가", "지역", "OO"],
            ["예시값", "5", "3", "1", "17", "13"],
        ):
            with col:
                with st.container(border=True):
                    st.markdown(label)
                    st.write(val)

        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("**전체 등록 현황 요약 차트 영역**")
                st.write("예: 도넛차트 / 전체 분포 차트")
        with c2:
            with st.container(border=True):
                st.markdown("**주요 비중 비교 차트 영역**")
                st.write("예: 연료별 비중 / 차종별 비중")

    # ── 유가 추이 (신규) ──
    elif selected_tab == "유가 추이":
        st.subheader("💰 유가 추이")
        if not selected_fuel_prices:
            st.info("왼쪽 사이드바에서 연료를 선택하면 유가 추이 차트가 표시됩니다.")
        else:
            custom_success(f"선택 연료: {', '.join(selected_fuel_prices)} / 기간: {year_range[0]} ~ {year_range[1]}")

            col1, col2, col3 = st.columns(3)
            col1.metric("선택 연료 수",  len(selected_fuel_prices))
            col2.metric("조회 시작 연도", year_range[0])
            col3.metric("조회 종료 연도", year_range[1])

            st.markdown("###")
            c1, c2 = st.columns(2)
            with c1:
                with st.container(border=True):
                    st.markdown("**연도별 유가 변동 추이 차트 영역**")
                    st.write("예: 연도별 휘발유·경유·LPG 가격 라인차트")
            with c2:
                with st.container(border=True):
                    st.markdown("**연료별 평균 가격 비교 차트 영역**")
                    st.write("예: 연료 유형별 평균가 바차트")

            st.markdown("###")
            with st.container(border=True):
                st.markdown("**유가 변동 상세 데이터 테이블 영역**")
                st.write("예: 연도·연료별 가격 테이블")

    # ── 연료별 현황 ──
    elif selected_tab == "연료별 현황":
        st.subheader("⛽ 연료별 현황")
        if not selected_fuels:
            st.info("왼쪽 사이드바에서 연료를 선택하면 관련 차트와 통계가 표시됩니다.")
        else:
            custom_success(f"선택 연료: {', '.join(selected_fuels)}")
            col1, col2, col3 = st.columns(3)
            col1.metric("선택 연료 수",  len(selected_fuels))
            col2.metric("총 등록 대수",  "예시값")
            col3.metric("최다 비중 연료", "예시값")
            st.markdown("###")
            c1, c2 = st.columns(2)
            with c1:
                with st.container(border=True): st.write("연료별 등록 대수 차트 영역")
            with c2:
                with st.container(border=True): st.write("연료별 비율 차트 영역")

    # ── 차종·용도 현황 ──
    elif selected_tab == "차종·용도 현황":
        st.subheader("🚘 차종·용도 현황")
        if not selected_types and not selected_usages:
            st.info("왼쪽 사이드바에서 차종 또는 용도를 선택하면 관련 차트와 통계가 표시됩니다.")
        else:
            custom_success(
                f"선택 조건: 차종({', '.join(selected_types) or '전체'}) / "
                f"용도({', '.join(selected_usages) or '전체'})"
            )
            col1, col2, col3 = st.columns(3)
            col1.metric("선택 차종 수", len(selected_types) or 4)
            col2.metric("선택 용도 수", len(selected_usages) or 2)
            col3.metric("총 등록 대수", "예시값")
            st.markdown("###")
            c1, c2 = st.columns(2)
            with c1:
                with st.container(border=True): st.write("차종별 등록 현황 차트 영역")
            with c2:
                with st.container(border=True): st.write("용도별 등록 현황 차트 영역")

    # ── 지역별 현황 ──
    elif selected_tab == "지역별 현황":
        st.subheader("🗺️ 지역별 현황")
        if not selected_regions:
            st.info("왼쪽 사이드바에서 지역을 선택하면 관련 차트와 통계가 표시됩니다.")
        else:
            custom_success(f"선택 지역: {', '.join(selected_regions)}")
            col1, col2, col3 = st.columns(3)
            col1.metric("선택 지역 수",  len(selected_regions))
            col2.metric("총 등록 대수",  "예시값")
            col3.metric("최다 등록 지역", "예시값")
            st.markdown("###")
            c1, c2 = st.columns(2)
            with c1:
                with st.container(border=True): st.write("지역별 등록 대수 차트 영역")
            with c2:
                with st.container(border=True): st.write("지역별 비율 차트 영역")
# -----------------------
# 페이지: 분석
# -----------------------
def page_analysis():
    render_page_header("""
    <div class="page-hero">
        <div class="page-hero-title">📈 분석</div>
        <div class="page-hero-desc">
            유가 변동과 자동차 등록현황을 선택한 조건에 따라 간단한 분석을 할 수 있습니다.
        </div>
    </div>
    """)

    with st.sidebar:
        st.header("🔎 분석 조건")
        selected_fuel   = st.multiselect("연료 선택", FUEL_OPTIONS)
        selected_type   = st.multiselect("차종 선택", TYPE_OPTIONS)
        selected_usage  = st.multiselect("용도 선택", USAGE_OPTIONS)
        selected_region = st.multiselect("지역 선택", REGION_OPTIONS)

    if not any([selected_fuel, selected_type, selected_usage, selected_region]):
        st.info("왼쪽 사이드바에서 조건을 선택하면 관련 데이터가 표시됩니다.")
        return

    def fmt(lst): return ", ".join(lst) if lst else "전체"

    custom_success(
        f"연료({fmt(selected_fuel)}) / 차종({fmt(selected_type)}) / "
        f"용도({fmt(selected_usage)}) / 지역({fmt(selected_region)})"
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("총 등록 대수",  "예시값")
    col2.metric("선택 연료 수",  len(selected_fuel))
    col3.metric("선택 차종 수",  len(selected_type))
    col4.metric("선택 지역 수",  len(selected_region))

    st.markdown("###")
    for (title1, title2), (c1, c2) in zip(
        [("연료별 분포", "차종별 분포"), ("지역별 분포", "용도별 분포")],
        [st.columns(2), st.columns(2)],
    ):
        with c1:
            st.subheader(title1)
            with st.container(border=True): st.write(f"{title1} 차트가 들어갑니다.")
        with c2:
            st.subheader(title2)
            with st.container(border=True): st.write(f"{title2} 차트가 들어갑니다.")

    st.subheader("상세 데이터")
    with st.container(border=True):
        st.write("필터링된 데이터 테이블이 들어갑니다.")

# -----------------------
# 페이지: FAQ
# -----------------------
FAQ_DATA = [
    {"company": "현대자동차", "category": "구매",  "question": "전기차 보조금은 어떻게 확인하나요?",   "answer": "지역별 공고와 구매 절차에 따라 확인할 수 있습니다."},
    {"company": "현대자동차", "category": "서비스", "question": "정기 점검 예약은 어디서 하나요?",      "answer": "공식 서비스센터 또는 온라인 예약 시스템을 통해 가능합니다."},
    {"company": "기아",       "category": "구매",  "question": "시승 신청은 어떻게 하나요?",           "answer": "공식 홈페이지의 시승 신청 메뉴에서 원하는 차종과 일정을 선택할 수 있습니다."},
    {"company": "기아",       "category": "계정",  "question": "멤버십 가입은 어디서 하나요?",         "answer": "공식 홈페이지 또는 앱에서 회원가입 후 멤버십 서비스를 이용할 수 있습니다."},
    {"company": "테슬라",     "category": "계정",  "question": "앱 계정 연결은 어떻게 하나요?",        "answer": "차량 인도 후 계정 등록 및 앱 연동 절차를 통해 사용할 수 있습니다."},
    {"company": "테슬라",     "category": "서비스","question": "서비스 예약은 어디서 진행하나요?",      "answer": "Tesla 앱에서 서비스 항목을 선택하고 예약을 진행할 수 있습니다."},
]

def page_faq():
    render_page_header("""
    <div class="page-hero">
        <div class="page-hero-title">❓ FAQ</div>
        <div class="page-hero-desc">
            기업 FAQ 정보를 주제별로 탐색하고 확인할 수 있는 페이지입니다.
        </div>
    </div>
    """)

    st.markdown("""
    <div class="page-section">
        <div class="page-section-title">🔎 FAQ 검색 및 필터</div>
        <div class="page-section-body">기업, 카테고리, 키워드를 선택하여 원하는 FAQ를 빠르게 확인할 수 있습니다.</div>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns([1, 1, 1.2])
    with f1:
        selected_company  = st.selectbox("기업 선택",      ["전체", "현대자동차", "기아", "테슬라"],           key="faq_company")
    with f2:
        selected_category = st.selectbox("카테고리 선택",   ["전체", "구매", "서비스", "계정", "결제", "환불"], key="faq_category")
    with f3:
        keyword = st.text_input("키워드 검색", placeholder="질문 또는 답변 키워드를 입력하세요", key="faq_keyword")

    filtered = [
        f for f in FAQ_DATA
        if (selected_company  == "전체" or f["company"]  == selected_company)
        and (selected_category == "전체" or f["category"] == selected_category)
        and (not keyword or keyword.lower() in f["question"].lower() or keyword.lower() in f["answer"].lower())
    ]

    col1, col2, col3 = st.columns(3)
    col1.metric("선택 기업",      selected_company)
    col2.metric("선택 카테고리",   selected_category)
    col3.metric("검색 결과 수",    len(filtered))

    st.markdown("###")
    st.markdown("""
    <div class="page-section">
        <div class="page-section-title">📋 FAQ 목록</div>
        <div class="page-section-body">질문을 클릭하면 답변을 확인할 수 있습니다.</div>
    </div>
    """, unsafe_allow_html=True)

    if not filtered:
        st.info("조건에 맞는 FAQ가 없습니다.")
    else:
        for faq in filtered:
            with st.expander(f"[{faq['company']}] {faq['question']}", expanded=False):
                st.markdown(f"**카테고리:** {faq['category']}")
                st.write(faq["answer"])

    st.markdown("""
    <div class="page-section">
        <div class="page-section-title">📌 안내</div>
        <div class="page-section-body">
            현재는 FAQ 페이지 구조를 구성하기 위한 예시 데이터가 표시되고 있습니다.<br><br>
            실제 기업 FAQ 데이터는 추후 웹 크롤링을 통해 연동할 예정입니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------
# 라우터
# -----------------------
PAGE_MAP = {
    #"start":      page_start,
    "main":       page_main,
    "intro":      page_intro,
    "team":       page_team,
    "dashboard":  page_dashboard,
    "analysis":   page_analysis,
    "faq":        page_faq,
    "data_guide": page_data_guide,
}

render_fn = PAGE_MAP.get(st.session_state.page)
if render_fn:
    render_fn()
else:
    st.error("알 수 없는 페이지입니다.")
    if st.button("홈으로"):
        go_to("start")













