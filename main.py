import streamlit as st
from app.utils import inject_global_css, go_to

from app.introduce import page_main, page_intro, page_data_guide, page_team
from app.dashboard import page_dashboard, page_analysis
from app.question  import page_faq

st.set_page_config(
    page_title="Team 6",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "main"
if "detail_page" not in st.session_state:
    st.session_state.detail_page = None

inject_global_css()

# 라우터
PAGE_MAP = {
    "main":       page_main,
    "intro":      page_intro,
    "team":       page_team,
    "data_guide": page_data_guide,
    "dashboard":  page_dashboard,
    "analysis":   page_analysis,
    "faq":        page_faq,
}

render_fn = PAGE_MAP.get(st.session_state.page)
if render_fn:
    render_fn()
else:
    st.error("알 수 없는 페이지입니다.")
    if st.button("홈으로"):
        go_to("main")

###############################























