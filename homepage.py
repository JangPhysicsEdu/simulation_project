import streamlit as st

txt_title = """
물리학 지능형과학실
"""

txt_information = """
개념을 배우는 것을 넘어서,
직접 실험하고, 데이터로 해석하고, 수식으로 설명하세요.
"""

txt_todayexp = """
포물선 운동에서 에너지는 보존되는가?
"""

st.set_page_config(page_title=txt_title, layout="wide")
st.title(txt_title)

st.markdown(txt_information)

if st.button("탐구 시작하기"):
    st.switch_page("pages/Simulation.py")

st.subheader("오늘의 탐구")
st.write(txt_todayexp)

st.subheader("바로가기")
c1, c2, c3 = st.columns(3)

with c1:
    st.button("교과서 바로가기", use_container_width=True)
with c2:
    st.button("탐구 Q&A", use_container_width=True)
with c3:
    st.button("학습 상황 확인하기", use_container_width=True)