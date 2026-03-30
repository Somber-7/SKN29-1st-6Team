import streamlit as st
from app.utils import render_page_header

FAQ_DATA = [
    {"company": "현대자동차", "category": "구매",  "question": "전기차 보조금은 어떻게 확인하나요?",  "answer": "지역별 공고와 구매 절차에 따라 확인할 수 있습니다."},
    {"company": "현대자동차", "category": "서비스", "question": "정기 점검 예약은 어디서 하나요?",     "answer": "공식 서비스센터 또는 온라인 예약 시스템을 통해 가능합니다."},
    {"company": "기아",       "category": "구매",  "question": "시승 신청은 어떻게 하나요?",          "answer": "공식 홈페이지의 시승 신청 메뉴에서 원하는 차종과 일정을 선택할 수 있습니다."},
    {"company": "기아",       "category": "계정",  "question": "멤버십 가입은 어디서 하나요?",        "answer": "공식 홈페이지 또는 앱에서 회원가입 후 멤버십 서비스를 이용할 수 있습니다."},
    {"company": "테슬라",     "category": "계정",  "question": "앱 계정 연결은 어떻게 하나요?",       "answer": "차량 인도 후 계정 등록 및 앱 연동 절차를 통해 사용할 수 있습니다."},
    {"company": "테슬라",     "category": "서비스","question": "서비스 예약은 어디서 진행하나요?",     "answer": "Tesla 앱에서 서비스 항목을 선택하고 예약을 진행할 수 있습니다."},
]

FAQ_TABS = ["기아", "제네시스", "현대", "KGM"]

# 탭 → company 필터 매핑 (None = 전체)
_TAB_COMPANY = {
    "기아":    "기아",
    "제네시스":    "제네시스",
    "현대": "현대",
    "KGM": "KGM" ,
}

_TAB_ICON = {
    "기아": "⭐", "제네시스": "💰", "현대": "⛽", "KGM": "🚘"
}

def _render_faq_body(company_filter: str | None, tab_key: str):
    """4개 탭 공통 본문 — company_filter=None 이면 전체 표시"""
    f1, f2 = st.columns([1, 1.2])
    with f1:
        selected_category = st.selectbox(
            "카테고리 선택",
            ["전체", "구매", "서비스", "계정", "결제", "환불"],
            key=f"faq_cat_{tab_key}",      # ← 탭마다 key 분리 (중복 key 에러 방지)
        )
    with f2:
        keyword = st.text_input(
            "키워드 검색",
            placeholder="질문 또는 답변 키워드를 입력하세요",
            key=f"faq_kw_{tab_key}",
        )

    filtered = [
        f for f in FAQ_DATA
        if (company_filter is None or f["company"] == company_filter)
        and (selected_category == "전체" or f["category"] == selected_category)
        and (not keyword
             or keyword.lower() in f["question"].lower()
             or keyword.lower() in f["answer"].lower())
    ]

    _, col2 = st.columns([9,1])
    #col1.metric("선택 카테고리", selected_category)
    col2.metric("검색 건수",  len(filtered))

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
            현재는 예시 데이터가 표시되고 있습니다.<br><br>
            실제 기업 FAQ 데이터는 추후 웹 크롤링을 통해 연동할 예정입니다.
        </div>
    </div>
    """, unsafe_allow_html=True)


def page_faq():
    render_page_header("""
    <div class="page-section">
        <div class="page-section-title">❓ FAQ</div>
        <div class="page-section-body">
            기업, 카테고리, 키워드를 선택하여 원하는 FAQ를 빠르게 확인할 수 있습니다.
        </div>
    </div>
    """)

    selected_tab = st.segmented_control(None, FAQ_TABS, default="기아")
    st.write("")
    st.subheader(f"{_TAB_ICON.get(selected_tab, '')} {selected_tab}")

    _render_faq_body(
        company_filter=_TAB_COMPANY.get(selected_tab),
        tab_key=selected_tab,
    )