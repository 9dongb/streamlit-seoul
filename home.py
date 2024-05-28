#
# home.py
#

import pandas as pd
import streamlit as st
from millify import prettify # 천 단위 콤마(, ) 적용할 수 이쓴 prettify 함수

def run_home(total_df):
    st.markdown("## 대시보드 개요 \n"
                "본 프로젝트는 서울시 부동산 실거래가를 알려주는 대시보드 입니다."
                "여기서 추가하고 싶은 내용을 추가됩니다.")

    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format="%Y-%m-%d")
    total_df['month'] = total_df['DEAL_YMD'].dt.month # 월을 추출해 월 컬럼 생성
    total_df['year'] = total_df['DEAL_YMD'].dt.year # 연도를 추출해 연도 컬럼 생성
    total_df = total_df.loc[total_df['HOUSE_TYPE'] == '아파트', :]

    sgg_nm = st.sidebar.selectbox("자치구", sorted(total_df['SGG_NM'].dropna().unique()))

    acc_year = st.sidebar.selectbox("년도", [2024])

    month_dic = {'1월':1, '2월' : 2, '3월' : 3, '4월' : 4, '5월' : 5, '6월' : 6,
    '7월' : 7, '8월' : 8, '9월' : 9, '10월' : 10, '11월' : 11, '12월' : 12}

    selected_month = st.sidebar.radio("확인하고 싶은 월을 선택하시오.", list(month_dic.keys()))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f'{sgg_nm} {acc_year}년 {selected_month} 아파트 가격 개요')
    st.markdown('자치구와 월을 클릭하면 자동으로 각 지역구에서 거래된 **최소가격**, **최대가격**을 확인할 수 있습니다.')

    # 컬럼을 두개 생성
    col1 ,col2, col3 = st.columns(3)

    filtered_month = total_df[total_df['month'] == month_dic[selected_month]]
    filtered_month = filtered_month[filtered_month['year'] == acc_year]
    filtered_month = filtered_month[filtered_month['SGG_NM'] == sgg_nm]

    march_min_price = filtered_month['OBJ_AMT'].min()
    march_max_price = filtered_month['OBJ_AMT'].max()
    march_volume = len(filtered_month)

    with col1:
        st.metric(label=f'{sgg_nm} 최소가격(만원)', value=prettify(march_min_price))
    with col2:
        st.metric(label=f'{sgg_nm} 최대가격(만원)', value=prettify(march_max_price))
    with col3:
        st.metric(label=f'{sgg_nm} 거래량', value=prettify(march_volume))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("아파트 가격 상위 3위")
    top3 = filtered_month.sort_values('OBJ_AMT', ascending=False).head(3)[['SGG_NM', 'BJDONG_NM', 'BLDG_NM', 'BLDG_AREA', 'OBJ_AMT']].reset_index(drop=True)
    st.dataframe(top3)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("아파트 가격 하위 3위")
    top3 = filtered_month.sort_values('OBJ_AMT').head(3)[['SGG_NM', 'BJDONG_NM', 'BLDG_NM', 'BLDG_AREA', 'OBJ_AMT']].reset_index(drop=True)
    st.dataframe(top3)

    