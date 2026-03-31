import streamlit as st
import base64

# -----------------------
# 공통 상수
# -----------------------
FUEL_OPTIONS       = ["휘발유", "경유", "전기", "하이브리드(휘발유+전기)", "하이브리드(경유+전기)"]
FUEL_PRICE_OPTIONS = ["휘발유", "경유", "LPG"]
TYPE_OPTIONS       = ["승용", "승합", "화물", "특수"]
USAGE_OPTIONS      = ["비사업용", "사업용"]
REGION_OPTIONS     = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
                      "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]

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

def get_image_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def render_high():
    _, col1 = st.columns([9, 1])
    with col1:
        if st.button("🏠", key="to_main", use_container_width=True, type="tertiary"):
            go_to("main")

def render_header():
    image_base64 = get_image_base64("image/img_ex4.jpg")
    st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <img src="data:image/jpg;base64,{image_base64}"
                style="width:100%; height:auto; object-fit:cover;
                       border-radius:16px; display:block;">
        </div>
    """, unsafe_allow_html=True)
    st.markdown("")

def render_top_nav():
    with st.container(border=False):
        _, _, _, col1, col2, col3, _, _, _ = st.columns(9)
        with col1:
            with st.popover("📌 소개", use_container_width=True):
                if st.button("🗂️ 데이터 설명", key="nav_home_2", use_container_width=True): go_to("data_guide")
                if st.button("👥 팀 소개",     key="nav_home_3", use_container_width=True): go_to("team")
        with col2:
            with st.popover("ℹ️ 현황", use_container_width=True):
                if st.button("📊 대시보드", key="nav_dash_1", use_container_width=True): go_to("dashboard")
                if st.button("📈 분석",     key="nav_dash_2", use_container_width=True): go_to("analysis")
        with col3:
            with st.popover("🔔 문의", use_container_width=True):
                if st.button("❓ FAQ", key="nav_contact_1", use_container_width=True): go_to("faq")

def render_page_header(hero_html: str):
    """🏠버튼 → 이미지헤더 → 네비 → 구분선 → hero"""
    render_high()
    render_header()
    render_top_nav()
    st.markdown('<div class="double-divider"></div>', unsafe_allow_html=True)
    st.markdown(hero_html, unsafe_allow_html=True)

def inject_global_css():
    st.markdown("""
    <style>
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #E3E7EB;
        color: #1f2937;
    }
    .custom-header {
        background: linear-gradient(180deg, #161A1F 0%, #24282D 55%, #4B5158 100%);
        padding: 24px 30px;
        border-radius: 16px;
        margin-bottom: 12px;
        color: white;
        overflow: hidden;
    }
    .custom-header-title { margin:0; font-size:28px; font-weight:700; color:white; line-height:1.25; }
    .custom-header-desc  { margin-top:8px; font-size:14px; opacity:0.92; color:white; line-height:1.6; }

    .st-key-nav_home_2 button, .st-key-nav_home_3 button,
    .st-key-nav_dash_1 button, .st-key-nav_dash_2 button,
    .st-key-nav_contact_1 button {
        color: #1f3a5f !important;
        font-weight: 600;
    }
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
    .page-hero {
        background: linear-gradient(180deg, #161A1F 0%, #24282D 55%, #4B5158 100%);
        color: white;
        padding: 32px 36px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 8px 20px rgba(31,59,91,0.10);
    }
    .page-hero-title { font-size:2rem; font-weight:800; margin-bottom:8px; }
    .page-hero-desc  { font-size:1rem; opacity:0.95; line-height:1.7; }

    .page-card {
        background: white;
        border: 1px solid #e6edf5;
        border-radius: 18px;
        padding: 22px 24px 18px 24px;
        box-shadow: 5px 5px 4px rgba(31,59,91,0.06);
        margin-bottom: 16px;
        height: 100%;
    }
    .page-card-title { font-size:1.15rem; font-weight:800; color:#1f3b5b; margin-bottom:10px; }
    .page-card-body  { color:#4f5d6b; font-size:0.97rem; line-height:1.8; }

    .page-section {
        background: #f8fbfe;
        border: 1px solid #e6edf5;
        border-radius: 18px;
        padding: 22px 24px 18px 24px;
        box-shadow: 5px 5px 4px rgba(31,59,91,0.04);
        margin-bottom: 18px;
    }
    .page-section-title { font-size:1.1rem; font-weight:800; color:#1f3b5b; margin-bottom:10px; }
    .page-section-body  { color:#556474; font-size:0.96rem; line-height:1.8; }

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
    .double-divider {
        border-top: 1px solid #24282D;
        border-bottom: 1px solid #24282D;
        height: 4px;
        margin: 12px 0 18px 0;
    }
    </style>
    """, unsafe_allow_html=True)