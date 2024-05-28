#
# eda.py (eda1.py)
#

import streamlit as st
from viz import showViz
import pandas as pd
from streamlit_option_menu import option_menu
from statistic import showStat
from map import showMap

def run_eda_home(total_df):
    st.markdown("### 탐색적 자료 분석 개요 \n"
                "탐색적 자료 분석 페이지 입니다."
                "여기에 포함하고 싶은 내용을 넣을 수 있습니다.")
    selected = option_menu(None, ['Home', 'Visualization', 'Statistics', 'Map'],
                           icons=['house', 'bar-chart', 'file-spreadsheet', 'map'],
                           menu_icon = 'cast', default_index=0, orientation='horizontal',
                           styles={
                               'container' : {
                                'padding' : '0!important',
                                'background-color' : '#808080'},
                                'icon' : {
                                'color' : 'orange',
                                'font-size' : '25px'},
                                'nav-link' : {
                                'font-size' : '15px',
                                'text-align' : 'left',
                                'margin' : '0px',
                                '--hover-color' : '#eee'},
                                'nav-link-selected' : {
                                'background-color' : 'green'}
                                })
    if selected == 'Home':
        st.markdown("### Visualization 개요\n"
                    "- 가구당 평균 가격 추이\n"
                    "- 가구당 거래 건수 추이\n"
                    "- 지역별 평균 가격 막대 그래프\n"
                    "### Statistics 개요\n"
                    "### Map 개요\n"
                    
                    )
    elif selected == 'Visualization':
        showViz(total_df)
    elif selected == 'Statistics':
        showStat(total_df)
    elif selected == 'Map':
        showMap(total_df)
    else:
        st.warning('Wrong')