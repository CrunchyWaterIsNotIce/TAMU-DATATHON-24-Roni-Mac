import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from collections import Counter


# Combines every csv file in a directory into a single DataFrame
def get_data_from_dir(dir_name):
    data_file_names = os.listdir(dir_name)
    data = pd.DataFrame()
    for file_name in data_file_names:
        new_file_data = pd.read_csv(f'{dir_name}/{file_name}')
        data = pd.concat([data, new_file_data], axis=0)
    return data

# Filters a DataFrame by a range of dates
def filter_by_date_range(data, start = '2024-01-1', end = '2024-01-1'):
    date_range = pd.date_range(start, end).strftime('%Y-%m-%d')
    return data[pd.to_datetime(data['Sent Date']).dt.strftime('%Y-%m-%d').isin(date_range)]




# All data from all CSV files
data = get_data_from_dir('data')
data['Parent Menu Selection'] = data['Parent Menu Selection'].replace('Mac and Cheese Party Tray (Plus FREE Garlic Bread)', 'Party Tray')


st.title("Roni's Mac Bar")



date_range = st.date_input('Enter Date Range:', (pd.to_datetime('2024-04-1'), pd.to_datetime('2024-11-09')))
if len(date_range) == 2:
    start, end = date_range
    filtered_data = filter_by_date_range(data, start, end)
else:
    filtered_data = data


col1, col2 = st.columns(2)
field = col1.selectbox('Select a field', ('Modifier', 'Option Group Name', 'Parent Menu Selection'))
if len(filtered_data) != 0:
    counts = pd.DataFrame.from_dict(Counter(filtered_data[field].dropna()), orient='index').nlargest(10, 0) 
    keys = list(counts[0].keys())
    vals = list(counts[0])
    fig, ax = plt.subplots()
    ax.bar(keys, vals)
    ax.tick_params(axis='x', rotation=90)
    col1.pyplot(fig)

# one_month = data[pd.to_datetime(data['Date']).dt.strftime('%m') == data]

