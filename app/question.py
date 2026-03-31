import streamlit as st
from PIL import Image
from app.utils import render_page_header
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

_TAB_ICON = {
    "기아": "image/kia.png", "제네시스": "image/genesis.png", "현대": "image/hyundai.png", "KGM": "image/KGM.png"
}


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
                st.markdown(
                    f'<div style="line-height:3.0;">{faq["content"]}</div>',
                    unsafe_allow_html=True,
                )

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
    image = Image.open(_TAB_ICON.get(selected_tab, ''))
    col1, col2 = st.columns([1, 25], vertical_alignment="center")
    with col1:
        st.image(image, "", width = 75)
    with col2:
        st.subheader(f"{selected_tab}")
    cfg = _TAB_CONFIG[selected_tab]
    _render_faq_body(
        table=cfg["table"],
        dual=cfg["dual"],
        tab_key=selected_tab,
    )