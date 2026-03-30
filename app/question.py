import streamlit as st
from app.utils import render_page_header
<<<<<<< HEAD

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

=======
from app.db_connect import (
    get_faq_cat1_options,
    get_faq_cat2_options,
    get_faq_cat_options,
    get_faq_list_dual,
    get_faq_list_single,
)

FAQ_TABS = ["기아", "제네시스", "현대", "KGM"]

# 탭별 DB 테이블 및 카테고리 구조 설정
# dual=True  → cat1/cat2 이중 구조 (현대, 제네시스)
# dual=False → cat 단일 구조      (기아, KGM)
_TAB_CONFIG = {
    "기아":    {"table": "tbl_kia_faq",      "dual": False},
    "제네시스": {"table": "tbl_genesis_faq",  "dual": True},
    "현대":    {"table": "tbl_hyundai_faq",   "dual": True},
    "KGM":    {"table": "tbl_kgm_faq",       "dual": False},
}

>>>>>>> 97cba086eff82b2eaee5f9c34f4dc36b537f8fb6
_TAB_ICON = {
    "기아": "🚗",
    "제네시스": "🚗",
    "현대": "🚗",
    "KGM": "🚗",
}


<<<<<<< HEAD
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
=======
@st.cache_data
def _cached_cat1_options(table: str) -> list:
    return get_faq_cat1_options(table)


@st.cache_data
def _cached_cat2_options(table: str, cat1: str) -> list:
    return get_faq_cat2_options(table, cat1)


@st.cache_data
def _cached_cat_options(table: str) -> list:
    return get_faq_cat_options(table)


def _render_faq_body(table: str, dual: bool, tab_key: str):
    """탭 공통 본문 렌더링

    dual=True  : 대분류(cat1) → 소분류(cat2) 동적 선택 (현대, 제네시스)
    dual=False : 단일 카테고리(cat) 선택 (기아, KGM)
    """
    cat1_sel = cat2_sel = cat_sel = None

    if dual:
        # ── 대분류 / 소분류 2열 ──────────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            cat1_list = ["전체"] + _cached_cat1_options(table)
            cat1_sel = st.selectbox("대분류 선택", cat1_list, key=f"faq_cat1_{tab_key}")
        with c2:
            if cat1_sel and cat1_sel != "전체":
                cat2_list = _cached_cat2_options(table, cat1_sel)
                if cat2_list:
                    cat2_sel = st.selectbox(
                        "소분류 선택",
                        ["전체"] + cat2_list,
                        key=f"faq_cat2_{tab_key}",
                    )
                else:
                    # 해당 대분류에 소분류 없음
                    st.selectbox("소분류 선택", ["전체"], key=f"faq_cat2_{tab_key}", disabled=True)
                    cat2_sel = "전체"
            else:
                st.selectbox("소분류 선택", ["전체"], key=f"faq_cat2_{tab_key}", disabled=True)
                cat2_sel = "전체"
    else:
        # ── 단일 카테고리 ────────────────────────────────────
        c1, _ = st.columns([1, 1.2])
        with c1:
            cat_list = ["전체"] + _cached_cat_options(table)
            cat_sel = st.selectbox("카테고리 선택", cat_list, key=f"faq_cat_{tab_key}")

    keyword = st.text_input(
        "키워드 검색",
        placeholder="질문 또는 답변 키워드를 입력하세요",
        key=f"faq_kw_{tab_key}",
    )

    # ── 데이터 조회 ──────────────────────────────────────────
    if dual:
        faq_list = get_faq_list_dual(
            table,
            cat1=None if cat1_sel == "전체" else cat1_sel,
            cat2=None if (not cat2_sel or cat2_sel == "전체") else cat2_sel,
            keyword=keyword,
        )
    else:
        faq_list = get_faq_list_single(
            table,
            cat=None if cat_sel == "전체" else cat_sel,
            keyword=keyword,
        )

    total = len(faq_list)

    st.markdown("###")
    st.markdown(f"""
    <div class="page-section">
        <div class="page-section-title" style="display:flex;align-items:center;gap:10px;">
            📋 FAQ 목록
            <span style="font-size:0.75rem;font-weight:normal;color:#888;">
                총 {total}건
            </span>
        </div>
        <div class="page-section-body">질문을 클릭하면 답변을 확인할 수 있습니다.</div>
    </div>
    """, unsafe_allow_html=True)

    if not faq_list:
        st.info("조건에 맞는 FAQ가 없습니다.")
    else:
        PAGE_SIZE = 10
        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

        # 카테고리/키워드 변경 시 페이지를 1로 초기화
        page_key = f"faq_page_{tab_key}"
        filter_sig = f"{cat1_sel}|{cat2_sel}|{cat_sel}|{keyword}"
        sig_key = f"faq_sig_{tab_key}"
        if st.session_state.get(sig_key) != filter_sig:
            st.session_state[sig_key] = filter_sig
            st.session_state[page_key] = 1

        current_page = st.session_state.get(page_key, 1)

        # ── FAQ 항목 출력 ─────────────────────────────────────
        start = (current_page - 1) * PAGE_SIZE
        for faq in faq_list[start: start + PAGE_SIZE]:
            if dual:
                label = f"[{faq['cat1']}] {faq['subject']}"
            else:
                label = f"[{faq['cat']}] {faq['subject']}"

            with st.expander(label, expanded=False):
                st.write(faq["content"])

        # ── 페이지네이션 컨트롤 ─────────────────────────────
        GROUP = 5
        group_idx   = (current_page - 1) // GROUP
        group_start = group_idx * GROUP + 1
        group_end   = min(group_start + GROUP - 1, total_pages)
        page_nums   = list(range(group_start, group_end + 1))

        # 버튼 수: ◀◀ ◀ + 페이지번호(최대5) + ▶ ▶▶ = 최대 9
        n_btns = 2 + len(page_nums) + 2
        # pad = (MAX_BTNS - n_btns)/2 + 여유 → 총 col_weight 항상 13 고정
        # → 버튼 개수에 관계없이 각 버튼 너비가 1/13 ≈ 7.7%로 일정
        MAX_BTNS = 9
        pad = (MAX_BTNS - n_btns) / 2 + 2
        col_weights = [pad] + [0.3] * n_btns + [pad]

        all_cols = st.columns(col_weights)
        btn_cols = all_cols[1: 1 + n_btns]
        idx = 0

        # ◀◀
        if btn_cols[idx].button("◀◀", key=f"faq_first_{tab_key}", disabled=(current_page == 1), use_container_width=True):
            st.session_state[page_key] = 1
            st.rerun()
        idx += 1
        # ◀
        if btn_cols[idx].button("◀", key=f"faq_prev_{tab_key}", disabled=(current_page == 1), use_container_width=True):
            st.session_state[page_key] = current_page - 1
            st.rerun()
        idx += 1
        # 숫자 버튼
        for n in page_nums:
            label = f"**{n}**" if n == current_page else str(n)
            if btn_cols[idx].button(label, key=f"faq_p{n}_{tab_key}", disabled=(n == current_page), use_container_width=True):
                st.session_state[page_key] = n
                st.rerun()
            idx += 1
        # ▶
        if btn_cols[idx].button("▶", key=f"faq_next_{tab_key}", disabled=(current_page == total_pages), use_container_width=True):
            st.session_state[page_key] = current_page + 1
            st.rerun()
        idx += 1
        # ▶▶
        if btn_cols[idx].button("▶▶", key=f"faq_last_{tab_key}", disabled=(current_page == total_pages), use_container_width=True):
            st.session_state[page_key] = total_pages
            st.rerun()

>>>>>>> 97cba086eff82b2eaee5f9c34f4dc36b537f8fb6


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

    cfg = _TAB_CONFIG[selected_tab]
    _render_faq_body(
<<<<<<< HEAD
        company=selected_tab,
=======
        table=cfg["table"],
        dual=cfg["dual"],
>>>>>>> 97cba086eff82b2eaee5f9c34f4dc36b537f8fb6
        tab_key=selected_tab,
    )



