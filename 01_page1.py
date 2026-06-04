# app.py
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# 선택: OpenAI 연결 시 사용
# from openai import OpenAI


# =========================================================
# 기본 설정
# =========================================================
PAGE_TITLE = "포물선 운동과 역학적 에너지 보존 AIDT"
VIDEO_URL = "https://www.youtube.com/watch?v=5A6h9F5VPMU"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "aidt_projectile.db"

TIMES = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

st.set_page_config(page_title=PAGE_TITLE, layout="wide")


# =========================================================
# DB 함수
# =========================================================
def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT,
        student_name TEXT,
        class_name TEXT,
        diagnosis_q1 TEXT,
        diagnosis_q2 TEXT,
        diagnosis_q3 TEXT,
        mass REAL,
        gravity REAL,
        data_json TEXT,
        conclusion TEXT,
        error_discussion TEXT,
        ai_feedback TEXT,
        misconception_type TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_record(record):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO student_records (
        created_at,
        student_name,
        class_name,
        diagnosis_q1,
        diagnosis_q2,
        diagnosis_q3,
        mass,
        gravity,
        data_json,
        conclusion,
        error_discussion,
        ai_feedback,
        misconception_type
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["created_at"],
        record["student_name"],
        record["class_name"],
        record["diagnosis_q1"],
        record["diagnosis_q2"],
        record["diagnosis_q3"],
        record["mass"],
        record["gravity"],
        record["data_json"],
        record["conclusion"],
        record["error_discussion"],
        record["ai_feedback"],
        record["misconception_type"],
    ))

    conn.commit()
    conn.close()


def load_records():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM student_records ORDER BY id DESC", conn)
    conn.close()
    return df


# =========================================================
# 유틸 함수
# =========================================================
def parse_float(value, default=0.0):
    try:
        text = str(value).strip()
        if text == "":
            return default
        return float(text)
    except Exception:
        return default


def calc_ke(m, vx, vy):
    return 0.5 * m * (vx**2 + vy**2)


def calc_pe(m, g, y):
    return m * g * y


def draw_chart(title, times, values, ylabel="에너지"):
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(times, values, marker="o")
    ax.set_title(title)
    ax.set_xlabel("시간(s)")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def simple_ai_feedback(conclusion, error_discussion, me_values):
    """
    OpenAI API 없이 작동하는 간단한 규칙 기반 피드백.
    나중에 GPT API로 교체 가능.
    """
    feedback = []
    misconception = "없음 또는 명확하지 않음"

    me_range = max(me_values) - min(me_values)
    me_mean = sum(me_values) / len(me_values) if len(me_values) > 0 else 0
    variation_ratio = me_range / me_mean if me_mean != 0 else 0

    if variation_ratio < 0.1:
        feedback.append("역학적 에너지가 비교적 일정하게 유지된다는 점을 잘 확인했습니다.")
    else:
        feedback.append("역학적 에너지 값의 변화가 비교적 크게 나타났습니다. 측정 오차, 위치 기준 설정, 속도 측정 오차를 함께 검토할 필요가 있습니다.")

    if "보존" in conclusion or "일정" in conclusion:
        feedback.append("결론에서 역학적 에너지 보존 개념을 언급한 점이 적절합니다.")
    else:
        feedback.append("결론에 운동에너지와 위치에너지의 합이 어떻게 변하는지 더 명확히 서술하면 좋습니다.")
        misconception = "역학적 에너지 보존 이해 부족"

    if "오차" in error_discussion or "측정" in error_discussion or "공기" in error_discussion:
        feedback.append("실험 오차 요인을 고려한 점이 좋습니다.")
    else:
        feedback.append("오차 감소 방안에는 공기 저항, 영상 촬영 각도, 좌표축 설정, 시간 간격 측정 문제 등을 포함할 수 있습니다.")

    return "\n".join([f"- {x}" for x in feedback]), misconception


# =========================================================
# 초기화
# =========================================================
init_db()

if "page" not in st.session_state:
    st.session_state.page = "단원 홈"

if "data" not in st.session_state:
    st.session_state.data = {
        "student_name": "",
        "class_name": "",
        "diagnosis_q1": "",
        "diagnosis_q2": "",
        "diagnosis_q3": "",
        "mass": "1.0",
        "gravity": "9.8",
        "x": {t: "" for t in TIMES},
        "y": {t: "" for t in TIMES},
        "vx": {t: "" for t in TIMES},
        "vy": {t: "" for t in TIMES},
        "conclusion": "",
        "error_discussion": "",
        "ai_feedback": "",
        "misconception_type": "",
    }


# =========================================================
# 사이드바
# =========================================================
st.sidebar.title("화면 흐름도")

pages = [
    "단원 홈",
    "도입",
    "사전 진단",
    "개념 학습",
    "시각화·시뮬레이션",
    "형성평가·AI 피드백",
    "교사용 대시보드",
]

st.session_state.page = st.sidebar.radio(
    "학습 단계",
    pages,
    index=pages.index(st.session_state.page)
)

st.sidebar.markdown("---")
st.sidebar.caption("포물선 운동 → 에너지 계산 → 그래프 해석 → AI 피드백 → 교사용 확인")


# =========================================================
# 1. 단원 홈
# =========================================================
if st.session_state.page == "단원 홈":
    st.title(PAGE_TITLE)

    st.markdown("""
    ## 단원: 포물선 운동에서 역학적 에너지 보존

    ### 핵심 질문
    포물선 운동을 하는 물체의 운동에너지, 위치에너지, 역학적 에너지는 시간에 따라 어떻게 변할까?

    ### 학습 목표
    1. 포물선 운동에서 위치와 속도의 변화를 해석할 수 있다.  
    2. 운동에너지와 위치에너지를 계산할 수 있다.  
    3. 그래프를 바탕으로 역학적 에너지 보존 여부를 설명할 수 있다.  
    4. 실험 오차의 원인을 분석하고 개선 방안을 제안할 수 있다.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.info("이 화면은 단순한 LMS가 아니라 AI가 데이터 해석과 피드백에 개입하는 AIDT 구조를 목표로 합니다.")

    with col2:
        st.success("학생 활동 결과는 SQLite DB에 저장되고, 교사용 대시보드에서 확인할 수 있습니다.")


# =========================================================
# 2. 도입
# =========================================================
elif st.session_state.page == "도입":
    st.title("도입: 포물선 운동 관찰하기")

    st.markdown("""
    포물선 운동은 눈으로 관찰할 수 있지만, 그 안에서 변화하는 속도 성분과 에너지 변화는 직접 볼 수 없습니다.  
    이 활동에서는 실제 운동 영상을 바탕으로 위치, 속도, 에너지를 분석합니다.
    """)

    st.video(VIDEO_URL)

    st.markdown("""
    ### 생각해보기
    - 공이 올라갈 때 운동에너지는 어떻게 변할까?
    - 가장 높은 지점에서 운동에너지는 0이 될까?
    - 위치에너지와 운동에너지의 합은 시간에 따라 어떻게 될까?
    """)


# =========================================================
# 3. 사전 진단
# =========================================================
elif st.session_state.page == "사전 진단":
    st.title("사전 진단: 나의 생각 확인하기")

    data = st.session_state.data

    col1, col2 = st.columns(2)

    with col1:
        data["student_name"] = st.text_input(
            "이름",
            value=data["student_name"]
        )

    with col2:
        data["class_name"] = st.text_input(
            "학급 또는 조",
            value=data["class_name"]
        )

    data["diagnosis_q1"] = st.radio(
        "1. 포물선 운동에서 가장 높은 지점에 도달하면 물체의 운동에너지는 0이 된다.",
        ["선택 안 함", "그렇다", "아니다", "잘 모르겠다"],
        index=["선택 안 함", "그렇다", "아니다", "잘 모르겠다"].index(data["diagnosis_q1"]) if data["diagnosis_q1"] else 0
    )

    data["diagnosis_q2"] = st.radio(
        "2. 공기 저항이 없다면 포물선 운동 중 역학적 에너지는 일정하게 보존된다.",
        ["선택 안 함", "그렇다", "아니다", "잘 모르겠다"],
        index=["선택 안 함", "그렇다", "아니다", "잘 모르겠다"].index(data["diagnosis_q2"]) if data["diagnosis_q2"] else 0
    )

    data["diagnosis_q3"] = st.radio(
        "3. 공이 아래로 내려올수록 위치에너지는 감소하고 운동에너지는 증가한다.",
        ["선택 안 함", "그렇다", "아니다", "잘 모르겠다"],
        index=["선택 안 함", "그렇다", "아니다", "잘 모르겠다"].index(data["diagnosis_q3"]) if data["diagnosis_q3"] else 0
    )

    st.info("이 단계는 학생의 선개념과 오개념을 확인하기 위한 화면입니다.")


# =========================================================
# 4. 개념 학습
# =========================================================
elif st.session_state.page == "개념 학습":
    st.title("개념 학습: 에너지 관계 이해하기")

    st.markdown("""
    ## 1. 운동에너지

    물체가 운동하기 때문에 가지는 에너지입니다.

    \\[
    E_k = \\frac{1}{2}m(v_x^2 + v_y^2)
    \\]

    ## 2. 위치에너지

    물체가 기준점보다 높은 위치에 있기 때문에 가지는 에너지입니다.

    \\[
    E_p = mgy
    \\]

    ## 3. 역학적 에너지

    운동에너지와 위치에너지의 합입니다.

    \\[
    E = E_k + E_p
    \\]

    공기 저항과 마찰이 없다면 포물선 운동 중 역학적 에너지는 일정하게 보존됩니다.
    """)

    st.warning("중요: 가장 높은 지점에서도 수평방향 속도가 남아 있으므로 운동에너지가 반드시 0이 되는 것은 아닙니다.")


# =========================================================
# 5. 시각화·시뮬레이션
# =========================================================
elif st.session_state.page == "시각화·시뮬레이션":
    st.title("시각화·시뮬레이션: 데이터 입력과 에너지 그래프")

    data = st.session_state.data

    col1, col2 = st.columns(2)

    with col1:
        data["mass"] = st.text_input("질량 m (kg)", value=data["mass"])

    with col2:
        data["gravity"] = st.text_input("중력가속도 g (m/s²)", value=data["gravity"])

    m = parse_float(data["mass"], 1.0)
    g = parse_float(data["gravity"], 9.8)

    st.markdown("### 운동 기록표")

    input_rows = []

    for t in TIMES:
        cols = st.columns(5)
        with cols[0]:
            st.markdown(f"**{t:.1f} s**")
        with cols[1]:
            data["x"][t] = st.text_input(f"x_{t}", value=data["x"][t], placeholder="x", label_visibility="collapsed")
        with cols[2]:
            data["y"][t] = st.text_input(f"y_{t}", value=data["y"][t], placeholder="y", label_visibility="collapsed")
        with cols[3]:
            data["vx"][t] = st.text_input(f"vx_{t}", value=data["vx"][t], placeholder="vx", label_visibility="collapsed")
        with cols[4]:
            data["vy"][t] = st.text_input(f"vy_{t}", value=data["vy"][t], placeholder="vy", label_visibility="collapsed")

    rows = []
    ke_values = []
    pe_values = []
    me_values = []

    for t in TIMES:
        x = parse_float(data["x"][t])
        y = parse_float(data["y"][t])
        vx = parse_float(data["vx"][t])
        vy = parse_float(data["vy"][t])

        ke = calc_ke(m, vx, vy)
        pe = calc_pe(m, g, y)
        me = ke + pe

        ke_values.append(ke)
        pe_values.append(pe)
        me_values.append(me)

        rows.append({
            "시간(s)": t,
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "운동에너지": round(ke, 3),
            "위치에너지": round(pe, 3),
            "역학적 에너지": round(me, 3),
        })

    df_energy = pd.DataFrame(rows)

    st.markdown("### 에너지 계산 결과")
    st.dataframe(df_energy, use_container_width=True)

    st.markdown("### 에너지 그래프")

    graph_col1, graph_col2, graph_col3 = st.columns(3)

    with graph_col1:
        draw_chart("운동에너지 변화", TIMES, ke_values)

    with graph_col2:
        draw_chart("위치에너지 변화", TIMES, pe_values)

    with graph_col3:
        draw_chart("역학적 에너지 변화", TIMES, me_values)

    st.info("이 화면은 비가시적인 에너지 변화를 그래프와 수치로 가시화하는 핵심 화면입니다.")


# =========================================================
# 6. 형성평가·AI 피드백
# =========================================================
elif st.session_state.page == "형성평가·AI 피드백":
    st.title("형성평가·AI 피드백")

    data = st.session_state.data

    st.markdown("""
    ### 형성평가 1
    시간에 따른 운동에너지, 위치에너지, 역학적 에너지 그래프를 바탕으로 포물선 운동에서 역학적 에너지가 어떻게 변하는지 설명하세요.
    """)

    data["conclusion"] = st.text_area(
        "결론 도출",
        value=data["conclusion"],
        height=180,
        placeholder="예: 운동에너지는 감소하다가 다시 증가하고, 위치에너지는 증가하다가 감소한다. 두 에너지의 합인 역학적 에너지는..."
    )

    st.markdown("""
    ### 형성평가 2
    실험 결과에서 역학적 에너지가 완전히 일정하지 않게 나타났다면 그 이유는 무엇일지 설명하세요.
    """)

    data["error_discussion"] = st.text_area(
        "오차 원인 및 개선 방안",
        value=data["error_discussion"],
        height=180,
        placeholder="예: 공기 저항, 영상 촬영 각도, 위치 측정 오차, 속도 계산 오차 등이 영향을 줄 수 있다..."
    )

    m = parse_float(data["mass"], 1.0)
    g = parse_float(data["gravity"], 9.8)

    rows = []
    me_values = []

    for t in TIMES:
        x = parse_float(data["x"][t])
        y = parse_float(data["y"][t])
        vx = parse_float(data["vx"][t])
        vy = parse_float(data["vy"][t])

        ke = calc_ke(m, vx, vy)
        pe = calc_pe(m, g, y)
        me = ke + pe
        me_values.append(me)

        rows.append({
            "time": t,
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "ke": ke,
            "pe": pe,
            "me": me,
        })

    data_json = pd.DataFrame(rows).to_json(force_ascii=False)

    if st.button("AI 피드백 받기 및 저장", use_container_width=True):
        feedback, misconception = simple_ai_feedback(
            data["conclusion"],
            data["error_discussion"],
            me_values
        )

        data["ai_feedback"] = feedback
        data["misconception_type"] = misconception

        record = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "student_name": data["student_name"],
            "class_name": data["class_name"],
            "diagnosis_q1": data["diagnosis_q1"],
            "diagnosis_q2": data["diagnosis_q2"],
            "diagnosis_q3": data["diagnosis_q3"],
            "mass": m,
            "gravity": g,
            "data_json": data_json,
            "conclusion": data["conclusion"],
            "error_discussion": data["error_discussion"],
            "ai_feedback": feedback,
            "misconception_type": misconception,
        }

        save_record(record)

        st.success("AI 피드백과 학생 기록이 저장되었습니다.")

    if data["ai_feedback"]:
        st.markdown("### AI 피드백")
        st.info(data["ai_feedback"])

        st.markdown("### 진단된 오개념 유형")
        st.warning(data["misconception_type"])


# =========================================================
# 7. 교사용 대시보드
# =========================================================
elif st.session_state.page == "교사용 대시보드":
    st.title("교사용 대시보드")

    df = load_records()

    if df.empty:
        st.warning("아직 저장된 학생 기록이 없습니다.")
    else:
        st.markdown("### 전체 학생 기록")
        st.dataframe(df, use_container_width=True)

        st.markdown("### 오개념 유형 분포")

        misconception_count = df["misconception_type"].value_counts().reset_index()
        misconception_count.columns = ["오개념 유형", "학생 수"]

        st.dataframe(misconception_count, use_container_width=True)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(misconception_count["오개념 유형"], misconception_count["학생 수"])
        ax.set_xlabel("오개념 유형")
        ax.set_ylabel("학생 수")
        ax.set_title("오개념 유형별 학생 수")
        plt.xticks(rotation=20)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("### 학생별 AI 피드백 확인")

        selected_id = st.selectbox(
            "학생 기록 선택",
            df["id"].tolist()
        )

        selected = df[df["id"] == selected_id].iloc[0]

        st.write("이름:", selected["student_name"])
        st.write("학급/조:", selected["class_name"])
        st.write("저장 시각:", selected["created_at"])

        st.markdown("#### 결론 도출")
        st.write(selected["conclusion"])

        st.markdown("#### 오차 원인 및 개선 방안")
        st.write(selected["error_discussion"])

        st.markdown("#### AI 피드백")
        st.info(selected["ai_feedback"])

        st.markdown("#### 진단된 오개념")
        st.warning(selected["misconception_type"])
