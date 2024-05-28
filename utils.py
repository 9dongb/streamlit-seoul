#
# utils.py
#
import pandas as pd

def load_data():

    # csv 파일을 읽어와 데이터프레임으로 만드는 파이썬 프로그램 작성 
    data = pd.read_csv('data/seoul_real_estate_10000.csv', parse_dates=['DEAL_YMD'])
    return data