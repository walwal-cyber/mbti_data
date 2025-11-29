import streamlit as st

# 정답 비밀번호 설정
CORRECT_PASSWORD = "651205"

# 🔑 CSS 주입 함수
def inject_custom_css():
    """모바일 환경에서 컬럼을 1열로 쌓지 않고 3열 레이아웃을 강제하는 CSS를 주입합니다."""
    st.markdown("""
        <style>
        /* 모든 버튼의 크기 조정 */
        div.stButton > button {
            width: 100%;
            height: 70px; /* 버튼 높이를 키워서 누르기 쉽게 조정 */
            font-size: 24px;
            margin-bottom: 5px; /* 버튼 사이에 약간의 간격 추가 */
        }
        
        /* st.columns (넘버패드 컨테이너)에 대한 스타일 강제 적용 */
        div[data-testid="stColumns"] {
            display: flex;
            flex-direction: row; /* 반드시 가로로 배열 */
            flex-wrap: wrap; 
            justify-content: space-between;
            gap: 10px; /* 컬럼 간 간격 */
        }
        
        /* 각 컬럼 요소 (넘버패드 버튼 컨테이너)에 대한 스타일 강제 적용 */
        div[data-testid="stColumns"] > div {
            flex-grow: 0;
            flex-shrink: 0;
            flex-basis: calc(33.33% - 7px); /* 3개 컬럼 너비 강제 (gap 고려하여 조정) */
            min-width: 90px; /* 최소 너비 지정 */
        }

        /* 비밀번호 표시창 스타일 */
        .password-display-box {
            text-align: center; 
            font-size: 40px; 
            border: 2px solid #ccc; 
            padding: 10px; 
            border-radius: 5px; 
            margin-bottom: 20px;
            letter-spacing: 10px; /* 동그라미 사이 간격 추가 */
        }
        </style>
        """, unsafe_allow_html=True)


# --- ⚙️ 초기 설정 ---
# 페이지 제목 및 세션 상태 초기화
st.set_page_config(page_title="정화님 환갑 ATM", layout="centered")

# CSS 주입
inject_custom_css()

# 'page'라는 세션 상태 변수가 없으면 'page_1'로 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'page_1'
    st.session_state.password_input = ""
    st.session_state.error_message = ""

# --- 1️⃣ 첫 번째 화면: 축하 메시지 및 출금 버튼 ---
def page_1():
    """첫 번째 화면: 축하 메시지와 출금 버튼"""
    st.markdown("<h1 style='text-align: center; color: #ff6347;'>💐 정화의 60번째 생일을 축하합니다! 💖</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # 버튼 클릭 시 두 번째 페이지로 이동
    if st.button("💰 출금", key="withdraw_btn", help="용돈을 인출합니다.", use_container_width=True):
        st.session_state.page = 'page_2'
        st.session_state.password_input = "" 
        st.session_state.error_message = ""
        st.rerun()

# --- 2️⃣ 두 번째 화면: 비밀번호 입력 ---
def page_2():
    """두 번째 화면: 비밀번호 입력 및 넘버패드"""
    st.markdown("<h2 style='text-align: center;'>🔐 비밀번호를 입력하십시오</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # 입력된 비밀번호를 검은색 동그라미(●)로 표시
    password_display = "●" * len(st.session_state.password_input)
    
    st.markdown(
        f"""
        <div class="password-display-box">
            {password_display}
        </div>
        """,
        unsafe_allow_html=True
    )

    # 에러 메시지가 있으면 표시
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
    
    # 넘버 패드 레이아웃 (3x3+1)
    col1, col2, col3 = st.columns(3)
    
    # 넘버 패드 버튼 정의: 숫자, 클리어, 엔터
    buttons = [
        ('7', col1), ('8', col2), ('9', col3),
        ('4', col1), ('5', col2), ('6', col3),
        ('1', col1), ('2', col2), ('3', col3),
        ('C', col1), ('0', col2), ('E', col3) # C: Clear, E: Enter
    ]
    
    for label, col in buttons:
        # 버튼 스타일을 적용하기 위해 on_click 사용
        col.button(label, key=f"keypad_{label}", use_container_width=True, on_click=handle_keypad_input, args=(label,))

# 넘버 패드 입력 처리 함수
def handle_keypad_input(key):
    # 'C'는 초기화 (Clear)
    if key == 'C':
        st.session_state.password_input = ""
        st.session_state.error_message = ""
    # 'E'는 입력 완료 (Enter)
    elif key == 'E':
        check_password()
    # 숫자는 비밀번호 입력에 추가 (최대 6자리)
    elif len(st.session_state.password_input) < 6:
        st.session_state.password_input += key
        st.session_state.error_message = "" 
    
    st.rerun()

# 비밀번호 확인 함수
def check_password():
    if st.session_state.password_input == CORRECT_PASSWORD:
        st.session_state.page = 'page_3' 
        st.session_state.error_message = ""
    else:
        st.session_state.error_message = "❌ 비밀번호가 틀렸습니다. 다시 입력해주세요."
        st.session_state.password_input = ""

# --- 3️⃣ 세 번째 화면: 출금 안내 ---
def page_3():
    """세 번째 화면: 출금 안내 메시지"""
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: green;'>✅ 출금을 시작합니다.</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>💳 카드를 투입구에 넣어주세요!</h3>", unsafe_allow_html=True)
    
    st.subheader("용돈 인출 중...")


# --- 🗺️ 페이지 라우팅 ---
if st.session_state.page == 'page_1':
    page_1()
elif st.session_state.page == 'page_2':
    page_2()
elif st.session_state.page == 'page_3':
    page_3()
