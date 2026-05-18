import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

# 페이지 설정
st.set_page_config(page_title="포물선 시뮬레이터 Pro", layout="wide")

st.title("⚾ 실시간 포물선 운동 시뮬레이션")
st.markdown("변수를 설정하고 **'시뮬레이션 시작'** 버튼을 클릭하세요.")

# --- 사이드바: 조작 변수 ---
st.sidebar.header("🛠 환경 설정")
g = st.sidebar.slider("중력 가속도 (m/s²)", 0.0, 20.0, 9.8, 0.1)
m = st.sidebar.slider("물체의 질량 (kg)", 0.1, 10.0, 1.0, 0.1)
h0 = st.sidebar.slider("초기 높이 (m)", 0.0, 50.0, 0.0, 1.0)
v0x = st.sidebar.slider("초기 수평 속도 (vx, m/s)", 0.0, 50.0, 15.0, 1.0)
v0y = st.sidebar.slider("초기 연직 속도 (vy, m/s)", 0.0, 50.0, 20.0, 1.0)

# --- 물리 계산 (사전 계산) ---
if g > 0:
    t_flight = (v0y + np.sqrt(v0y**2 + 2 * g * h0)) / g
else:
    t_flight = 10.0

# 궤적 전체 데이터 미리 계산
t_total = np.linspace(0, t_flight, num=100)
x_total = v0x * t_total
y_total = h0 + v0y * t_total - 0.5 * g * t_total**2

# --- 시뮬레이션 화면 ---
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🎬 애니메이션")
    # 애니메이션을 위한 빈 공간 생성
    plot_spot = st.empty()
    
    start_btn = st.button("🚀 시뮬레이션 시작")

with col2:
    st.subheader("📊 실시간 데이터")
    status_text = st.empty()
    metrics_spot = st.empty()

# --- 시뮬레이션 실행 로직 ---
if start_btn:
    # 애니메이션 프레임 설정
    frames = 50
    t_anim = np.linspace(0, t_flight, num=frames)
    
    for i in range(len(t_anim)):
        curr_t = t_anim[i]
        curr_x = v0x * curr_t
        curr_y = h0 + v0y * curr_t - 0.5 * g * curr_t**2
        
        # 그래프 업데이트
        fig = go.Figure()
        
        # 1. 이동 중인 궤적 (선)
        fig.add_trace(go.Scatter(
            x=v0x * t_anim[:i+1], 
            y=h0 + v0y * t_anim[:i+1] - 0.5 * g * t_anim[:i+1]**2,
            mode='lines', line=dict(color='gray', width=1, dash='dot'),
            showlegend=False
        ))
        
        # 2. 현재 공의 위치 (점)
        fig.add_trace(go.Scatter(
            x=[curr_x], y=[curr_y],
            mode='markers+text',
            marker=dict(color='red', size=15, symbol='circle'),
            name='현재 위치',
            text=["Ball"], textposition="top center"
        ))
        
        # 그래프 축 고정 및 레이아웃
        fig.update_layout(
            xaxis=dict(range=[0, max(x_total)*1.1 if max(x_total)>0 else 10], title="거리 (m)"),
            yaxis=dict(range=[0, max(y_total)*1.1 if max(y_total)>0 else 10], title="높이 (m)"),
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )
        
        # 플레이스홀더에 그래프 그리기
        plot_spot.plotly_chart(fig, use_container_width=True)
        
        # 사이드 정보 업데이트
        metrics_spot.write(f"""
        - **현재 시간:** {curr_t:.2f} s
        - **현재 위치:** ({curr_x:.1f}m, {curr_y:.1f}m)
        - **현재 속도(y):** {v0y - g * curr_t:.1f} m/s
        """)
        
        time.sleep(0.05) # 애니메이션 속도 조절
    
    st.success("운동 종료!")

else:
    # 버튼 누르기 전 초기 화면
    fig_init = go.Figure()
    fig_init.add_trace(go.Scatter(x=[0], y=[h0], mode='markers', marker=dict(size=15, color='red')))
    fig_init.update_layout(
        xaxis=dict(range=[0, max(x_total)*1.1], title="거리 (m)"),
        yaxis=dict(range=[0, max(y_total)*1.1], title="높이 (m)"),
        height=500
    )
    plot_spot.plotly_chart(fig_init, use_container_width=True)

# --- 하단 분석 그래프 (최종 결과 기준) ---
st.divider()
st.subheader("📈 물리 분석 결과")

# 에너지 데이터 계산
vx = np.full_like(t_total, v0x)
vy = v0y - g * t_total
v_total = np.sqrt(vx**2 + vy**2)
ke = 0.5 * m * v_total**2
pe = m * g * y_total
te = ke + pe

tab1, tab2 = st.tabs(["에너지 변화", "속도 변화"])

with tab1:
    fig_e = go.Figure()
    fig_e.add_trace(go.Scatter(x=t_total, y=ke, name='운동 에너지'))
    fig_e.add_trace(go.Scatter(x=t_total, y=pe, name='위치 에너지'))
    fig_e.add_trace(go.Scatter(x=t_total, y=te, name='역학적 에너지 합', line=dict(dash='dash')))
    fig_e.update_layout(xaxis_title="시간 (s)", yaxis_title="에너지 (J)")
    st.plotly_chart(fig_e, use_container_width=True)

with tab2:
    fig_v = go.Figure()
    fig_v.add_trace(go.Scatter(x=t_total, y=vx, name='수평 속도(Vx)'))
    fig_v.add_trace(go.Scatter(x=t_total, y=vy, name='연직 속도(Vy)'))
    fig_v.update_layout(xaxis_title="시간 (s)", yaxis_title="속도 (m/s)")
    st.plotly_chart(fig_v, use_container_width=True)