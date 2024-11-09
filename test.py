import streamlit as st
import pandas as pd

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})
'''
# Hello! 
## Hey gang32
- Im yapping
- More yapping
- Yap yap yap yap yap
'''

col1, col2 = st.columns(2)
col1.write("Im in a coloumn right now")
col2.write('The quick brown fox jumps over the lazy dog')



col1.line_chart(df)