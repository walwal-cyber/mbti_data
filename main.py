import streamlit as st

# 정답 비밀번호 설정
CORRECT_PASSWORD = "651205"

# --- ⚙️ 초기 설정 ---
# 페이지 제목 및 세션 상태 초기화
st.set_page_config(page_title="정화님 환갑 ATM", layout="centered")

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
        st.session_state.password_input = "" # 비밀번호 입력 초기화
        st.session_state.error_message = "" # 오류 메시지 초기화
        st.rerun() # ✅ st.experimental_rerun() 대신 st.rerun() 사용

    # 화면에 도움될 만한 이미지 첨부 (ATM 기계나 생일 케이크 등)
    # 

# --- 2️⃣ 두 번째 화면: 비밀번호 입력 ---
def page_2():
    """두 번째 화면: 비밀번호 입력 및 넘버패드"""
    st.markdown("<h2 style='text-align: center;'>🔐 비밀번호를 입력하십시오</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # 입력된 비밀번호를 '*'로 가려서 보여줌
    password_display = "*" * len(st.session_state.password_input)
    st.text_input("비밀번호", value=password_display, key="display", disabled=True)

    # 에러 메시지가 있으면 표시
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
    
    # 넘버 패드 레이아웃 (3x3+1)
    col1, col2, col3 = st.columns(3)
    
    # 넘버 패드 버튼 정의: 숫자, 백스페이스, 엔터
    buttons = [
        ('7', col1), ('8', col2), ('9', col3),
        ('4', col1), ('5', col2), ('6', col3),
        ('1', col1), ('2', col2), ('3', col3),
        ('C', col1), ('0', col2), ('E', col3) # C: Clear, E: Enter
    ]
    
    for label, col in buttons:
        if col.button(label, key=f"keypad_{label}", use_container_width=True):
            handle_keypad_input(label)

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
        st.session_state.error_message = "" # 새로운 입력이 들어오면 에러 메시지 초기화
    
    # 입력 후 화면 갱신
    st.rerun() # ✅ st.experimental_rerun() 대신 st.rerun() 사용

# 비밀번호 확인 함수
def check_password():
    if st.session_state.password_input == CORRECT_PASSWORD:
        st.session_state.page = 'page_3' # 정답이면 세 번째 화면으로
        st.session_state.error_message = ""
    else:
        st.session_state.error_message = "❌ 비밀번호가 틀렸습니다. 다시 입력해주세요."
        st.session_state.password_input = "" # 틀리면 비밀번호 입력 초기화

# --- 3️⃣ 세 번째 화면: 출금 안내 ---
def page_3():
    """세 번째 화면: 출금 안내 메시지"""
    st.balloons() # 축하 풍선 효과!
    st.markdown("<h1 style='text-align: center; color: green;'>✅ 출금을 시작합니다.</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>💳 카드를 투입구에 넣어주세요!</h3>", unsafe_allow_html=True)
    
    # 
    
    st.subheader("용돈 인출 중...")
    
    # '처음으로' 버튼 (선택 사항)
    if st.button("처음 화면으로 돌아가기", key="home_btn", use_container_width=True):
        st.session_state.page = 'page_1'
        st.rerun() # ✅ st.experimental_rerun() 대신 st.rerun() 사용


# --- 🗺️ 페이지 라우팅 ---
# 현재 세션 상태의 'page' 값에 따라 해당 함수를 호출하여 화면을 그림
if st.session_state.page == 'page_1':
    page_1()
elif st.session_state.page == 'page_2':
    page_2()
elif st.session_state.page == 'page_3':
    page_3()
