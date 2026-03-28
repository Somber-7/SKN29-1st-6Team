
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

load_dotenv()





st.set_page_config(page_title="Team 6", layout="wide")

# ------------
# header bar
# ------------

def render_header():
    st.markdown("""
        <style>
        .custom-header {
            background: linear-gradient(90deg, #1f3a5f, #2b5876);
            padding: 24px 30px;
            border-radius: 16px;
            margin-bottom: 12px;
            color: white;
        }
        .custom-header h1 {
            margin: 0;
            font-size: 30px;
        }
        .custom-header p {
            margin: 8px 0 0 0;
            font-size: 15px;
            opacity: 0.92;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="custom-header">
            <h1>전국 자동차 등록 현황 대시보드</h1>
            <p>자동차 등록 데이터를 직관적으로 탐색하고 비교하는 서비스</p>
        </div>
    """, unsafe_allow_html=True)

# ------------
# page logo
# ------------

def render_page_logo():
    col1, _ = st.columns([1,9])

    with col1:
            if st.button("🏠 Main", key="logo_to_main",
                         type="tertiary", use_container_width=False,
                         ):
                go_to("main")

    st.markdown("""
    <style>
    .page-logo {
        display: inline-block;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 1.2px;
        color: white;
        background-color: #1f3a5f;
        padding: 6px 12px;
        border-radius: 999px;
        margin-top: -30px;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-logo">삼총사</div>', unsafe_allow_html=True)


# -----------
# success
# -----------

def custom_success(message):
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="custom-success">✅ {message}</div>',
        unsafe_allow_html=True
    )

# -----------
# 세부 페이지 css
# -----------

def inject_page_css():
    st.markdown("""
    <style>
    .page-hero {
        background: linear-gradient(135deg, #1f3b5b, #2b5876);
        color: white;
        padding: 32px 36px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 8px 20px rgba(31, 59, 91, 0.10);
    }

    .page-hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .page-hero-desc {
        font-size: 1rem;
        opacity: 0.95;
        line-height: 1.7;
    }

    .page-card {
        background: white;
        border: 1px solid #e6edf5;
        border-radius: 18px;
        padding: 22px 24px 18px 24px;
        box-shadow: 0 4px 12px rgba(31, 59, 91, 0.06);
        margin-bottom: 16px;
        height: 100%;
    }

    .page-card-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #1f3b5b;
        margin-bottom: 10px;
    }

    .page-card-body {
        color: #4f5d6b;
        font-size: 0.97rem;
        line-height: 1.8;
    }

    .page-section {
        background: #f8fbfe;
        border: 1px solid #e6edf5;
        border-radius: 18px;
        padding: 22px 24px 18px 24px;
        box-shadow: 0 3px 10px rgba(31, 59, 91, 0.04);
        margin-bottom: 18px;
    }

    .page-section-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #1f3b5b;
        margin-bottom: 10px;
    }

    .page-section-body {
        color: #556474;
        font-size: 0.96rem;
        line-height: 1.8;
    }

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





def page_team():
    render_page_logo()
    render_header()
    render_top_nav()
    inject_page_css()

    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">👥 팀 소개</div>
        <div class="page-hero-desc">
            본 프로젝트는 3명의 팀원이 역할을 분담하여 기획, 데이터 구성,
            페이지 설계, 서비스 구현을 함께 수행하였습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    with col1:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">팀원 1</div>
            <div class="page-chip">기획 · 서비스 설계</div>
            <div class="page-card-body">
                프로젝트의 전체 방향성을 설정하고, 서비스 목적과 페이지 구조를 설계하였습니다.<br><br>
                사용자가 데이터를 직관적으로 탐색할 수 있도록 서비스 흐름과 주요 기능 구성을 담당하였습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">팀원 2</div>
            <div class="page-chip">데이터 구성 · 분석 지원</div>
            <div class="page-card-body">
                자동차 등록 현황 데이터의 구조를 정리하고, 조회 및 시각화에 필요한 데이터 기준을 구성하였습니다.<br><br>
                또한 탭별 현황 페이지에 활용할 수 있는 분석 방향과 데이터 활용 방식을 함께 설계하였습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">팀원 3</div>
            <div class="page-chip">UI 구현 · 페이지 개발</div>
            <div class="page-card-body">
                Streamlit 기반 화면 구현과 페이지 연결, 탭 구성, 사이드바 필터 등 서비스의 인터페이스를 개발하였습니다.<br><br>
                사용성과 가독성을 높이기 위해 카드형 레이아웃과 페이지 전반의 디자인 요소를 반영하였습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

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
                하나의 일관된 서비스 경험으로 이어질 수 있도록 하였습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="page-section">
            <div class="page-section-title">✨ 팀의 강점</div>
            <div class="page-section-body">
                우리 팀은 데이터 이해와 서비스 구현을 분리하지 않고,
                사용자가 실제로 활용하기 쉬운 구조를 만드는 데 중점을 두었습니다.<br><br>
                단순한 결과 제시를 넘어, 데이터를 탐색 가능한 형태로 제공하는 점이
                팀 프로젝트의 핵심 강점입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)


# -------------
# 메인 화면 카드
# -------------
def inject_card_css():
    st.markdown("""
    <style>
    .st-key-main_card_1, .st-key-main_card_2, .st-key-main_card_3 {
        background: white;
        border: 1px solid #e8edf3;
        border-radius: 16px;
        padding: 18px 18px 12px 18px;
        box-shadow: 9px 9px 5px rgba(31, 59, 91, 0.55);
        margin-bottom: 10px;
    }

    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1f3b5b;
        margin-bottom: 6px;
    }

    .card-desc {
        color: #5f6b7a;
        font-size: 0.94rem;
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

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
    st.markdown("###")
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            with st.popover("⭐ 홈", use_container_width=True):
                
                st.markdown("**홈 메뉴**")
                
                if st.button("📋 서비스 소개", key="nav_home_1",use_container_width=True): go_to("intro")
                if st.button("👥 팀 소개",    key="nav_home_2",use_container_width=True): go_to("team")
                if st.button("⭐ 버전 정보",  key="nav_home_3",use_container_width=True): go_to("main")
                

        with col2:
            with st.popover("ℹ️ 현황 조회", use_container_width=True):
                st.markdown("**서비스 정보**")
                if st.button("📊 대시보드", key="nav_about_1",use_container_width=True): 
                    go_to("dashboard")
                if st.button("👥 조회",     key="nav_about_2",use_container_width=True): st.info("팀 소개 페이지")
                if st.button("🔖 분석",   key="nav_about_3",use_container_width=True): go_to("analysis")

        with col3:
            with st.popover("✉️ FAQ", use_container_width=True):
                st.markdown("**문의하기**")
                if st.button("📧 이메일 문의", key="nav_contact_1"): st.info("contact@example.com")
                if st.button("📞 고객센터",    key="nav_contact_2"): st.info("02-1234-5678")
                if st.button("❓ FAQ",          key="nav_contact_3"): st.info("FAQ 페이지")


        with col4:
            if st.button("🏠 시작화면", use_container_width=True, key="go_start"):
                go_to("start")


# -----------------------
# 각 페이지 렌더링
# -----------------------

# -----------------------
# 시작화면
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


# -----------------------
# 메인화면
# -----------------------

def page_main():
    render_page_logo()
    render_header()
    render_top_nav()
    inject_card_css()

    st.title("🏠 메인페이지")
    st.write("상단 메뉴를 통해 원하는 기능으로 이동할 수 있습니다.")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(key="main_card_1"):
            st.markdown('<div class="card-title">📈 대시보드</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">전체 현황과 주요 분포를 ' \
            '시각적으로 확인합니다.</div>', unsafe_allow_html=True)
            

    with col2:
        with st.container(key="main_card_2"):
            st.markdown('<div class="card-title">🔎 분석페이지</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">조건을 선택해 원하는 데이터를 ' \
            '조회합니다.</div>', unsafe_allow_html=True)
            

    with col3:
        with st.container(key="main_card_3"):
            st.markdown('<div class="card-title">❓ FAQ</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">서비스 설명과 자주 묻는 질문을 ' \
            '확인합니다.</div>', unsafe_allow_html=True)
            

# def page_main():
#     render_page_logo()
#     render_header()
#     render_top_nav()
    
#     st.title("🏠 메인페이지")
#     st.write("전국 자동차 등록 현황 대시보드의 메인 페이지입니다.")

#     st.divider()
    
#     col1,col2,col3 = st.columns(3)

    

#     with col1:
#             with st.container(border=True):
#                 st.markdown("서비스 소개")
#                 st.write("이 서비스는...")
#     with col2:
#             with st.container(border=True):
#                 st.markdown("서비스 소개")
#                 st.write("이 서비스는...")
#     with col3:
#             with st.container(border=True):
#                 st.markdown("서비스 소개")
#                 st.write("이 서비스는...")

    

#     with col1:
#             with st.expander("서비스 소개"):
#                 st.write("이 서비스는...")
#     with col2:
#             with st.expander("서비스 소개"):
#                 st.write("이 서비스는...")
#     with col3:
#             with st.expander("서비스 소개"):
#                 st.write("이 서비스는...")


# -------------------------
# intro Section
# -------------------------

def page_intro():
    render_page_logo()
    render_header()
    render_top_nav()
    inject_page_css()

    # -------------------------
    # Hero Section
    # -------------------------
    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">📘 서비스 소개</div>
        <div class="page-hero-desc">
            전국 자동차 등록 현황 데이터를 연료, 차종, 용도, 지역 기준으로
            직관적으로 탐색하고 비교할 수 있도록 설계한 데이터 기반 서비스입니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # 목표 / 문제 정의
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">🎯 프로젝트 목표</div>
            <div class="page-card-body">
                자동차 등록 데이터는 다양한 기준으로 구성되어 있어 단순한 표 형태만으로는
                전체 구조를 파악하기 어렵습니다.<br><br>
                본 프로젝트는 이러한 데이터를 시각화 중심의 대시보드와 조건 기반 조회 기능으로
                재구성하여, 사용자가 필요한 정보를 더 쉽고 빠르게 이해할 수 있도록 하는 것을
                목표로 합니다.
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
                사용자는 특정 연료, 차종, 용도, 지역 기준으로 데이터를 비교하고 싶어도
                이를 빠르게 확인하기 어려우며, 단순 수치 나열만으로는 데이터 구조를
                이해하는 데 한계가 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------
    # 서비스 방향성
    # -------------------------
    st.markdown("""
    <div class="page-card">
        <div class="page-card-title">🧭 서비스 방향성</div>
        <div class="page-card-body">
            본 서비스는 단순한 데이터 나열이 아니라 <b>탐색 가능한 정보 서비스</b>를 지향합니다.
            사용자가 원하는 조건을 선택하고, 그 결과를 직관적인 시각화와 함께 확인할 수 있도록
            설계하였습니다.<br><br>
            또한 전체 현황을 빠르게 이해할 수 있는 대시보드와,
            세부 조건별로 데이터를 탐색할 수 있는 조회·분석 기능을 분리하여
            정보 접근성과 활용성을 높이는 데 초점을 두었습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # 핵심 키워드
    # -------------------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">직관성</div>
            <div class="page-card-body">
                복잡한 데이터를 한눈에 이해할 수 있도록 시각화 중심으로 구성
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">탐색성</div>
            <div class="page-card-body">
                사용자가 원하는 기준을 선택해 필요한 정보를 직접 조회 가능
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">비교 가능성</div>
            <div class="page-card-body">
                연료, 차종, 용도, 지역 기준으로 데이터를 비교하며 구조를 파악
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">확장성</div>
            <div class="page-card-body">
                향후 기능 추가와 세부 분석 확장을 고려한 페이지 구조 설계
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("###")

    # -------------------------
    # 주요 기능 / 기대 효과
    # -------------------------
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="page-section">
            <div class="page-section-title">🛠️ 주요 기능</div>
            <div class="page-section-body">
                • 대시보드 기반 전체 현황 확인<br>
                • 연료, 차종, 용도, 지역별 시각화 제공<br>
                • 조건 선택을 통한 조회 및 분석 기능<br>
                • FAQ 및 서비스 안내 제공
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



# ------------
# dashboard
# ------------

def page_dashboard():
    render_page_logo()
    render_header()
    render_top_nav()

    # -------------------------
    # 대시보드 탭 선택
    # -------------------------
    
    selected_tab = st.segmented_control(None,
        ["개요","연료별 현황","차종 용도 현황", "지역별 현황"],
        default="개요"
    )

    
    # -------------------------
    # 현재 탭 표시
    # -------------------------
    st.markdown(
        f"""
        <div style="
            background-color:#f4f6f8;
            padding:12px 16px;
            border-radius:12px;
            margin-top:8px;
            margin-bottom:18px;
            font-weight:600;
            color:#1f3b5b;
        ">
            현재 대시보드: {selected_tab}
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------
    # 탭별 사이드바
    # -------------------------
    with st.sidebar:
        st.header("📌 대시보드 필터")

        selected_fuels = []
        selected_types = []
        selected_usages = []
        selected_regions = []

        if selected_tab == "연료별 현황":
            selected_fuels = st.multiselect(
                "연료 선택",
                ["휘발유", "경유", "전기", "하이브리드(휘발유+전기)", "하이브리드(경유+전기)"],
                default=[],
                placeholder="연료를 선택하세요"
            )

        elif selected_tab == "차종·용도 현황":
            selected_types = st.multiselect(
                "차종 선택",
                ["승용", "승합", "화물", "특수"],
                default=[],
                placeholder="차종을 선택하세요"
            )

            selected_usages = st.multiselect(
                "용도 선택",
                ["비사업용", "사업용"],
                default=[],
                placeholder="용도를 선택하세요"
            )

        elif selected_tab == "지역별 현황":
            selected_regions = st.multiselect(
                "지역 선택",
                ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
                 "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"],
                default=[],
                placeholder="지역을 선택하세요"
            )

        else:
            st.caption("개요 탭은 별도 필터 없이 전체 현황을 보여줍니다.")

    # -------------------------
    # 본문 렌더링
    # -------------------------
    st.title("📈 대시보드")
    st.write("자동차 등록 현황을 다양한 관점에서 시각적으로 확인할 수 있습니다.")

    # -------------------------
    # 개요
    # -------------------------
    if selected_tab == "개요":
        st.subheader("⭐ 전체 현황 개요")
        st.write("자동차 등록 현황을 전체적으로 요약해서 보여주는 영역입니다.")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("전체 등록 대수", "예시값")
        with col2:
            st.metric("연료 종류 수", "5")
        with col3:
            st.metric("차종 종류 수", "4")
        with col4:
            st.metric("지역 수", "17")

        st.markdown("###")

        c1, c2 = st.columns(2)

        with c1:
            with st.container(border=True):
                st.markdown("**전체 등록 현황 요약 차트 영역**")
                st.write("예: 도넛차트 / 전체 분포 차트")

        with c2:
            with st.container(border=True):
                st.markdown("**주요 비중 비교 차트 영역**")
                st.write("예: 연료별 비중 / 차종별 비중")

    # -------------------------
    # 연료별 현황
    # -------------------------
    elif selected_tab == "연료별 현황":
        st.subheader("⛽ 연료별 현황")
        st.write("선택한 연료 기준으로 자동차 등록 현황을 확인합니다.")

        if not selected_fuels:
            st.info("왼쪽 사이드바에서 연료를 선택하면 관련 차트와 통계가 표시됩니다.")
        else:
            custom_success(f"선택 연료: {', '.join(selected_fuels)}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("선택 연료 수", len(selected_fuels))
            with col2:
                st.metric("총 등록 대수", "예시값")
            with col3:
                st.metric("최다 비중 연료", "예시값")

            st.markdown("###")

            c1, c2 = st.columns(2)

            with c1:
                with st.container(border=True):
                    st.markdown("**연료별 등록 대수 차트 영역**")
                    st.write("예: 휘발유 / 경유 비교")

            with c2:
                with st.container(border=True):
                    st.markdown("**연료별 비율 차트 영역**")
                    st.write("예: 도넛차트")

    # -------------------------
    # 차종·용도 현황
    # -------------------------
    elif selected_tab == "차종·용도 현황":
        st.subheader("🚘 차종·용도 현황")
        st.write("선택한 차종과 용도 기준으로 자동차 등록 현황을 확인합니다.")

        if not selected_types and not selected_usages:
            st.info("왼쪽 사이드바에서 차종 또는 용도를 선택하면 관련 차트와 통계가 표시됩니다.")
        else:
            selected_type_text = ", ".join(selected_types) if selected_types else "전체"
            selected_usage_text = ", ".join(selected_usages) if selected_usages else "전체"

            custom_success(
                f"선택 조건: 차종({selected_type_text}) / 용도({selected_usage_text})"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("선택 차종 수", len(selected_types) if selected_types else 4)
            with col2:
                st.metric("선택 용도 수", len(selected_usages) if selected_usages else 2)
            with col3:
                st.metric("총 등록 대수", "예시값")

            st.markdown("###")

            c1, c2 = st.columns(2)

            with c1:
                with st.container(border=True):
                    st.markdown("**차종별 등록 현황 차트 영역**")
                    st.write("예: 승용 / 승합 / 화물 / 특수 비교")

            with c2:
                with st.container(border=True):
                    st.markdown("**용도별 등록 현황 차트 영역**")
                    st.write("예: 사업용 / 비사업용 비교")

    # -------------------------
    # 지역별 현황
    # -------------------------
    elif selected_tab == "지역별 현황":
        st.subheader("🗺️ 지역별 현황")
        st.write("선택한 지역 기준으로 자동차 등록 현황을 비교합니다.")

        if not selected_regions:
            st.info("왼쪽 사이드바에서 지역을 선택하면 관련 차트와 통계가 표시됩니다.")
        else:
            custom_success(f"선택 지역: {', '.join(selected_regions)}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("선택 지역 수", len(selected_regions))
            with col2:
                st.metric("총 등록 대수", "예시값")
            with col3:
                st.metric("최다 등록 지역", "예시값")

            st.markdown("###")

            c1, c2 = st.columns(2)

            with c1:
                with st.container(border=True):
                    st.markdown("**지역별 등록 대수 차트 영역**")
                    st.write("예: 서울 / 경기 / 제주 비교")

            with c2:
                with st.container(border=True):
                    st.markdown("**지역별 비율 차트 영역**")
                    st.write("예: 비중 비교 차트")




# ===== 분석 =====
    

def page_analysis():
    render_page_logo()
    render_header()
    render_top_nav()

    with st.sidebar:
        st.header("🔎 분석 조건")

        selected_fuel = st.multiselect("연료 선택", ["휘발유", "경유", "전기", "하이브리드(휘발유+전기)", "하이브리드(경유+전기)"])
        selected_type = st.multiselect("차종 선택", ["승용", "승합", "화물", "특수"])
        
        
        selected_usage = st.multiselect("용도 선택", ["비사업용", "사업용"])
        selected_region = st.multiselect("지역 선택", ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
                                                     "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"])

    st.title("📊 분석 페이지")
    st.write("선택한 조건에 따라 자동차 등록 현황을 확인할 수 있습니다.")

    has_filter = any([selected_fuel, selected_type, selected_usage, selected_region])

    if not has_filter:
        st.info("왼쪽 사이드바에서 조건을 선택하면 관련 데이터가 표시됩니다.")
        return

    st.info("현재 선택 조건에 따른 분석 결과입니다.")

    # 여기부터 결과 출력
    st.metric("총 등록 대수", "예시값")
    st.container(border=True).write("차트 영역")
    st.container(border=True).write("테이블 영역")

    def format_filter_text(selected):
        return ", ".join(selected) if selected else "전체"

    st.success("조건이 선택되었습니다.")

    st.info(
        f"현재 조건: "
        f"연료({format_filter_text(selected_fuel)}) / "
        f"차종({format_filter_text(selected_type)}) / "
        f"용도({format_filter_text(selected_usage)}) / "
        f"지역({format_filter_text(selected_region)})"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("총 등록 대수", "예시값")

    with col2:
        st.metric("선택 연료 수", len(selected_fuel) if selected_fuel else 0)

    with col3:
        st.metric("선택 차종 수", len(selected_type) if selected_type else 0)

    with col4:
        st.metric("선택 지역 수", len(selected_region) if selected_region else 0)

    st.markdown("###")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("연료별 분포")
        with st.container(border=True):
            st.write("여기에 연료별 차트가 들어갑니다.")

    with c2:
        st.subheader("차종별 분포")
        with st.container(border=True):
            st.write("여기에 차종별 차트가 들어갑니다.")

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("지역별 분포")
        with st.container(border=True):
            st.write("여기에 지역별 차트가 들어갑니다.")

    with c4:
        st.subheader("용도별 분포")
        with st.container(border=True):
            st.write("여기에 용도별 차트가 들어갑니다.")

    st.subheader("상세 데이터")
    with st.container(border=True):
        st.write("여기에 필터링된 데이터 테이블이 들어갑니다.")







# -----------------------
# 라우터
# -----------------------
PAGE_MAP = {
    "start": page_start,
    "main": page_main,
    "analysis": page_analysis,
    "dashboard" : page_dashboard,
    "intro" : page_intro,
    "team" : page_team
    #"faq": page_faq
}

render_fn = PAGE_MAP.get(st.session_state.page)
if render_fn:
    render_fn()
else:
    st.error("알 수 없는 페이지입니다.")
    if st.button("홈으로"):
        go_to("start")







