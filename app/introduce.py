import streamlit as st
from app.utils import render_page_header

# 메인/소개 공용 hero HTML
_INTRO_HERO = """
<div class="page-section">
    <div class="page-section-title">📘 서비스 소개</div>
    <div class="page-section-body">
        전국 자동차 등록 현황과 유가 변동 데이터를 파악하고,
        탐색할 수 있도록 설계한 데이터 기반 서비스입니다.
    </div>
</div>
"""

def _render_intro_content():
    st.markdown("###")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">🎯 프로젝트 목표</div>
            <div class="page-card-body">
                자동차 등록 데이터는 다양한 기준으로 구성되어 있어<br>
                단순한 표 형태만으로는 전체 구조를 파악하기 어렵습니다.<br><br>
                본 프로젝트는 자동차 등록현황 데이터와 유가 변동 데이터를 함께 활용하여,<br>
                사용자가 전반적인 현황과 두 데이터 사이 관계를 보다 쉽게 이해할 수 있는 것을 목표로 합니다.<br><br><br><br>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">⚠️ 문제 정의</div>
            <div class="page-card-body">
                자동차 등록 현황 데이터는 항목 수가 많고 분류 기준이 다양해<br>
                원하는 정보를 직관적으로 찾기 어렵습니다.<br><br>
                또한 유가 변동은 차량 선택과 등록 흐름에 영향을 줄 수 있는 요인이지만,<br>
                이를 함께 비교하고 해석할 수 있는 서비스는 제한적입니다.<br><br>
                따라서 본 서비스는 자동차 등록현황과 유가 가격을 함께 탐색할 수 있도록
                돕는<br>사용자 친화적 정보 구조 시스템을 채택하고 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("###")
    with st.container(border=True):
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
                "복잡한 데이터를 한눈에<br>이해할 수 있도록 시각화 중심으로 구성",
                "사용자가 원하는 기준을 선택해<br>필요한 정보를 직접 조회 가능",
                "연료, 차종, 용도, 지역, 유가를 기준으로<br>데이터를 비교하며 구조를 파악",
                "향후 기능 추가와 확장을<br>고려한 페이지 구조 설계",
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
                • 사용자 중심의 탐색형 정보 서비스 구현<br><br>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("##")
    st.markdown('<div class="double-divider"></div>', unsafe_allow_html=True)

# -----------------------
# 페이지 함수
# -----------------------
def page_main():
    render_page_header(_INTRO_HERO)
    _render_intro_content()

def page_intro():   # nav 직접 접근 시에도 동일 화면
    render_page_header(_INTRO_HERO)
    _render_intro_content()

def page_data_guide():
    render_page_header("""
    <div class="page-section">
        <div class="page-section-title">🗂️ 데이터 설명</div>
        <div class="page-section-body">
            서비스에서 활용하는 자동차 등록 현황 데이터와 유가 변동 데이터의
            구성 항목 및 분류 기준을 안내합니다.
        </div>
    </div>
    """)
    st.markdown("###")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">⛽ 연료 기준</div>
            <div class="page-card-body">
                • 휘발유<br>• 경유<br>• 전기<br>
                • 하이브리드(휘발유+전기)<br>• 하이브리드(경유+전기)<br><br>
                내연기관차와 친환경차의 구성 차이를 비교할 수 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">🚘 차종 기준</div>
            <div class="page-card-body">
                • 승용<br>• 승합<br>• 화물<br>• 특수<br><br><br>
                차량 유형별 등록 현황과 분포를 확인할 수 있습니다.<br>
            </div>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">🏷️ 용도 기준</div>
            <div class="page-card-body">
                • 비사업용<br>• 사업용<br><br>
                개인 및 기업·운송 목적 차량의 구성을 비교할 수 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="page-card">
            <div class="page-card-title">🗺️ 지역 기준</div>
            <div class="page-card-body">
                • 시: 서울, 부산, 인천, 대구, 대전, 광주, 울산, 세종<br>
                • 도: 경기, 충북, 충남, 전남, 경북, 경남, 강원, 전북, 제주<br><br>
                전국 17개 시도 기준입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("###")
    st.markdown("""
    <div class="page-section">
        <div class="page-section-title">📌 데이터 활용 방식</div>
        <div class="page-section-body">
            대시보드 페이지에서는 각 기준별 전체 흐름을 확인할 수 있으며,
            분석 페이지에서는 여러 조건을 조합하여 보다 구체적인 현황을 탐색할 수 있습니다.
        </div>
    </div>
    <div class="page-section">
        <div class="page-section-title">🔎 해석 시 참고사항</div>
        <div class="page-section-body">
            실제 데이터 연동 단계에서는 데이터 원본의 구성 방식과 기준에 따라
            일부 분류 항목명 또는 해석 방식이 달라질 수 있습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("##")
    st.markdown('<div class="double-divider"></div>', unsafe_allow_html=True)

def page_team():
    render_page_header("""
    <div class="page-section">
        <div class="page-section-title">👥 팀 소개</div>
        <div class="page-section-body">
            3명의 팀원이 역할을 분담하여 기획, 데이터 구성,
            페이지 설계, 서비스 구현을 함께 수행하였습니다.
        </div>
    </div>
    """)
    st.markdown("##")
    col1, col2, col3 = st.columns(3)
    for col, name, chip, body in zip(
        [col1, col2, col3],
        ["팀원 1 : 임준", "팀원 2 : 우석현", "팀원 3 : 한경찬"],
        ["기획 · DB설계", "페이지 개발 · 분석 지원", "UI 구현 · 디자인 구성"],
        [   
            "<br>프로젝트의 전체 방향성을 설정하고,<br>서비스 목적과 페이지 구조를 설계하였습니다.<br><br>"
            "서비스 흐름과 주요 기능 구성을 담당하였습니다.<br><br>",
            "<br>자동차 등록 현황 데이터의 구조를 정리하고,<br>조회 및 시각화에 필요한 데이터 기준을 구성하였습니다.<br><br>"
            "탭별 현황 페이지의 분석 방향과 데이터 활용 방식을<br>함께 설계하였습니다.",
            "<br>Streamlit 기반 화면 구현과 페이지 연결, 탭 구성,<br>사이드바 필터 등을 개발하였습니다.<br><br>"
            "카드형 레이아웃과 페이지 전반의 디자인 요소를<br>반영하였습니다.",
        ],
    ):
        col.markdown(
            f'<div class="page-card"><div class="page-card-title">{name}</div>'
            f'<div class="page-chip">{chip}</div>'
            f'<div class="page-card-body">{body}</div></div>',
            unsafe_allow_html=True,
        )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="page-section">
            <div class="page-section-title">🤝 협업 방식</div>
            <div class="page-section-body">
                기획, 데이터, 구현 역할을 분담하되,
                전체 서비스 흐름과 핵심 기능은 함께 논의하며 결정하였습니다.<br><br>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="page-section">
            <div class="page-section-title">✨ 팀의 강점</div>
            <div class="page-section-body">
                유가와 자동차 등록 현황 데이터를 함께 탐색하고,<br>
                대시보드 시각화를 통해 이들의 관계성을 파악할 수 있다는 점이 핵심 강점입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("##")
    st.markdown('<div class="double-divider"></div>', unsafe_allow_html=True)