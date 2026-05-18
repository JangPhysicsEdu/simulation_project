import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (환경에 따라 다를 수 있음)
plt.rc('font', family='NanumGothic') 

# 1. 데이터 생성 함수
@st.cache_data
def generate_data():
    surnames = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임"]
    first_names = ["민준", "서연", "도윤", "서윤", "하준", "지우", "은우", "하은", "준우", "지유"]
    
    data = []
    for _ in range(100):
        name = random.choice(surnames) + random.choice(first_names)
        kor, eng, math, sci = [random.randint(40, 100) for _ in range(4)]
        total = kor + eng + math + sci
        avg = total / 4
        
        if avg >= 90: grade = 'A'
        elif avg >= 80: grade = 'B'
        elif avg >= 70: grade = 'C'
        elif avg >= 60: grade = 'D'
        else: grade = 'E'
        
        data.append([name, kor, eng, math, sci, total, avg, grade])
    
    return pd.DataFrame(data, columns=['이름', '국어', '영어', '수학', '과학', '총점', '평균', '등급'])

# 데이터 로드
df = generate_data()

# 2. 사이드바 메뉴 구성
st.sidebar.title("📌 성적 관리 시스템")
menu = st.sidebar.radio("메뉴 선택", ["HOME", "성적테이블조회", "성적시각화"])

# 3. 메뉴별 화면 구성
if menu == "HOME":
    st.title("🎓 성적 처리 웹앱")
    st.subheader("시스템 개요")
    st.write("이 앱은 Streamlit을 이용해 100명의 가상 성적 데이터를 관리하고 시각화합니다.")
    
    # CSV 다운로드 버튼
    st.info("아래 버튼을 클릭하여 생성된 `score.csv` 파일을 다운로드할 수 있습니다.")
    csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button(
        label="📥 score.csv 다운로드",
        data=csv,
        file_name='score.csv',
        mime='text/csv',
    )
    
    st.image("https://unsplash.com")

elif menu == "성적테이블조회":
    st.title("🔍 성적 테이블 조회")
    
    # 검색 기능
    search_name = st.text_input("학생 이름 검색")
    if search_name:
        display_df = df[df['이름'].str.contains(search_name)]
    else:
        display_df = df
        
    st.dataframe(display_df, use_container_width=True)
    st.write(f"총 인원: {len(display_df)}명")

elif menu == "성적시각화":
    st.title("📊 성적 데이터 시각화")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("과목별 평균 점수")
        subject_avg = df[['국어', '영어', '수학', '과학']].mean()
        st.bar_chart(subject_avg)
        
    with col2:
        st.subheader("등급 분포 (Pie Chart)")
        grade_counts = df['등급'].value_counts().sort_index()
        fig, ax = plt.subplots()
        ax.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        ax.axis('equal')
        st.pyplot(fig)

    st.subheader("평균 점수 분포 (Histogram)")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.histplot(df['평균'], bins=10, kde=True, ax=ax2, color='skyblue')
    st.pyplot(fig2)
