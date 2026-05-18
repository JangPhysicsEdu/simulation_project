import streamlit as st

c1, c2, c3, c4 = st.columns((1,1,1,1))
with c1:
    if st.button("역학적 에너지 보존", use_container_width=True):
        st.switch_page("pages/01_page1.py")
with c2:
    if st.button("등가속도 운동", use_container_width=True):
        st.switch_page("pages/02_page2.py")
with c3:
    if st.button("스넬의 법칙과 전반사", use_container_width=True):
        st.switch_page("pages/03_page3.py")
with c4:
    if st.button("뉴턴의 결정적 실험", use_container_width=True):
        st.switch_page("pages/04_page4.py")

c5, c6, c7, c8 = st.columns((1,1,1,1))
with c5:
    if st.button("exp1", use_container_width=True):
        st.switch_page("pages/01_page1.py")
with c6:
    if st.button("exp2", use_container_width=True):
        st.switch_page("pages/02_page2.py")
with c7:
    if st.button("exp3", use_container_width=True):
        st.switch_page("pages/03_page3.py")
with c8:
    if st.button("exp4", use_container_width=True):
        st.switch_page("pages/04_page4.py")