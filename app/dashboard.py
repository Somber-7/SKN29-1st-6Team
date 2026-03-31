import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from app.utils import (
    render_page_header, custom_success,
    FUEL_OPTIONS, FUEL_PRICE_OPTIONS,
    TYPE_OPTIONS, USAGE_OPTIONS, REGION_OPTIONS,
)
from app.db_connect import (
    DB_connect, DB_CONFIG,
    get_fuel_registration_data, get_type_registration_data,
    get_national_average_fuel_price_trend
)

DASHBOARD_TABS = ["유가 추이", "연료별 현황", "차종 현황" ,"용도 현황"]

def load_dynamic_options():
    """
    데이터베이스에서 동적 옵션(연료, 차종 등)을 로드하고, 실패 시 기본값을 사용합니다.
    """
    default_options = {
        "FUEL_OPTIONS": ["휘발유", "경유", "전기", "하이브리드(휘발유+전기)", "하이브리드(경유+전기)"],
        "FUEL_PRICE_OPTIONS": ["휘발유", "경유"],
        "TYPE_OPTIONS": ["승용", "승합", "화물", "특수"],
        "USAGE_OPTIONS": ["비사업용", "사업용"],
        "REGION_OPTIONS": ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]
    }

    option_methods = {
        "FUEL_OPTIONS": "get_fuel_options",
        "FUEL_PRICE_OPTIONS": "get_fuel_price_options",
        "TYPE_OPTIONS": "get_type_options",
        "USAGE_OPTIONS": "get_usage_options",
        "REGION_OPTIONS": "get_region_options"
    }

    loaded_options = default_options.copy()
    with DB_connect(DB_CONFIG) as db:
        print(DB_CONFIG)
        try:
            for key, method_name in option_methods.items():
                if hasattr(db, method_name):
                    df = getattr(db, method_name)()
                    if not df.empty and 'CODE_NAME' in df.columns:
                        db_options = df['CODE_NAME'].tolist()
                        if db_options:
                            loaded_options[key] = db_options
                else:
                    print(f"Warning: Method {method_name} not found in DB_connect. Using default for {key}.")
        except Exception as e:
            print(f"Database error during option loading: {e}. Using default values.")
            # In case of any exception, return the default dictionary
            return default_options
        finally:
            db.close()
    return loaded_options


# Load dynamic options once and use them throughout the app
dynamic_options = load_dynamic_options()
FUEL_OPTIONS = dynamic_options["FUEL_OPTIONS"]
FUEL_PRICE_OPTIONS = dynamic_options["FUEL_PRICE_OPTIONS"]
TYPE_OPTIONS = dynamic_options["TYPE_OPTIONS"]
USAGE_OPTIONS = dynamic_options["USAGE_OPTIONS"]
REGION_OPTIONS = dynamic_options["REGION_OPTIONS"]

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

    STAT_YM = '202602'
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("연료별 등록 현황")
        with st.container(border=True):
            # 함수 파라미터 제거됨
            fuel_data = get_fuel_registration_data(STAT_YM) 
            
            if not fuel_data.empty:
                # Plotly 파이 차트 생성
                fig_fuel = px.pie(fuel_data, values='등록대수', names='연료', hole=0.3)
                fig_fuel.update_traces(textposition='inside', textinfo='percent+label')
                fig_fuel.update_layout(paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
                st.plotly_chart(fig_fuel, use_container_width=True)
            else:
                st.info("연료별 등록 현황 데이터가 없습니다.")
                
    with c2:
        st.subheader("차종별 등록 현황")
        with st.container(border=True):
            # 함수 파라미터 제거됨
            type_data = get_type_registration_data(STAT_YM) 
            
            if not type_data.empty:
                # Plotly 파이 차트 생성
                fig_type = px.pie(type_data, values='등록대수', names='차종', hole=0.3)
                fig_type.update_traces(textposition='inside', textinfo='percent+label')
                fig_type.update_layout(paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
                st.plotly_chart(fig_type, use_container_width=True)
            else:
                st.info("차종별 등록 현황 데이터가 없습니다.")

    st.markdown("##")

    t1, t2 = st.columns(2)
    price_data = get_national_average_fuel_price_trend()

    if not price_data.empty:
        price_data['DATE'] = pd.to_datetime(price_data['STAT_YM'], format='%Y%m')
        gasoline_data = price_data[price_data['FUEL_NM'] == '휘발유']
        diesel_data = price_data[price_data['FUEL_NM'] == '경유']

        with t1:
            st.subheader("전국 휘발유 가격 추이")
            with st.container(border=True):
                if not gasoline_data.empty:
                    fig_gas = px.line(gasoline_data, x='DATE', y='AVG_PRICE', color_discrete_sequence=['crimson'])
                    fig_gas.update_layout(xaxis_title="기간",
                                          yaxis_title="평균 가격 (원/L)",
                                          paper_bgcolor='#f8fbfe',
                                          plot_bgcolor='#f8fbfe',
                                          margin=dict(r=50))
                    st.plotly_chart(fig_gas, use_container_width=True)
                else:
                    st.info("휘발유 가격 데이터가 없습니다.")
        with t2:
            st.subheader("전국 경유 가격 추이")
            with st.container(border=True):
                if not diesel_data.empty:
                    fig_diesel = px.line(diesel_data, x='DATE', y='AVG_PRICE', color_discrete_sequence=['royalblue'])
                    fig_diesel.update_layout(xaxis_title="기간",
                                             yaxis_title="평균 가격 (원/L)",
                                             paper_bgcolor='#f8fbfe',
                                             plot_bgcolor='#f8fbfe',
                                             margin=dict(r=50))
                    st.plotly_chart(fig_diesel, use_container_width=True)
                else:
                    st.info("경유 가격 데이터가 없습니다.")
    else:
        st.info("유가 추이 데이터를 불러올 수 없습니다.")

    

def page_analysis():
    render_page_header("""
    <div class="page-section">
        <div class="page-section-title">📈 분석</div>
        <div class="page-section-body">
            유가 변동과 자동차 등록현황을 선택한 조건에 따라 간단한 분석을 할 수 있습니다.
        </div>
    </div>
    """)

    selected_tab = st.segmented_control(None, DASHBOARD_TABS, default="유가 추이")

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
        st.header("📌 조건 필터")

        if selected_tab == "유가 추이":
            year_range = st.slider("기간 선택", min_value=2021, max_value=2026, value=(2021, 2026))
            st.divider()
            selected_regions = st.multiselect("지역 선택", REGION_OPTIONS, placeholder="지역을 선택하세요")
        elif selected_tab == "연료별 현황":
            selected_fuels  = st.multiselect("연료 선택", FUEL_OPTIONS,  placeholder="연료를 선택하세요")
        elif selected_tab == "차종 현황":
            selected_types  = st.multiselect("차종 선택", TYPE_OPTIONS,  placeholder="차종을 선택하세요")
        elif selected_tab == "용도 현황":
            selected_usages = st.multiselect("용도 선택", USAGE_OPTIONS, placeholder="용도를 선택하세요")
        elif selected_tab == "지역별 현황":
            selected_regions = st.multiselect("지역 선택", REGION_OPTIONS, placeholder="지역을 선택하세요")

    if selected_tab == "유가 추이":
        st.subheader("💰 유가 추이")
        if not selected_regions:
            st.info("왼쪽 사이드바에서 지역을 선택하면 유가 추이 차트가 표시됩니다.")
        else:
            custom_success(f"선택 지역: {', '.join(selected_regions)} / 기간: {year_range[0]} ~ {year_range[1]}")
            
            # DB에서 유가 데이터 불러오기
            with DB_connect(DB_CONFIG) as db:
                print(DB_CONFIG)
                df_price = db.get_fuel_price_trend()
                
            if not df_price.empty:
                # 기간 및 지역 필터링
                df_price['YEAR'] = df_price['STAT_YM'].str[:4].astype(int)
                df_filtered = df_price[(df_price['YEAR'] >= year_range[0]) & (df_price['YEAR'] <= year_range[1])]
                df_filtered = df_filtered[df_filtered['REGION_NM'].isin(selected_regions)]
                
                # X축을 위한 날짜 형식 변환
                df_filtered['DATE'] = pd.to_datetime(df_filtered['STAT_YM'], format='%Y%m')
                
                # 휘발유, 경유 데이터 분리
                df_gasoline = df_filtered[df_filtered['FUEL_NM'] == '휘발유']
                df_diesel = df_filtered[df_filtered['FUEL_NM'] == '경유']
                
                st.markdown("### 휘발유 가격 추이")
                with st.container(border=True):
                    if not df_gasoline.empty:
                        fig_gas = px.line(df_gasoline, x="DATE", y="AVG_PRICE", color="REGION_NM",
                                          markers=True,
                                          color_discrete_sequence=px.colors.qualitative.Vivid, 
                                          labels={"DATE": "시간", "AVG_PRICE": "평균 가격(원/리터)", "REGION_NM": "지역"})
                        fig_gas.update_layout(paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
                        st.plotly_chart(fig_gas, use_container_width=True)
                    else:
                        st.warning("선택한 조건에 해당하는 휘발유 데이터가 없습니다.")
                        
                st.markdown("### 경유 가격 추이")
                with st.container(border=True):
                    if not df_diesel.empty:
                        fig_diesel = px.line(df_diesel, x="DATE", y="AVG_PRICE", color="REGION_NM",
                                             markers=True,
                                             color_discrete_sequence=px.colors.qualitative.Vivid,
                                             labels={"DATE": "시간", "AVG_PRICE": "평균 가격(원/리터)", "REGION_NM": "지역"})
                        fig_diesel.update_layout(paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
                        st.plotly_chart(fig_diesel, use_container_width=True)
                    else:
                        st.warning("선택한 조건에 해당하는 경유 데이터가 없습니다.")
            else:
                st.error("데이터베이스에서 유가 데이터를 불러오지 못했습니다.")
                
    # ── 연료별 현황 ──
    elif selected_tab == "연료별 현황":
        st.subheader("⛽ 연료별 현황")
        if not selected_fuels:
            st.info("왼쪽 사이드바에서 연료를 선택하면 관련 차트와 통계가 표시됩니다.")
        else:
            with DB_connect(DB_CONFIG) as db:
                df_trend = db.get_trend_analysis_data()

            if df_trend.empty:
                st.error("데이터를 불러오는 데 실패했습니다.")
                return

            # 날짜 형식 변환 및 필터링
            df_trend['DATE'] = pd.to_datetime(df_trend['STAT_YM'], format='%Y%m')
            df_filtered = df_trend[df_trend['FUEL_NM'].isin(selected_fuels)]

            if df_filtered.empty:
                st.warning("선택하신 조건에 해당하는 데이터가 없습니다.")
                return

            custom_success(f"선택 연료: {', '.join(selected_fuels)}")

            # 데이터 집계
            df_reg_agg = df_filtered.groupby(['DATE', 'FUEL_NM'])['REG_CNT'].sum().reset_index()
            
            # 2. 연료 및 날짜순 정렬 후 증감폭(diff) 계산 추가
            df_reg_agg = df_reg_agg.sort_values(by=['FUEL_NM', 'DATE'])
            df_reg_agg['REG_CNT_DIFF'] = df_reg_agg.groupby('FUEL_NM')['REG_CNT'].diff()
            
            # 첫 달은 이전 달 데이터가 없으므로 NaN이 됩니다. 이를 0으로 채웁니다.
            df_reg_agg['REG_CNT_DIFF'] = df_reg_agg['REG_CNT_DIFF'].fillna(0)

            df_price_agg = df_trend.groupby('DATE').agg(
                GASOLINE_PRICE=('GASOLINE_PRICE', 'mean'),
                DIESEL_PRICE=('DIESEL_PRICE', 'mean')
            ).reset_index()

                # 연료별 색상 매핑
            fuel_color_map = {
                '휘발유': '#F59E0B', 
                '경유': '#64748B', 
                '전기': '#10B981', 
                '하이브리드(휘발유+전기)': '#EC4899', 
                '하이브리드(경유+전기)': '#06B6D4'
            }

            # --- 이중 축 차트 생성 ---
            fig = go.Figure()

            # 등록 대수 증감폭 라인 추가 (좌측 Y축)
            for fuel in selected_fuels:
                df_fuel = df_reg_agg[df_reg_agg['FUEL_NM'] == fuel]
                
                # 딕셔너리에서 연료명(fuel)에 해당하는 색상을 고정으로 할당
                fig.add_trace(go.Scatter(
                    x=df_fuel['DATE'], 
                    y=df_fuel['REG_CNT_DIFF'], 
                    mode='lines+markers', 
                    name=f'{fuel} 증감폭',
                    line=dict(color=fuel_color_map[fuel]) # 👈 지정한 색상이 여기서 적용됩니다.
                ))

            # 유가 라인 추가 (우측 Y축) - 진한 실선과 두께(width=3)로 기준선 강조
            fig.add_trace(go.Scatter(
                x=df_price_agg['DATE'], 
                y=df_price_agg['GASOLINE_PRICE'], 
                mode='lines', 
                name='휘발유 가격', 
                line=dict(color='crimson', width=3),
                yaxis='y2'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_price_agg['DATE'], 
                y=df_price_agg['DIESEL_PRICE'], 
                mode='lines', 
                name='경유 가격', 
                line=dict(color='royalblue', width=3),
                yaxis='y2'
            ))

            fig.update_layout(
                title='연료별 등록 대수 증감폭과 유가 추이 비교',
                yaxis=dict(title='등록 대수 증감폭 (대)'), # Y축 이름 변경
                yaxis2=dict(title='평균 유가 (원/L)', overlaying='y', side='right'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                paper_bgcolor='#f8fbfe',
                plot_bgcolor='#f8fbfe'
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- 상관분석 및 히트맵 생성 ---
            st.markdown("### 📊 유가 및 연료별 등록 증감폭 상관관계")
            
            # 1. 차량 데이터를 날짜 기준, 연료별 컬럼으로 넓게 펴기 (Pivot)
            df_reg_pivot = df_reg_agg.pivot(index='DATE', columns='FUEL_NM', values='REG_CNT_DIFF').reset_index()
            
            # 2. 유가 데이터와 차량 데이터 병합
            df_corr_base = pd.merge(df_price_agg, df_reg_pivot, on='DATE', how='inner')
            
            # 3. 날짜 컬럼 제외하고 상관계수 행렬 계산
            corr_matrix = df_corr_base.drop(columns=['DATE']).corr()
            
            # 4. Plotly Heatmap 그리기
            fig_corr = px.imshow(corr_matrix, 
                                 text_auto=".2f",
                                 aspect="auto",
                                 color_continuous_scale="RdBu_r",
                                 zmin=-1, zmax=1)
            
            fig_corr.update_layout(title='변수 간 피어슨 상관계수 (-1 ~ 1)', paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
            st.plotly_chart(fig_corr, use_container_width=True)


            # --- 교차 상관분석 (시차 적용) ---
            st.markdown("### 시차 적용 교차 상관분석 (Lag 0~6개월)")
            
            lag_results = []
            
            # 날짜순 정렬 보장
            df_corr_sorted = df_corr_base.sort_values('DATE').copy()
            
            # 0개월부터 3개월까지 시차(Lag) 반복
            for lag in range(7):
                df_temp = df_corr_sorted.copy()
                
                # 핵심 로직: 유가 데이터를 lag 개월만큼 뒤로 미루기
                df_temp['GASOLINE_PRICE'] = df_temp['GASOLINE_PRICE'].shift(lag)
                df_temp['DIESEL_PRICE'] = df_temp['DIESEL_PRICE'].shift(lag)
                
                # 데이터를 미루면서 생긴 빈칸(결측치) 제거
                df_temp = df_temp.dropna()
                
                # 빈 데이터프레임이 아닐 경우에만 상관계수 계산
                if not df_temp.empty:
                    corr_m = df_temp.drop(columns=['DATE']).corr()
                    
                    # 선택된 각 차종별로 휘발유/경유 가격과의 상관계수 추출하여 리스트에 저장
                    for fuel in selected_fuels:
                        if fuel in corr_m.columns:
                            lag_results.append({
                                '시차': f'{lag}개월 뒤',
                                '차종': fuel,
                                '기준': '휘발유 가격',
                                '상관계수': corr_m.loc['GASOLINE_PRICE', fuel]
                            })
                            lag_results.append({
                                '시차': f'{lag}개월 뒤',
                                '차종': fuel,
                                '기준': '경유 가격',
                                '상관계수': corr_m.loc['DIESEL_PRICE', fuel]
                            })

            # 수집된 결과를 데이터프레임으로 변환
            df_lag_corr = pd.DataFrame(lag_results)

# 시각화를 위해 휘발유/경유 데이터 분리
            df_lag_gas = df_lag_corr[df_lag_corr['기준'] == '휘발유 가격']
            df_lag_diesel = df_lag_corr[df_lag_corr['기준'] == '경유 가격']
            
            # 그래프를 나란히 배치하기 위해 컬럼 2개 생성
            lag_col1, lag_col2 = st.columns(2)
            
            with lag_col1:
                with st.container(border=True):
                    # 1. 휘발유 상관계수 그래프
                    fig_lag_gas = px.line(df_lag_gas, x='시차', y='상관계수', color='차종', markers=True,
                                          title='휘발유 가격 변동의 영향',
                                          labels={'시차': '경과 시간', '상관계수': '상관계수'})
                    
                    fig_lag_gas.update_layout(paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
                    fig_lag_gas.update_yaxes(range=[-0.5, 0.5], zeroline=True, zerolinewidth=2, zerolinecolor='black')
                    
                    st.plotly_chart(fig_lag_gas, use_container_width=True)

            with lag_col2:
                with st.container(border=True):
                    # 2. 경유 상관계수 그래프
                    fig_lag_diesel = px.line(df_lag_diesel, x='시차', y='상관계수', color='차종', markers=True,
                                             title='경유 가격 변동의 영향',
                                             labels={'시차': '경과 시간', '상관계수': '상관계수'})
                    
                    fig_lag_diesel.update_layout(paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
                    fig_lag_diesel.update_yaxes(range=[-0.5, 0.5], zeroline=True, zerolinewidth=2, zerolinecolor='black')
                    
                    st.plotly_chart(fig_lag_diesel, use_container_width=True)

    # ── 차종 현황 ──
    elif selected_tab == "차종 현황":
        st.subheader("🚘 차종 현황")
        if not selected_types:
            st.info("왼쪽 사이드바에서 차종을 선택하면 관련 차트와 통계가 표시됩니다.")
        else:
            with DB_connect(DB_CONFIG) as db:
                df_trend = db.get_trend_analysis_data()

            if df_trend.empty:
                st.error("데이터를 불러오는 데 실패했습니다.")
                return

            # 날짜 형식 변환 및 필터링
            df_trend['DATE'] = pd.to_datetime(df_trend['STAT_YM'], format='%Y%m')
            df_filtered = df_trend[df_trend['TYPE_NM'].isin(selected_types)]

            if df_filtered.empty:
                st.warning("선택하신 조건에 해당하는 데이터가 없습니다.")
                return

            custom_success(f"선택 차종: {', '.join(selected_types)}")

            # 데이터 집계
            df_reg_agg = df_filtered.groupby(['DATE', 'TYPE_NM'])['REG_CNT'].sum().reset_index()
            
            # 2. 차종 및 날짜순 정렬 후 증감폭(diff) 계산 추가
            df_reg_agg = df_reg_agg.sort_values(by=['TYPE_NM', 'DATE'])
            df_reg_agg['REG_CNT_DIFF'] = df_reg_agg.groupby('TYPE_NM')['REG_CNT'].diff()
            
            # 첫 달은 이전 달 데이터가 없으므로 NaN이 됩니다. 이를 0으로 채웁니다.
            df_reg_agg['REG_CNT_DIFF'] = df_reg_agg['REG_CNT_DIFF'].fillna(0)

            df_price_agg = df_trend.groupby('DATE').agg(
                GASOLINE_PRICE=('GASOLINE_PRICE', 'mean'),
                DIESEL_PRICE=('DIESEL_PRICE', 'mean')
            ).reset_index()

            # --- 이중 축 차트 생성 ---
            fig = go.Figure()

            type_color_map = {
                            '승용': '#10B981',
                            '승합': '#8B5CF6',
                            '화물': '#F59E0B',
                            '특수': '#64748B'
                        }

            # 등록 대수 증감폭 라인 추가 (좌측 Y축)
            for type in selected_types:
                df_type = df_reg_agg[df_reg_agg['TYPE_NM'] == type]
                
                fig.add_trace(go.Scatter(
                    x=df_type['DATE'], 
                    y=df_type['REG_CNT_DIFF'], 
                    mode='lines+markers', 
                    name=f'{type} 증감폭',
                    fill='tozeroy', 
                    opacity=0.5, 
                    line=dict(color=type_color_map[type]) 
                ))

            # 유가 라인
            fig.add_trace(go.Scatter(
                x=df_price_agg['DATE'], 
                y=df_price_agg['GASOLINE_PRICE'], 
                mode='lines', 
                name='휘발유 가격', 
                line=dict(color='crimson', width=3),
                yaxis='y2'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_price_agg['DATE'], 
                y=df_price_agg['DIESEL_PRICE'], 
                mode='lines', 
                name='경유 가격', 
                line=dict(color='royalblue', width=3),
                yaxis='y2'
            ))
            fig.update_layout(
                title='차종별 등록 대수 증감폭과 유가 추이 비교',
                yaxis=dict(title='등록 대수 증감폭 (대)'), 
                yaxis2=dict(title='평균 유가 (원/L)', overlaying='y', side='right'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                paper_bgcolor='#f8fbfe',
                plot_bgcolor='#f8fbfe'
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- 상관분석 및 히트맵 생성 ---
            st.markdown("### 📊 유가 및 차종별 등록 증감폭 상관관계")
            
            # 1. 차량 데이터를 날짜 기준, 차종별 컬럼으로 넓게 펴기 (Pivot)
            df_reg_pivot = df_reg_agg.pivot(index='DATE', columns='TYPE_NM', values='REG_CNT_DIFF').reset_index()
            
            # 2. 유가 데이터와 차량 데이터 병합
            df_corr_base = pd.merge(df_price_agg, df_reg_pivot, on='DATE', how='inner')
            
            # 3. 날짜 컬럼 제외하고 상관계수 행렬 계산
            corr_matrix = df_corr_base.drop(columns=['DATE']).corr()
            
            # 4. Plotly Heatmap 그리기
            fig_corr = px.imshow(corr_matrix, 
                                 text_auto=".2f",
                                 aspect="auto",
                                 color_continuous_scale="RdBu_r",
                                 zmin=-1, zmax=1)
            
            fig_corr.update_layout(title='변수 간 피어슨 상관계수 (-1 ~ 1)', paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
            st.plotly_chart(fig_corr, use_container_width=True)


            # --- 교차 상관분석 (시차 적용) ---
            st.markdown("### 시차 적용 교차 상관분석 (Lag 0~6개월)")
            
            lag_results = []
            
            # 날짜순 정렬 보장
            df_corr_sorted = df_corr_base.sort_values('DATE').copy()
            
            # 0개월부터 6개월까지 시차(Lag) 반복
            for lag in range(7):
                df_temp = df_corr_sorted.copy()
                
                # 핵심 로직: 유가 데이터를 lag 개월만큼 뒤로 미루기
                df_temp['GASOLINE_PRICE'] = df_temp['GASOLINE_PRICE'].shift(lag)
                df_temp['DIESEL_PRICE'] = df_temp['DIESEL_PRICE'].shift(lag)
                
                # 데이터를 미루면서 생긴 빈칸(결측치) 제거
                df_temp = df_temp.dropna()
                
                # 빈 데이터프레임이 아닐 경우에만 상관계수 계산
                if not df_temp.empty:
                    corr_m = df_temp.drop(columns=['DATE']).corr()
                    
                    # 선택된 각 차종별로 휘발유/경유 가격과의 상관계수 추출하여 리스트에 저장
                    for type in selected_types:
                        if type in corr_m.columns:
                            lag_results.append({
                                '시차': f'{lag}개월 뒤',
                                '차종': type,
                                '기준': '휘발유 가격',
                                '상관계수': corr_m.loc['GASOLINE_PRICE', type]
                            })
                            lag_results.append({
                                '시차': f'{lag}개월 뒤',
                                '차종': type,
                                '기준': '경유 가격',
                                '상관계수': corr_m.loc['DIESEL_PRICE', type]
                            })

            # 수집된 결과를 데이터프레임으로 변환
            df_lag_corr = pd.DataFrame(lag_results)

            # 시각화를 위해 휘발유/경유 데이터 분리
            df_lag_gas = df_lag_corr[df_lag_corr['기준'] == '휘발유 가격']
            df_lag_diesel = df_lag_corr[df_lag_corr['기준'] == '경유 가격']
            
            # 그래프를 나란히 배치하기 위해 컬럼 2개 생성
            lag_col1, lag_col2 = st.columns(2)
            
            with lag_col1:
                with st.container(border=True):
                    # 1. 휘발유 상관계수 그래프
                    fig_lag_gas = px.line(df_lag_gas, x='시차', y='상관계수', color='차종', markers=True,
                                          title='휘발유 가격 변동의 영향',
                                          labels={'시차': '경과 시간', '상관계수': '상관계수'})
                    
                    fig_lag_gas.update_layout(paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
                    fig_lag_gas.update_yaxes(range=[-0.5, 0.5], zeroline=True, zerolinewidth=2, zerolinecolor='black')
                    
                    st.plotly_chart(fig_lag_gas, use_container_width=True)

            with lag_col2:
                with st.container(border=True):
                    # 2. 경유 상관계수 그래프
                    fig_lag_diesel = px.line(df_lag_diesel, x='시차', y='상관계수', color='차종', markers=True,
                                             title='경유 가격 변동의 영향',
                                             labels={'시차': '경과 시간', '상관계수': '상관계수'})
                    
                    fig_lag_diesel.update_layout(paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
                    fig_lag_diesel.update_yaxes(range=[-0.5, 0.5], zeroline=True, zerolinewidth=2, zerolinecolor='black')
                    
                    st.plotly_chart(fig_lag_diesel, use_container_width=True)

    # ── 용도 현황 ──
    elif selected_tab == "용도 현황":
        st.subheader("📋 용도 현황")
        if not selected_usages:
            st.info("왼쪽 사이드바에서 용도를 선택하면 관련 차트와 통계가 표시됩니다.")
        else:
            with DB_connect(DB_CONFIG) as db:
                df_trend = db.get_trend_analysis_data()

            if df_trend.empty:
                st.error("데이터를 불러오는 데 실패했습니다.")
                return

            # 날짜 형식 변환 및 필터링
            df_trend['DATE'] = pd.to_datetime(df_trend['STAT_YM'], format='%Y%m')
            df_filtered = df_trend[df_trend['USAGE_NM'].isin(selected_usages)]

            if df_filtered.empty:
                st.warning("선택하신 조건에 해당하는 데이터가 없습니다.")
                return

            custom_success(f"선택 용도: {', '.join(selected_usages)}")

            # 데이터 집계
            df_reg_agg = df_filtered.groupby(['DATE', 'USAGE_NM'])['REG_CNT'].sum().reset_index()
            
            # 2. 용도 및 날짜순 정렬 후 증감폭(diff) 계산 추가
            df_reg_agg = df_reg_agg.sort_values(by=['USAGE_NM', 'DATE'])
            df_reg_agg['REG_CNT_DIFF'] = df_reg_agg.groupby('USAGE_NM')['REG_CNT'].diff()
            
            # 첫 달은 이전 달 데이터가 없으므로 NaN이 됩니다. 이를 0으로 채웁니다.
            df_reg_agg['REG_CNT_DIFF'] = df_reg_agg['REG_CNT_DIFF'].fillna(0)

            df_price_agg = df_trend.groupby('DATE').agg(
                GASOLINE_PRICE=('GASOLINE_PRICE', 'mean'),
                DIESEL_PRICE=('DIESEL_PRICE', 'mean')
            ).reset_index()

            # --- 이중 축 차트 생성 ---
            fig = go.Figure()

            for usage in selected_usages:
                df_usage = df_reg_agg[df_reg_agg['USAGE_NM'] == usage]
                fig.add_trace(go.Waterfall(
                    x=df_usage['DATE'], 
                    y=df_usage['REG_CNT_DIFF'], 
                    measure=['relative'] * len(df_usage),
                    name=f'{usage} 증감폭',
                    orientation='v',
                    decreasing=dict(marker=dict(color='blue')),
                    increasing=dict(marker=dict(color='red')),
                    totals=dict(marker=dict(color='gray'))
                ))
            # 유가 라인
            fig.add_trace(go.Scatter(
                x=df_price_agg['DATE'], 
                y=df_price_agg['GASOLINE_PRICE'], 
                mode='lines', 
                name='휘발유 가격', 
                line=dict(color='crimson', width=3),
                yaxis='y2'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_price_agg['DATE'], 
                y=df_price_agg['DIESEL_PRICE'], 
                mode='lines', 
                name='경유 가격', 
                line=dict(color='royalblue', width=3),
                yaxis='y2'
            ))

            fig.update_layout(
                title='용도별 등록 대수 증감폭과 유가 추이 비교',
                yaxis=dict(title='등록 대수 증감폭 (대)'), 
                yaxis2=dict(title='평균 유가 (원/L)', overlaying='y', side='right'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                paper_bgcolor='#f8fbfe',
                plot_bgcolor='#f8fbfe',
                waterfallmode='group' # 여러 용도(예: 영업용, 비영업용)가 선택되었을 때 막대가 겹치지 않고 나란히 보이게 함
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- 상관분석 및 히트맵 생성 ---
            st.markdown("### 📊 유가 및 용도별 등록 증감폭 상관관계")
            
            # 1. 차량 데이터를 날짜 기준, 용도별 컬럼으로 넓게 펴기 (Pivot)
            df_reg_pivot = df_reg_agg.pivot(index='DATE', columns='USAGE_NM', values='REG_CNT_DIFF').reset_index()
            
            # 2. 유가 데이터와 차량 데이터 병합
            df_corr_base = pd.merge(df_price_agg, df_reg_pivot, on='DATE', how='inner')
            
            # 3. 날짜 컬럼 제외하고 상관계수 행렬 계산
            corr_matrix = df_corr_base.drop(columns=['DATE']).corr()
            
            # 4. Plotly Heatmap 그리기
            fig_corr = px.imshow(corr_matrix, 
                                 text_auto=".2f",
                                 aspect="auto",
                                 color_continuous_scale="RdBu_r",
                                 zmin=-1, zmax=1)
            
            fig_corr.update_layout(title='변수 간 피어슨 상관계수 (-1 ~ 1)', paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
            st.plotly_chart(fig_corr, use_container_width=True)


            # --- 교차 상관분석 (시차 적용) ---
            st.markdown("### 시차 적용 교차 상관분석 (Lag 0~6개월)")
            
            lag_results = []
            
            # 날짜순 정렬 보장
            df_corr_sorted = df_corr_base.sort_values('DATE').copy()
            
            # 0개월부터 6개월까지 시차(Lag) 반복
            for lag in range(7):
                df_temp = df_corr_sorted.copy()
                
                # 핵심 로직: 유가 데이터를 lag 개월만큼 뒤로 미루기
                df_temp['GASOLINE_PRICE'] = df_temp['GASOLINE_PRICE'].shift(lag)
                df_temp['DIESEL_PRICE'] = df_temp['DIESEL_PRICE'].shift(lag)
                
                # 데이터를 미루면서 생긴 빈칸(결측치) 제거
                df_temp = df_temp.dropna()
                
                # 빈 데이터프레임이 아닐 경우에만 상관계수 계산
                if not df_temp.empty:
                    corr_m = df_temp.drop(columns=['DATE']).corr()
                    
                    # 선택된 각 용도별로 휘발유/경유 가격과의 상관계수 추출하여 리스트에 저장
                    for usage in selected_usages:
                        if usage in corr_m.columns:
                            lag_results.append({
                                '시차': f'{lag}개월 뒤',
                                '용도': usage,
                                '기준': '휘발유 가격',
                                '상관계수': corr_m.loc['GASOLINE_PRICE', usage]
                            })
                            lag_results.append({
                                '시차': f'{lag}개월 뒤',
                                '용도': usage,
                                '기준': '경유 가격',
                                '상관계수': corr_m.loc['DIESEL_PRICE', usage]
                            })

            # 수집된 결과를 데이터프레임으로 변환
            df_lag_corr = pd.DataFrame(lag_results)

            # 시각화를 위해 휘발유/경유 데이터 분리
            df_lag_gas = df_lag_corr[df_lag_corr['기준'] == '휘발유 가격']
            df_lag_diesel = df_lag_corr[df_lag_corr['기준'] == '경유 가격']
            
            # 그래프를 나란히 배치하기 위해 컬럼 2개 생성
            lag_col1, lag_col2 = st.columns(2)
            
            with lag_col1:
                with st.container(border=True):
                    # 1. 휘발유 상관계수 그래프
                    fig_lag_gas = px.line(df_lag_gas, x='시차', y='상관계수', color='용도', markers=True,
                                          title='휘발유 가격 변동의 영향',
                                          labels={'시차': '경과 시간', '상관계수': '상관계수'})
                    
                    fig_lag_gas.update_layout(paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
                    # 중복된 코드 제거하고 범위 -0.5 ~ 0.5 로 완벽 고정
                    fig_lag_gas.update_yaxes(range=[-0.5, 0.5], zeroline=True, zerolinewidth=2, zerolinecolor='black')
                    
                    st.plotly_chart(fig_lag_gas, use_container_width=True)

            with lag_col2:
                with st.container(border=True):
                    # 2. 경유 상관계수 그래프
                    fig_lag_diesel = px.line(df_lag_diesel, x='시차', y='상관계수', color='용도', markers=True,
                                             title='경유 가격 변동의 영향',
                                             labels={'시차': '경과 시간', '상관계수': '상관계수'})
                    
                    fig_lag_diesel.update_layout(paper_bgcolor='#f8fbfe', plot_bgcolor='#f8fbfe')
                    # 동일하게 범위 -0.5 ~ 0.5 로 완벽 고정
                    fig_lag_diesel.update_yaxes(range=[-0.5, 0.5], zeroline=True, zerolinewidth=2, zerolinecolor='black')
                    
                    st.plotly_chart(fig_lag_diesel, use_container_width=True)


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