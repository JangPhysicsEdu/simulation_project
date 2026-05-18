import csv
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
import pandas as pd
import streamlit as st

# =========================================================
# 기본 설정
# =========================================================
PAGE_TITLE = "역학과 에너지 탐구 LMS"
VIDEO_URL = "https://www.youtube.com/watch?v=5A6h9F5VPMU"
REFERENCE_URL = "https://viewer.vivasam.com/qrviewer/viewer.html?qrcode=106491_20p_6_ST"

TIMES = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
STATE_KEY = "projectile_energy_state"

BASE_DIR = Path(__file__).resolve().parent.parent
SAVE_FILE = BASE_DIR / "page1_response.csv"

st.set_page_config(page_title=PAGE_TITLE, layout="wide")

# =========================================================
# 안내 문구
# =========================================================
TXT_INTRO = """
## 포물선 운동에서 역학적 에너지 보존
> 포물선 운동을 하는 물체는 위치와 속도가 계속 달라진다. 이때 운동에너지와 위치에너지의 합인 역학적 에너지는 어떻게 되는지 다음 탐구로 알아보자.
"""

TXT_ACTIVITY = """
### 포물선 운동 동영상을 분석하여 역학적 에너지 보존 확인하기
#### 목표
> 포물선 운동을 하는 물체의 운동 에너지와 위치 에너지는 계속 변한다. 이때 역학적 에너지는 어떻게 될까?

#### 문제 인식
> 포물선 운동을 하는 물체의 운동 에너지와 위치 에너지는 계속 변한다. 이때 역학적 에너지는 어떻게 될까?

#### 준비물
> 공, 모눈종이, 스마트 기기, 동영상 분석 앱

#### 탐구 수행
> 1. 스마트 기기를 삼각대에 고정하여 동영상 촬영을 준비한다.  
> 2. 모눈종이 앞에서 질량을 알고 있는 공을 비스듬히 던져 포물선 운동 동영상을 촬영한다.

#### 결과 및 정리
> 1. 촬영한 동영상을 운동 분석 앱을 이용하여 0.1초 간격으로 위치(x, y)와 속력(vx, vy)를 기록한다.  
> 2. 운동 에너지, 위치에너지, 역학적 에너지를 계산한다.
"""

TXT_GRAPH_GUIDE = """
> 3. 시간에 따른 운동 에너지, 위치 에너지, 역학적 에너지를 각각 그래프로 나타낸다.
"""

TXT_CONCLUSION = """
#### 결론 도출
> 포물선 운동을 하는 물체의 역학적 에너지는 시간에 따라 어떠한지 설명해보자.
"""

TXT_COMMUNICATION = """
#### 소통하기
> 실험 오차를 줄이기 위한 방법을 토의해보자.
"""

# =========================================================
# 스타일
# =========================================================
st.markdown("""
<style>
:root {
    --label-bg: #dfe3f4;
    --head-bg: #e8ebf5;
    --cell-border: #bfc6d8;
    --value-border: #bfbfbf;
    --input-border: #8d97aa;
    --row-h: 58px;
    --top-h: 52px;
    --radius: 0px;
    --font-size: 15px;
}

div[data-testid="stExpander"] details {
    border-radius: 8px;
}
div[data-testid="stExpander"] details > summary {
    font-weight: 700;
}

.sheet-cell-wrap {
    height: var(--row-h);
    display: flex;
    align-items: stretch;
    margin: 0 !important;
}

.sheet-top-wrap {
    height: var(--top-h);
    display: flex;
    align-items: stretch;
    margin: 0 !important;
}

.sheet-label {
    width: 100%;
    height: 100%;
    background: var(--label-bg);
    border: 1px solid var(--cell-border);
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4px 8px;
    box-sizing: border-box;
    font-weight: 700;
    line-height: 1.2;
    font-size: var(--font-size);
}

.sheet-head {
    width: 100%;
    height: 100%;
    background: var(--head-bg);
    border: 1px solid var(--cell-border);
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4px 8px;
    box-sizing: border-box;
    font-weight: 700;
    font-size: var(--font-size);
}

.sheet-value {
    width: 100%;
    height: 100%;
    background: white;
    border: 1px solid var(--value-border);
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4px 6px;
    box-sizing: border-box;
    font-size: var(--font-size);
}

div[data-testid="stTextInput"] {
    height: var(--row-h);
    margin: 0 !important;
}
div[data-testid="stTextInput"] > div {
    height: 100%;
}
div[data-testid="stTextInput"] [data-baseweb="base-input"] {
    height: 100% !important;
    min-height: 100% !important;
}
div[data-testid="stTextInput"] input {
    height: 100% !important;
    min-height: 100% !important;
    text-align: center !important;
    border: 1.5px solid var(--input-border) !important;
    border-radius: var(--radius) !important;
    background: #ffffff !important;
    box-sizing: border-box !important;
    font-size: var(--font-size) !important;
    padding: 0 6px !important;
}
div[data-testid="stTextInput"] label {
    display: none !important;
}

div[data-testid="column"] {
    padding: 0 !important;
}

.frac {
    display: inline-block;
    vertical-align: middle;
    text-align: center;
    line-height: 1;
    margin-right: 2px;
}
.frac .top {
    display: block;
    border-bottom: 1px solid #222;
    padding: 0 2px 1px 2px;
    font-size: 0.86em;
}
.frac .bottom {
    display: block;
    padding: 1px 2px 0 2px;
    font-size: 0.86em;
}

.sheet-spacer {
    height: 8px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 유틸 함수
# =========================================================
def parse_float(text, default=0.0):
    try:
        text = str(text).strip()
        return default if text == "" else float(text)
    except Exception:
        return default


def fmt_time(t):
    return "0" if t == 0 else f"{t:.1f}초"


def sub_var(main, sub):
    return f"<i>{main}</i><sub>{sub}</sub>"


def sup_var(base_html, sup):
    return f"{base_html}<sup>{sup}</sup>"


def frac_half():
    return '<span class="frac"><span class="top">1</span><span class="bottom">2</span></span>'


def label_box(text):
    return f'<div class="sheet-cell-wrap"><div class="sheet-label">{text}</div></div>'


def head_box(text):
    return f'<div class="sheet-cell-wrap"><div class="sheet-head">{text}</div></div>'


def top_box(text):
    return f'<div class="sheet-top-wrap"><div class="sheet-label">{text}</div></div>'


def value_box(text):
    return f'<div class="sheet-cell-wrap"><div class="sheet-value">{text}</div></div>'


def calc_ke(vx, vy, m):
    return 0.5 * m * (vx**2 + vy**2)


def calc_pe(y, m, g):
    return m * g * y


def calc_me(ke, pe):
    return ke + pe


def initialize_state():
    if STATE_KEY not in st.session_state:
        st.session_state[STATE_KEY] = {
            "m": "1.0",
            "g": "9.8",
            "x": {t: "" for t in TIMES},
            "vx": {t: "" for t in TIMES},
            "y": {t: "" for t in TIMES},
            "vy": {t: "" for t in TIMES},
        }
    return st.session_state[STATE_KEY]


def setup_korean_font():
    korean_font_candidates = [
        "Malgun Gothic",
        "AppleGothic",
        "NanumGothic",
        "Noto Sans CJK KR",
        "Noto Sans KR"
    ]

    available_fonts = {f.name for f in font_manager.fontManager.ttflist}
    selected_font = None

    for font_name in korean_font_candidates:
        if font_name in available_fonts:
            selected_font = font_name
            break

    if selected_font is not None:
        rcParams["font.family"] = selected_font

    rcParams["axes.unicode_minus"] = False


def save_response(conclusion, communication):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = SAVE_FILE.exists()

    with open(SAVE_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["time", "conclusion", "communication"])

        writer.writerow([now, conclusion, communication])


def draw_energy_chart(title, x_values, y_values, has_input):
    fig, ax = plt.subplots(figsize=(4.2, 3.2))

    if has_input:
        ax.plot(x_values, y_values, marker="o")
        ax.relim()
        ax.autoscale_view()

        y_min = min(y_values)
        y_max = max(y_values)
        if y_min == y_max:
            margin = 1.0 if y_min == 0 else abs(y_min) * 0.1
            ax.set_ylim(y_min - margin, y_max + margin)
    else:
        ax.set_xlim(min(x_values), max(x_values))
        ax.set_ylim(0, 1)

    ax.set_title(title)
    ax.set_xlabel("시간 (s)")
    ax.set_ylabel("에너지")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# =========================================================
# 화면 구성
# =========================================================
state = initialize_state()
setup_korean_font()

st.title(PAGE_TITLE)
st.markdown(TXT_INTRO, unsafe_allow_html=True)

preview_col, link_col = st.columns((5, 2))
with preview_col:
    with st.expander("실험 미리보기"):
        st.video(VIDEO_URL)

with link_col:
    st.link_button("바로가기", REFERENCE_URL, use_container_width=True)

st.markdown(TXT_ACTIVITY, unsafe_allow_html=True)

# =========================================================
# 입력 표
# =========================================================
with st.expander("운동 기록표", expanded=False):
    top_cols = st.columns([1.1, 1.2, 1.1, 1.2], gap="small")

    with top_cols[0]:
        st.markdown(top_box("물체의 질량"), unsafe_allow_html=True)
    with top_cols[1]:
        state["m"] = st.text_input(
            "mass_input",
            value=state["m"],
            key="mass_input_sheet",
            label_visibility="collapsed"
        )
    with top_cols[2]:
        st.markdown(top_box("중력가속도"), unsafe_allow_html=True)
    with top_cols[3]:
        state["g"] = st.text_input(
            "gravity_input",
            value=state["g"],
            key="gravity_input_sheet",
            label_visibility="collapsed"
        )

    m = parse_float(state["m"], 1.0)
    g = parse_float(state["g"], 9.8)

    st.markdown('<div class="sheet-spacer"></div>', unsafe_allow_html=True)

    widths = [2.1] + [0.82] * len(TIMES)

    # 시간 행
    row_time = st.columns(widths, gap="small")
    with row_time[0]:
        st.markdown(label_box("시간"), unsafe_allow_html=True)
    for i, t in enumerate(TIMES):
        with row_time[i + 1]:
            st.markdown(head_box(fmt_time(t)), unsafe_allow_html=True)

    # x 행
    row_x = st.columns(widths, gap="small")
    with row_x[0]:
        st.markdown(label_box("수평방향 위치(<i>x</i>)"), unsafe_allow_html=True)
    for i, t in enumerate(TIMES):
        with row_x[i + 1]:
            state["x"][t] = st.text_input(
                f"x_{t}",
                value=state["x"][t],
                key=f"x_sheet_{t}",
                label_visibility="collapsed"
            )

    # vx 행
    row_vx = st.columns(widths, gap="small")
    with row_vx[0]:
        st.markdown(label_box(f"수평방향 속력({sub_var('v', 'x')})"), unsafe_allow_html=True)
    for i, t in enumerate(TIMES):
        with row_vx[i + 1]:
            state["vx"][t] = st.text_input(
                f"vx_{t}",
                value=state["vx"][t],
                key=f"vx_sheet_{t}",
                label_visibility="collapsed"
            )

    # y 행
    row_y = st.columns(widths, gap="small")
    with row_y[0]:
        st.markdown(label_box("연직방향 위치(<i>y</i>)"), unsafe_allow_html=True)
    for i, t in enumerate(TIMES):
        with row_y[i + 1]:
            state["y"][t] = st.text_input(
                f"y_{t}",
                value=state["y"][t],
                key=f"y_sheet_{t}",
                label_visibility="collapsed"
            )

    # vy 행
    row_vy = st.columns(widths, gap="small")
    with row_vy[0]:
        st.markdown(label_box(f"연직방향 속력({sub_var('v', 'y')})"), unsafe_allow_html=True)
    for i, t in enumerate(TIMES):
        with row_vy[i + 1]:
            state["vy"][t] = st.text_input(
                f"vy_{t}",
                value=state["vy"][t],
                key=f"vy_sheet_{t}",
                label_visibility="collapsed"
            )

    # 숫자 변환
    x_vals = {t: parse_float(state["x"][t], 0.0) for t in TIMES}
    vx_vals = {t: parse_float(state["vx"][t], 0.0) for t in TIMES}
    y_vals = {t: parse_float(state["y"][t], 0.0) for t in TIMES}
    vy_vals = {t: parse_float(state["vy"][t], 0.0) for t in TIMES}

    # 에너지 계산
    ke_values = {}
    pe_values = {}
    me_values = {}

    for t in TIMES:
        ke = calc_ke(vx_vals[t], vy_vals[t], m)
        pe = calc_pe(y_vals[t], m, g)
        me = calc_me(ke, pe)

        ke_values[t] = ke
        pe_values[t] = pe
        me_values[t] = me

    vx2 = sup_var(sub_var("v", "x"), "2")
    vy2 = sup_var(sub_var("v", "y"), "2")
    ke_formula = f"운동 에너지({frac_half()}<i>m</i>({vx2}+{vy2}))"

    # 운동에너지 행
    row_ke = st.columns(widths, gap="small")
    with row_ke[0]:
        st.markdown(label_box(ke_formula), unsafe_allow_html=True)
    for i, t in enumerate(TIMES):
        with row_ke[i + 1]:
            st.markdown(value_box(f"{ke_values[t]:.3f}"), unsafe_allow_html=True)

    # 위치에너지 행
    row_pe = st.columns(widths, gap="small")
    with row_pe[0]:
        st.markdown(label_box("위치 에너지(<i>mgy</i>)"), unsafe_allow_html=True)
    for i, t in enumerate(TIMES):
        with row_pe[i + 1]:
            st.markdown(value_box(f"{pe_values[t]:.3f}"), unsafe_allow_html=True)

    # 역학적에너지 행
    row_me = st.columns(widths, gap="small")
    with row_me[0]:
        st.markdown(label_box("역학적 에너지"), unsafe_allow_html=True)
    for i, t in enumerate(TIMES):
        with row_me[i + 1]:
            st.markdown(value_box(f"{me_values[t]:.3f}"), unsafe_allow_html=True)

# =========================================================
# 그래프
# =========================================================
st.markdown(TXT_GRAPH_GUIDE, unsafe_allow_html=True)

has_any_input = any(
    str(state[var][t]).strip() != ""
    for var in ["x", "vx", "y", "vy"]
    for t in TIMES
)

with st.expander("에너지 그래프", expanded=False):
    col1, col2, col3 = st.columns(3, gap="small")

    with col1:
        draw_energy_chart(
            "시간에 따른 운동 에너지",
            TIMES,
            [ke_values[t] for t in TIMES],
            has_any_input
        )

    with col2:
        draw_energy_chart(
            "시간에 따른 위치 에너지",
            TIMES,
            [pe_values[t] for t in TIMES],
            has_any_input
        )

    with col3:
        draw_energy_chart(
            "시간에 따른 역학적 에너지",
            TIMES,
            [me_values[t] for t in TIMES],
            has_any_input
        )

# =========================================================
# 학생 응답
# =========================================================
st.markdown(TXT_CONCLUSION, unsafe_allow_html=True)

student_conclusion = st.text_area(
    "결론 도출에 대한 나의 생각",
    placeholder="포물선 운동을 하는 물체의 역학적 에너지가 시간에 따라 어떻게 되는지 자신의 말로 설명해보세요.",
    height=180,
    key="student_conclusion"
)

st.markdown(TXT_COMMUNICATION, unsafe_allow_html=True)

student_communication = st.text_area(
    "소통하기에 대한 나의 생각",
    placeholder="실험 오차를 줄이기 위한 방법을 자신의 생각으로 작성해보세요.",
    height=180,
    key="student_communication"
)

if st.button("GPT 평가 및 피드백 받기", use_container_width=True):
    if student_conclusion.strip() == "" and student_communication.strip() == "":
        st.warning("의견을 먼저 입력해주세요.")
    else:
        save_response(student_conclusion, student_communication)
        st.success("저장 완료")
        st.write("저장 위치:", SAVE_FILE)

        # 필요하면 아래 주석을 해제해서 저장된 응답을 바로 확인할 수 있습니다.
        # if SAVE_FILE.exists():
        #     df_response = pd.read_csv(SAVE_FILE, encoding="utf-8-sig")
        #     st.dataframe(df_response, use_container_width=True)

# =========================================================
# GPT 평가 기능은 나중에 필요할 때 아래처럼 연결 가능
# =========================================================
# from openai import OpenAI
# client = OpenAI()
#
# if student_conclusion.strip() != "":
#     prompt = f"..."
#     response = client.responses.create(
#         model="gpt-5",
#         input=prompt
#     )
#     st.write(response.output_text)