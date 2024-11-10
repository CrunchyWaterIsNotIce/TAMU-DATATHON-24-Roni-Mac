import streamlit as st
import pandas as pd
import numpy as np
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

def make_bar_graph(data, field):
    data = data.copy(deep=False).drop_duplicates(subset=[field, 'Order ID', 'Sent Date'])
    counts = pd.DataFrame.from_dict(Counter(data[field].dropna()), orient='index').nlargest(10, 0) 
    keys = list(counts[0].keys())[::-1]
    vals = list(counts[0])[::-1]
    fig, ax = plt.subplots()
    ax.set_xlabel('Number of Purchases with Option')
    ax.barh(keys, vals)
    return fig

def order_by_time(data):
    data = data.copy(deep=False).drop_duplicates(subset=['Sent Date', 'Order ID'])
    data['time'] = pd.to_datetime(data['Sent Date']).dt.strftime('%H').astype(float)
    data = data.sort_values(by = ['time'])
    counts = pd.DataFrame.from_dict(Counter(data['time'].dropna()), orient='index')
    fig, ax = plt.subplots()
    ax.set_xlim(6,22)
    ax.set_xticks(range(6,23, 2))
    ax.set_xticklabels(('6 AM','8 AM', '10 AM', '12 PM', '2 PM', '4 PM', '6 PM','8 PM', '10 PM'))
    ax.set_xlabel('Time')
    ax.set_ylabel('Orders')
    ax.plot(counts)
    return fig

def graph_monthly_sales(data):
    data = data.copy(deep=False).drop_duplicates(subset=['Sent Date', 'Order ID'])
    data['month'] = pd.to_datetime(data['Sent Date']).dt.strftime('%b')

    counts = pd.DataFrame.from_dict(Counter(data['month'].dropna()), orient='index')
    fig, ax = plt.subplots() 
    ax.set_ylim(0,5000)
    ax.set_xlabel('Month')
    ax.set_ylabel('Orders')
    ax.plot(counts)
    return fig

def graph_daily_sales(data):
    data = data.copy(deep=False).drop_duplicates(subset=['Sent Date', 'Order ID'])
    data['day'] = pd.to_datetime(data['Sent Date']).dt.strftime('%m').astype(float) * 31 + pd.to_datetime(data['Sent Date']).dt.strftime('%d').astype(float)
    data = data.sort_values(by = ['day'])
    counts = pd.DataFrame.from_dict(Counter(data['day'].dropna()), orient='index')
    # counts
    fig, ax = plt.subplots() 
    # data['day'][0]
    # st.write(max(data['day'])-min(data['day']))
    # dates = data[data['day'].isin(range(int(min(data['day'])), int(max(data['day'])), int((max(data['day'])-min(data['day']))//2)))].drop_duplicates(subset=['day'])
    # st.write()    
    # ax.set_xticklabels(pd.to_datetime(dates['Sent Date']).dt.strftime('%b %d'))
    ax.set_xticklabels('')
    
    
    # ax.set_xlabel('Month')
    ax.set_ylabel('Orders')
    ax.plot(counts)
    return fig


## look at filter data

# All data from all CSV files
data = get_data_from_dir('data')
data['Parent Menu Selection'] = data['Parent Menu Selection'].replace('Mac and Cheese Party Tray (Plus FREE Garlic Bread)', 'Party Tray')
data['Option Group Name'] = data['Option Group Name'].replace('Do you want Mac and Cheese added inside?', 'Mac and Cheese inside?')

# Total sales over time
orderID_sentData = data[["Order #", "Sent Date"]]



st.title("Roni's Mac Bar")



date_range = st.date_input('Enter Date Range:', (pd.to_datetime('2024-04-1'), pd.to_datetime('2024-11-09')))
if len(date_range) == 2:
    start, end = date_range
    filtered_data = filter_by_date_range(data, start, end)
else:
    filtered_data = data


col1, col2 = st.columns(2)
col1.subheader('Most Popular Options')
col2.subheader('Sales throughout the day')
graph_container = col1.container()


cont = st.container()
col3, col4 = cont.columns(2)
col3.subheader('Monthly Sales')
col4.subheader('Daily Sales over time')

filed_selected = col1.selectbox('Select a field', ('Item Type', 'Modifier'))
fields = {'Item Type':'Parent Menu Selection', 'Modifier':'Modifier', 'Options':'Option Group Name'}
field = fields[filed_selected]

if len(filtered_data) != 0:
    fig1  = make_bar_graph(filtered_data, field)
    graph_container.pyplot(fig1)
    fig2 = order_by_time(filtered_data)
    col2.pyplot(fig2)
    fig3 = graph_monthly_sales(data)
    col3.pyplot(fig3)
    fig4 = graph_daily_sales(filtered_data)
    col4.pyplot(fig4)



    




# one_month = data[pd.to_datetime(data['Date']).dt.strftime('%m') == data]

