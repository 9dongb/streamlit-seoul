#
# viz.py
#

import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px

def showViz(total_df):
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format='%Y-%m-%d')

    sgg_nm = st.sidebar.selectbox('자치구명', sorted(total_df['SGG_NM'].dropna().unique()))
    selected = st.sidebar.radio('차트메뉴', ['가구당 평균 가격 추세', '가구당 거래 건수', '지역별 평균 가격 막대 그래프'])

    if selected == '가구당 평균 가격 추세':
        meanChart(total_df, sgg_nm)
    elif selected =='가구당 거래 건수':
        pass
        lenChart(total_df, sgg_nm)
    elif selected == '지역별 평균 가격 막대 그래프':
        localMeanchart(total_df)
    else:
        st.warning("Error")

def meanChart(total_df, sgg_nm):
    st.markdown("## 가구별 평균 가격 추세 \n")

    filtered_df = total_df[total_df['SGG_NM'] == sgg_nm] # 
    filtered_df = filtered_df[filtered_df['DEAL_YMD'].between('2024-01-01', '2024-02-28')] # 두 기간 사이의 데이터만 추출
    result = filtered_df.groupby(['DEAL_YMD', 'HOUSE_TYPE'])['OBJ_AMT'].agg('mean').reset_index()

    df1 = result[result['HOUSE_TYPE'] == '아파트']
    df2 = result[result['HOUSE_TYPE'] == '단독다가구']
    df3 = result[result['HOUSE_TYPE'] == '오피스텔']
    df4 = result[result['HOUSE_TYPE'] == '연립다세대']

    fig = make_subplots(rows=2, cols=2,
                        shared_xaxes=True,
                        subplot_titles=('아파트', '단독다가구', '오피스텔', '연립다세대'),
                        horizontal_spacing=0.15)
    
    fig.add_trace(px.line(df1, x='DEAL_YMD', y='OBJ_AMT',
                          title='아파트 실거래가 평균', 
                          markers=True).data[0], 
                          row=1, col=1)
    fig.add_trace(px.line(df2, x='DEAL_YMD', y='OBJ_AMT',
                          title='단독다가구 실거래가 평균', 
                          markers=True).data[0], 
                          row=1, col=2)
    fig.add_trace(px.line(df3, x='DEAL_YMD', y='OBJ_AMT',
                          title='오피스텔 실거래가 평균', 
                          markers=True).data[0], 
                          row=2, col=1)
    fig.add_trace(px.line(df4, x='DEAL_YMD', y='OBJ_AMT',
                          title='오피스텔 실거래가 평균', 
                          markers=True).data[0], 
                          row=2, col=2)
    
    fig.update_yaxes(tickformat='.0f',
                     title_text='물건가격(원)',
                     range=[result['OBJ_AMT'].min(), result['OBJ_AMT'].max()])
    
    fig.update_layout(
        title='가구별 평균값 추세 그래프',
        width=800, height=600,
        showlegend=True, template='plotly_white')
    st.plotly_chart(fig)

def lenChart(total_df, sgg_nm):
    st.markdown('### 가구당 거래 건수\n')

    filtered_df = total_df[total_df['SGG_NM'] == sgg_nm]
    filtered_df = filtered_df[filtered_df['DEAL_YMD'].between('2024-01-01', '2024-03-11')] # 두 기간 사이의 데이터만 추출
    filtered_df['month'] = filtered_df['DEAL_YMD'].dt.month # 월을 추출하여 열 생성

    f_df1 = filtered_df[filtered_df['HOUSE_TYPE'] == '아파트']
    f_df1 = f_df1.groupby('month').size().reset_index(name='count') # 월 별 거래 건수 계산하고 count 열 추가

    f_df2 = filtered_df[filtered_df['HOUSE_TYPE'] == '단독다가구']
    f_df2 = f_df2.groupby('month').size().reset_index(name='count') # 월 별 거래 건수 계산하고 count 열 추가

    f_df3 = filtered_df[filtered_df['HOUSE_TYPE'] == '오피스텔']
    f_df3 = f_df3.groupby('month').size().reset_index(name='count') # 월 별 거래 건수 계산하고 count 열 추가

    f_df4 = filtered_df[filtered_df['HOUSE_TYPE'] == '연립다세대']
    f_df4 = f_df4.groupby('month').size().reset_index(name='count') # 월 별 거래 건수 계산하고 count 열 추가

    fig = make_subplots(rows=2, cols=2,
                        shared_xaxes=True,
                        subplot_titles=('아파트', '단독다가구', '오피스텔', '연립다세대'),
                        horizontal_spacing=0.15)

    fig.add_trace(px.bar(f_df1, x='month', y='count',
                        title='아파트 월별 거래 건수').data[0], 
                        row=1, col=1)
    fig.add_trace(px.bar(f_df2, x='month', y='count',
                        title='단독다가구 월별 거래 건수').data[0], 
                        row=1, col=2)
    fig.add_trace(px.bar(f_df3, x='month', y='count',
                        title='오피스텔 월별 거래 건수').data[0], 
                        row=2, col=1)
    fig.add_trace(px.bar(f_df4, x='month', y='count',
                        title='연립다세대 월별 거래 건수').data[0], 
                        row=2, col=2)
    
    realmax = max([max(f_df1['count']), max(f_df2['count']), max(f_df3['count']), max(f_df4['count'])]) # 네 가구 중 최대 거래 건수 찾기
    fig.update_yaxes(title_text='거래 건 수 (개)',
                    range=[0, realmax])

    st.plotly_chart(fig)
def localMeanchart(total_df):
    st.markdown('### 지역별 평균 가격 막대 그래프')

    total_df['YEAR_MONTH'] = total_df['DEAL_YMD'].dt.year.astype(str) + '-'+ total_df['DEAL_YMD'].dt.month.astype(str)
    yearMonth = sorted(total_df['YEAR_MONTH'].unique())
    houseType = sorted(total_df['HOUSE_TYPE'].unique())
    selectYearMonth = st.selectbox('월을 선택하세요.', yearMonth)
    selectHouseType = st.selectbox('가구 유형을 선택하세요.', houseType)
    
    result = total_df.query(f"YEAR_MONTH == '{selectYearMonth}' and HOUSE_TYPE == '{selectHouseType}'")
    result_mean = result.groupby('SGG_NM')['OBJ_AMT'].agg('mean').reset_index()

    fig = px.bar(result_mean, x='SGG_NM', y='OBJ_AMT', title='지역별 평균 가격')
    fig.update_layout(xaxis_title="지역구명", yaxis_title="평균 가격(만원)")
    st.plotly_chart(fig)

    st.markdown('---')

    result_count = result.groupby('SGG_NM').size().reset_index(name='count')
    fig = px.bar(result_count, x='SGG_NM', y='count', title='지역별 거래 건수 막대 그래프')
    fig.update_layout(xaxis_title="지역구명", yaxis_title="거래건수")
    st.plotly_chart(fig)
