import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px

from pingouin import ttest
import pingouin as pg

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

def twoMeans(total_df, sgg_nm):
    st.markdown('### 서울시 2월, 3월 아파트 평균 가격 차이 검증')

    total_df['month'] = total_df['DEAL_YMD'].dt.month # 월을 추출해 월 컬럼 생성
    apt_df = total_df[(total_df['HOUSE_TYPE']=='아파트') & (total_df['month'].isin([2, 3]))] 

    feb_df = apt_df[apt_df['month'] == 2]
    mar_df = apt_df[apt_df['month'] == 3]

    st.markdown(f"2월 아파트 평균 가격: { feb_df['OBJ_AMT'].mean().round(0) }만원")
    st.markdown(f"3월 아파트 평균 가격: { mar_df['OBJ_AMT'].mean().round(0) }만원")
    
    result = ttest(feb_df['OBJ_AMT'], mar_df['OBJ_AMT'], paired=False)
    st.dataframe(result, use_container_width=True)

    if result['p-val'].values[0] > 0.05:
        st.markdown('p-val 값이 0.05를 초과로 서울시 2월, 3월 아파트 평균 가격 차이는 없다.')
    else:
        st.markdown('p-val 값이 0.05를 미만으로 서울시 2월, 3월 아파트 평균 가격 차이는 있다.')
############################################################################################
    st.markdown(f'### 서울시 {sgg_nm} 2월, 3월 아파트 평균 가격 차이 검증')

    sgg_df = apt_df[apt_df['SGG_NM']==sgg_nm] # 필터링 (구)
    sgg_feb_df = sgg_df[sgg_df['month'] == 2] # 필터링 (월)
    sgg_mar_df = sgg_df[sgg_df['month'] == 3] # 필터링 (월)

    st.markdown(f"2월 아파트 평균 가격: { sgg_feb_df['OBJ_AMT'].mean().round(0) }만원")
    st.markdown(f"3월 아파트 평균 가격: { sgg_mar_df['OBJ_AMT'].mean().round(0) }만원")

    sgg_result = ttest(sgg_feb_df['OBJ_AMT'], sgg_mar_df['OBJ_AMT'], paired=False)
    st.dataframe(sgg_result, use_container_width=True)

    if sgg_result['p-val'].values[0] > 0.05:
        st.markdown(f'p-val 값이 0.05를 초과로 {sgg_nm} 2월, 3월 아파트 평균 가격 차이는 없다.')
    else:
        st.markdown(f'p-val 값이 0.05를 미만으로 {sgg_nm} 2월, 3월 아파트 평균 가격 차이는 있다.')
###########################################################################################################################
def correlation(total_df, sgg_nm):
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2, 3]))]

    st.markdown('### 상관관계 분석 데이터 확인 \n'
                '- 건물 면적과 거래 금액의 상관 관계 분석\n'
                '- 먼저 추출한 데이터 확인')
    
    corr_df = apt_df[['DEAL_YMD', 'OBJ_AMT', 'BLDG_AREA', 'SGG_NM', 'month']].reset_index(drop=True)
    st.dataframe(corr_df.head())

    st.markdown('### 상관관계 분석 시각화\n'
                '- 상관관계 시각화(산포도)\n')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='BLDG_AREA', y='OBJ_AMT', data=corr_df, ax=ax)
    st.pyplot(fig)
### 상관 계수 확인 ###
    st.markdown('### 서울시 상관관계 게수 및 검정\n'
                '- 상관관계 계수를 확인\n')
    st.dataframe(pg.corr(corr_df['BLDG_AREA'], corr_df['OBJ_AMT']).round(3), use_container_width=False)
    corr_r = pg.corr(corr_df['BLDG_AREA'], corr_df['OBJ_AMT']).round(3)['r']

    st.write(corr_r.item())

    if (corr_r.item() > 0.5):
        st.markdown(f'상관 계수는 {corr_r.item()}이며, 건물 면적이 증가할수록 물건금액도 증가하는 경향성을 가진다.')
    elif (corr_r.item() < -0.5):
        st.markdown(f'상관 계수는 {corr_r.item()}이며, 건물 면적이 증가할수록 물건금액은 감소하는 경향성을 가진다.')
    else:
        st.markdown(f'상관 계수는 {corr_r.item()}이며, 건물 면적과 물건 금액의 관계성은 비교적 작다.')
### 서울시 구별 상관계수 시각화 ###
    st.markdown(f'### 서울시 {sgg_nm} 2월, 3월 아파트 가격 ~ 건물면적 상관관계 분석 \n')
    sgg_df = corr_df[corr_df['SGG_NM'] == sgg_nm]
    corr_coef = pg.corr(sgg_df['BLDG_AREA'], sgg_df['OBJ_AMT'])
    st.dataframe(corr_coef, use_container_width=False)

    # 폰트 설정
    path = 'C:\\windows\Fonts\H2MJRE.TTF'
    fontprop = fm.FontProperties(fname=path, size=12)


    ax.text(0.95, 0.05, f'Pearson Correlation: {corr_coef['r'].values[0]:.2f}',
                                transform=ax.transAxes, ha='right', fontsize=12)
    
    ax.set_title(f'{sgg_nm} 피어슨 상관계수', fontproperties=fontprop)
    st.pyplot(fig)

###########################################################################################################################
def correlation2(total_df, sgg_nm):
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    


def showStat(total_df):
    analysis_nm = st.sidebar.selectbox('분석 메뉴', ['두 집단간 차이 검정', '상관분석', '상관분석(거래 건수)'])
    sgg_nm = st.sidebar.selectbox('자치구명', total_df['SGG_NM'].unique())

    if analysis_nm == '두 집단간 차이 검정':
        twoMeans(total_df, sgg_nm)
    elif analysis_nm == '상관분석':
        correlation(total_df, sgg_nm)
    elif analysis_nm == '상관분석(거래 건수)':
        correlation2(total_df, sgg_nm)
    else:
        st.warning('Error')