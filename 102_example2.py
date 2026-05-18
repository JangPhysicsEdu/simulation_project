import streamlit as st
import pandas as pd
st.subheader('두번째 콘텐츠')
df_score = pd.read_csv('./score.csv')
st.write(df_score)

df_score['총점'] = 0
st.bar_chart(df_score.groupby(by='이름').sum())

for i in range(5):
    j=0
    df_score.iloc[i, -1] = df_score.iloc[i, j+1]+df_score.iloc[i, j+2]+df_score.iloc[i, j+3]

st.table(df_score)