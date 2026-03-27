
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

load_dotenv()






selected = option_menu(
    menu_title=None,  # 메뉴 타이틀 (없애면 깔끔)
    options=["Page 1", "Page 2", "Page 3"],
    icons=["house", "bar-chart", "map"],  # 아이콘 FontAwesome 사용 가능
    menu_icon="cast",  # 전체 메뉴 아이콘
    orientation="horizontal"  # 가로 메뉴
)
#


st.set_page_config(page_title="Option Menu 예제", layout="wide")
st.title("상단 메뉴 예제")

st.write(f"선택된 페이지: {selected}")

# ===== 페이지 설정 =====
st.set_page_config(
    page_title="쇼핑몰 데이터 대시보드 (MySQL)",
    page_icon="",
    layout="wide"
)
st.write("안녕하세요! 쇼핑몰 데이터 대시보드입니다.")




