import streamlit as st
from app.utils import (
    render_page_header, custom_success,
    FUEL_OPTIONS, FUEL_PRICE_OPTIONS,
    TYPE_OPTIONS, USAGE_OPTIONS, REGION_OPTIONS,
)

DASHBOARD_TABS = ["개요", "유가 추이", "연료별 현황", "차종·용도 현황", "지역별 현황"]

def page_dashboard():
    render_page_header("""
    <div class="page-section">
        <div class="page-section-title">📊 대시보드</div>
        <div class="page-section-body">
            전국 시도별 자동차 등록 현황과 유가 변동 흐름을 다양한 관점에서 확인하고,
            주요 분포와 변화 추이를 직관적으로 볼 수 있는 페이지입니다.
        </div>
    </div>
    """)

    _,col1 = st.columns([9,1])
    with col1:
        st.markdown("2026년 2월 기준")

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("차트 영역 1")
            st.write("예 : 연료별")
    with c2:
        with st.container(border=True):
            st.markdown("차트 영역 2")
            st.write("예:차종별")

    st.markdown("##")

    t1, t2 = st.columns(2)
    with t1:
        with st.container(border=True):
            st.markdown("차트 영역 1")
            st.write("예 : 휘발유 가격 추이")
    with t2:
        with st.container(border=True):
            st.markdown("차트 영역 2")
            st.write("예:경유 가격 추이")

    

def page_analysis():
    render_page_header("""
    <div class="page-section">
        <div class="page-section-title">📈 분석</div>
        <div class="page-section-body">
            유가 변동과 자동차 등록현황을 선택한 조건에 따라 간단한 분석을 할 수 있습니다.
        </div>
    </div>
    """)

    selected_tab = st.segmented_control(None, DASHBOARD_TABS, default="개요")

    # 탭 전환 시 초기값 보장
    selected_fuels = selected_types = selected_usages = selected_regions = []
    selected_fuel_prices = []
    year_range = (2020, 2024)

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
            selected_fuels  = st.multiselect("연료 선택", FUEL_OPTIONS,  placeholder="연료를 선택하세요")
        elif selected_tab == "차종·용도 현황":
            selected_types  = st.multiselect("차종 선택", TYPE_OPTIONS,  placeholder="차종을 선택하세요")
            selected_usages = st.multiselect("용도 선택", USAGE_OPTIONS, placeholder="용도를 선택하세요")
        elif selected_tab == "지역별 현황":
            selected_regions = st.multiselect("지역 선택", REGION_OPTIONS, placeholder="지역을 선택하세요")
        else:
            st.caption("개요 탭은 별도 필터 없이 전체 현황을 보여줍니다.")

    # ── 개요 ──
    if selected_tab == "개요":
        st.write("")
        st.subheader("⭐ 전체 현황 개요")
        cols = st.columns(6)
        for col, label, val in zip(
            cols,
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

    # ── 유가 추이 ──
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
    st.markdown("##")
    st.markdown('<div class="double-divider"></div>', unsafe_allow_html=True)

    # with st.sidebar:
    #     st.header("🔎 분석 조건")
    #     selected_fuel   = st.multiselect("연료 선택", FUEL_OPTIONS)
    #     selected_type   = st.multiselect("차종 선택", TYPE_OPTIONS)
    #     selected_usage  = st.multiselect("용도 선택", USAGE_OPTIONS)
    #     selected_region = st.multiselect("지역 선택", REGION_OPTIONS)

    # if not any([selected_fuel, selected_type, selected_usage, selected_region]):
    #     st.info("왼쪽 사이드바에서 조건을 선택하면 관련 데이터가 표시됩니다.")
    #     return

    # def fmt(lst): return ", ".join(lst) if lst else "전체"

    # custom_success(
    #     f"연료({fmt(selected_fuel)}) / 차종({fmt(selected_type)}) / "
    #     f"용도({fmt(selected_usage)}) / 지역({fmt(selected_region)})"
    # )

    # col1, col2, col3, col4 = st.columns(4)
    # col1.metric("총 등록 대수", "예시값")
    # col2.metric("선택 연료 수", len(selected_fuel))
    # col3.metric("선택 차종 수", len(selected_type))
    # col4.metric("선택 지역 수", len(selected_region))

    # st.markdown("###")
    # for (title1, title2), (c1, c2) in zip(
    #     [("연료별 분포", "차종별 분포"), ("지역별 분포", "용도별 분포")],
    #     [st.columns(2), st.columns(2)],
    # ):
    #     with c1:
    #         st.subheader(title1)
    #         with st.container(border=True): st.write(f"{title1} 차트가 들어갑니다.")
    #     with c2:
    #         st.subheader(title2)
    #         with st.container(border=True): st.write(f"{title2} 차트가 들어갑니다.")

    # st.subheader("상세 데이터")
    # with st.container(border=True):
    #     st.write("필터링된 데이터 테이블이 들어갑니다.")
    
    st.markdown("###")
    st.markdown('<div class="double-divider"></div>', unsafe_allow_html=True)