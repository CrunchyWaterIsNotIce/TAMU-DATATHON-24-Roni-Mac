import streamlit as st
import pandas as pd
import os

def get_data_from_dir(dir_name):
    data_file_names = os.listdir(dir_name)
    data = pd.DataFrame()
    for file_name in data_file_names:
        new_file_data = pd.read_csv(f'{dir_name}/{file_name}')
        data = pd.concat([data, new_file_data], axis=0)
    return data

def filter_by_date_range(data, start, end):
    date_range = pd.date_range(start, end).strftime('%Y-%m-%d')
    return data[pd.to_datetime(data['Sent Date']).dt.strftime('%Y-%m-%d').isin(date_range)]


'''
# Hello! 
## Hey gang32
- Im yapping
- More yapping
- Yap yap yap yap yap
'''

data = get_data_from_dir('data')
st.write(filter_by_date_range(data, '2024-04-25', '2024-05-02'))


# one_month = data[pd.to_datetime(data['Date']).dt.strftime('%m') == data]

col1, col2 = st.columns(2)
col1.write("Im in a coloumn right now")
col2.write('The quick brown fox jumps over the lazy dog')
