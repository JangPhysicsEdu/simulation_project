import streamlit as st
st.subheader('첫번째 콘텐츠')

import pandas as pd
df = pd.read_csv('./data.csv', encoding='cp949')
st.write(df)
st.bar_chart(df.groupby(by='행정구역').sum())
