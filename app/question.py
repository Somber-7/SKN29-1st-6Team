import streamlit as st
from app.utils import render_page_header

# -------------------------
# 회사별 카테고리 메타
# cat2_list가 비어 있으면 2차 카테고리 없음
# -------------------------
CATEGORY_META = {
    "제네시스": {
        "MY GENESIS 앱": ["기타", "디지털 키", "마이 메뉴", "서비스", "설치 및 실행", "인사이트", "차량 등록 및 공유", "컨트롤"],
        "Pleos 계정": ["가입", "소개", "전환 상세 안내", "전환 예외 케이스", "제네시스 통합계정 관련 사항", "탈퇴"],
        "무선 소프트웨어 업데이트": [],
        "빌트인 캠": [],
        "인카페이먼트": [],
        "정비예약": ["A/S", "가입", "서비스이용", "요금", "해지"],
        "차량 구매": ["구입 조건", "리스", "세이브오토", "일반", "카드 결제", "포인트", "할부"],
        "홈페이지": [],
    },
    "현대": {
        "모젠서비스": ["사용법", "이용단말"],
        "블루링크": ["가입/해지/변경", "서비스 이용", "오류 및 A/S", "요금"],
        "정비예약": ["일반"],
        "차량구매": ["일반"],
        "차량정비": ["일반"],
        "특허관련": ["일반"],
        "현대 디지털 키": ["일반"],
        "홈페이지": ["기타", "로그인", "회원"],
    },
    "기아": {
        "차량 구매": [],
        "차량 정비": [],
        "기아멤버스": [],
        "홈페이지": [],
        "PBV": [],
        "기타": [],
    },
    "KGM": {
        "차량정비": [],
        "구매/영업": [],
        "홈페이지": [],
        "부품": [],
        "기타": [],
        "IR 자료실": [],
    },
}

FAQ_TABS = ["기아", "제네시스", "현대", "KGM"]

_TAB_ICON = {
    "기아": "🚗",
    "제네시스": "🚗",
    "현대": "🚗",
    "KGM": "🚗",
}


def _render_faq_body(company: str, tab_key: str):
    company_categories = CATEGORY_META.get(company, {})
    cat1_options = ["전체"] + list(company_categories.keys())

    f1, f2, _, _, _ = st.columns(5)

    with f1:
        selected_cat1 = st.selectbox(
            "1차 카테고리",
            cat1_options,
            key=f"faq_cat1_{tab_key}",
        )

    selected_cat2 = "전체"
    cat2_options = []

    if selected_cat1 != "전체":
        cat2_options = company_categories.get(selected_cat1, [])

    with f2:
        if cat2_options:
            selected_cat2 = st.selectbox(
                "2차 카테고리",
                ["전체"] + cat2_options,
                key=f"faq_cat2_{tab_key}",
            )

    cat2_html = ""
    if cat2_options and selected_cat2 != "전체":
        cat2_html = f"<p><b>2차 카테고리:</b> {selected_cat2}</p>"

    st.markdown(f"""
        <div class="page-section">
            <div class="page-section-title">📌 현재 선택</div>
            <div class="page-section-body">
                <p><b>회사:</b> {company}</p>
                <p><b>1차 카테고리:</b> {selected_cat1}</p>
                {cat2_html}</div>
        </div>
    """, unsafe_allow_html=True)
    
    

    

    st.markdown("###")

    # -------------------------
    # 크롤링 데이터 들어갈 자리
    # -------------------------
    st.markdown("""
    <div class="page-section">
        <div class="page-section-title">📋 FAQ 결과 영역</div>
        <div class="page-section-body">
            선택한 회사 및 카테고리를 기준으로, 추후 크롤링한 질문/답변 데이터가 이 영역에 표시될 예정입니다.
        </div>
    </div>
    """, unsafe_allow_html=True)


def page_faq():
    render_page_header("""
    <div class="page-section">
        <div class="page-section-title">❓ FAQ</div>
        <div class="page-section-body">
            회사와 카테고리를 선택하여 FAQ를 탐색할 수 있는 페이지입니다.
        </div>
    </div>
    """)

    selected_tab = st.segmented_control(None, FAQ_TABS, default="제네시스")
    st.write("")
    st.subheader(f"{_TAB_ICON.get(selected_tab, '')} {selected_tab}")

    _render_faq_body(
        company=selected_tab,
        tab_key=selected_tab,
    )



