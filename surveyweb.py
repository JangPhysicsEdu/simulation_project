import streamlit as st
import sqlite3
import pandas as pd
import os

# ==========================================================
# 1. 설문 문항 설정 (여기에서 질문 내용을 자유롭게 수정하세요)
# ==========================================================
SURVEY_QUESTIONS = [
    "1. 나는 일상생활 중 발생할 수 있는 잠재적 위험 요소를 민감하게 인지한다.",
    "2. 현대 사회의 불확실성*기후 위기, 감염병, 디지털 위험 등)이 학생들의 안전에 직접적인 위협이 된다고 느낀다.",
    "3. 단순 안전 수칙 암기보다는 위험을 분석하고 판단하는 '위험 리터러시' 교육이 교육과정에 필수적이라고 생각한다.",
    "4. 교사는 교과 수업 중 자연스럽게 위험 관리 및 의사결정 역량을 가르칠 책임이 있다.",
    "5. 나는 위험 상황 발생 시 학생들에게 구체적인 행동 지침과 논리적 근거를 설명할 수 있는 전문성을 갖추고 있다.",
    "6. 현재 제공되는 교사 대상 안전/위험 교육 연수는 학교 현장의 실제적인 요구를 충분히 반영하고 있다.",
    "7. 우리 학교는 위험 교육을 실시하기 위한 매뉴얼이나 교육 자료(도서, 교구, 에듀테크 등)가 충분히 구비되어 있다.",
    "8. 위험 교육을 추진함에 있어서 동료 고사 및 관리자와의 협력 체계가 잘 구축되어 있다.",
    "9. 향후 기회가 주어진다면 위험 교육과 관련된 교수법 연수나 연구 모임에 적극적으로 참여할 의사가 있다.",
    "10. 체계적인 위험 교육은 학생들의 자기 보호 능력뿐만 아니라 합리적인 시민 의식을 함양하는 데 기여할 것이다."
]
# ==========================================================

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(current_dir, "data.db")
TOTAL_QUESTIONS = len(SURVEY_QUESTIONS)

def get_connection():
    return sqlite3.connect(DB_FILE)

def check_existing_user(email, phone):
    conn = get_connection()
    query = "SELECT * FROM User WHERE Email = ? AND Phone = ?"
    df = pd.read_sql_query(query, conn, params=(email, phone))
    conn.close()
    return df

def save_data(data_dict, is_update=False):
    conn = get_connection()
    cursor = conn.cursor()
    keys = list(data_dict.keys())
    values = list(data_dict.values())
    
    if is_update:
        update_cols = ", ".join([f'"{k}" = ?' for k in keys if k not in ['Email', 'Phone']])
        update_values = [data_dict[k] for k in keys if k not in ['Email', 'Phone']]
        update_values.extend([data_dict['Email'], data_dict['Phone']])
        cursor.execute(f'UPDATE User SET {update_cols} WHERE Email = ? AND Phone = ?', update_values)
    else:
        placeholders = ", ".join(["?"] * len(keys))
        columns = ", ".join([f'"{k}"' for k in keys])
        cursor.execute(f'INSERT INTO User ({columns}) VALUES ({placeholders})', values)
    conn.commit()
    conn.close()

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'basic_info'
if 'survey_data' not in st.session_state:
    st.session_state.survey_data = {}

# --- 화면 구성 ---

# 화면 1: 기본 정보 입력
if st.session_state.page == 'basic_info':
    st.title("중등 교원 대상 위험교육 인식 설문조사")
    
    with st.form("info_form"):
        name = st.text_input("성함", placeholder="성함을 입력하세요")
        subject = st.text_input("담당 과목", placeholder="예: 물리")
        experience = st.number_input("경력 (년)", min_value=0, max_value=50, step=1)
        email = st.text_input("이메일", placeholder="example@email.com")
        phone = st.text_input("휴대전화 번호", placeholder="010-0000-0000")
        
        submit_info = st.form_submit_button("설문 시작하기")
        
        if submit_info:
            if not (name and subject and email and phone):
                st.error("모든 필수 정보를 입력해주세요.")
            else:
                existing = check_existing_user(email, phone)
                if not existing.empty:
                    st.info("이전 응답 기록을 불러옵니다.")
                    st.session_state.survey_data = existing.iloc[0].to_dict()
                else:
                    st.session_state.survey_data = {
                        "Name": name, "Subject": subject, "Experience": experience,
                        "Email": email, "Phone": phone
                    }
                st.session_state.page = 'survey'
                st.rerun()

# 화면 2: 설문 응답 페이지
elif st.session_state.page == 'survey':
    st.title("📝 설문 응답")
    
    likert_options = {1: "매우 그렇지 않다", 2: "그렇지 않다", 3: "보통이다", 4: "그렇다", 5: "매우 그렇다"}
    
    # 문항 출력 루프
    for i, question_text in enumerate(SURVEY_QUESTIONS):
        idx = i + 1
        col_name = f"Answer {idx}"
        current_val = st.session_state.survey_data.get(col_name)
        
        default_index = list(likert_options.keys()).index(current_val) if current_val in likert_options else None
        
        # 질문 텍스트가 리스트에서 자동으로 반영됨
        st.session_state.survey_data[col_name] = st.radio(
            question_text, 
            options=list(likert_options.keys()),
            format_func=lambda x: likert_options[x],
            index=default_index,
            key=f"q_{idx}",
            horizontal=True
        )
        st.divider()

    # 진행률 계산
    answered_count = sum(1 for i in range(1, TOTAL_QUESTIONS + 1) if st.session_state.survey_data.get(f"Answer {i}") is not None)
    progress_val = answered_count / TOTAL_QUESTIONS
    
    st.write(f"현재 응답 진행률: {int(progress_val * 100)}% ({answered_count}/{TOTAL_QUESTIONS})")
    st.progress(progress_val)

    if st.button("설문 제출하기"):
        missing = [i for i in range(1, TOTAL_QUESTIONS + 1) if st.session_state.survey_data.get(f"Answer {i}") is None]
        
        if missing:
            st.error(f"응답하지 않은 문항이 있습니다: {', '.join(map(str, missing))}번")
        else:
            existing = check_existing_user(st.session_state.survey_data['Email'], st.session_state.survey_data['Phone'])
            save_payload = {k: v for k, v in st.session_state.survey_data.items() if k != 'ID'}
            save_data(save_payload, is_update=not existing.empty)
            st.session_state.page = 'thanks'
            st.rerun()

# 화면 3: 감사 인사
elif st.session_state.page == 'thanks':
    st.balloons()
    st.success("제출 완료!")
    st.title("🙏 참여해주셔서 감사합니다.")
    st.write(f"**{st.session_state.survey_data.get('Name')}** 선생님의 응답이 안전하게 저장되었습니다.")
    
    if st.button("처음으로 돌아가기"):
        st.session_state.clear()
        st.rerun()