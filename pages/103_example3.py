import streamlit as st
import pandas as pd

st.subheader('세번째 콘텐츠')

#로그인 시스템을 만들 수 있는 코드 또는 DB 상에 자료를 모을 수 있음
#w를 하면 매번 새로 쓰는데 a로하면 밑에다가 추가로 더 붙여넣음 (open 함수 이야기)
#실험데이터를 기록시키는 것도 좋은 방법이 될 것 같음
#성적처리기와 같이 데이터를 넣었다 뺐다할 수 있는 것을 만들어보기


name = st.text_input('Name:')
age = st.number_input('Age:', min_value=1, max_value=100, step=1)
email = st.text_input('Email:')

if st.button('방명록에 추가하기'):

    if all ([name, age, email]):
        input_data=f'{name},{age},{email}\n'
        with open('./guestbook.csv', 'a') as f:
            f.write(input_data)
            f.close()
    else:
            st.error('모든 값은 필수입니다.')

    st.success('추가되었습니다.')

df_guest = pd.read_csv('./guestbook.csv', encoding='cp949')
st.write(df_guest)