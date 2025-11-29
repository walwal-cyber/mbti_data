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
        st.rerun()

# --- 2️⃣ 두 번째 화면: 비밀번호 입력 ---
def page_2():
    """두 번째 화면: 비밀번호 입력 및 넘버패드"""
    st.markdown("<h2 style='text-align: center;'>🔐 비밀번호를 입력하십시오</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # **수정 사항 1: 입력된 비밀번호를 검은색 동그라미로 표시**
    # CSS를 사용하여 글꼴 크기를 키우고 동그라미 모양으로 보이게 합니다.
    # U+25CF (●) 검은색 동그라미 문자를 사용합니다.
    password_display = "●" * len(st.session_state.password_input)
    
    st.markdown(
        f"""
        <div style="text-align: center; font-size: 40px; border: 2px solid #ccc; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
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
        # 버튼 스타일을 조정하여 더 잘 보이게 할 수 있습니다. (예: font-size)
        col.button(label, key=f"keypad_{label}", use_container_width=True, on_click=handle_keypad_input, args=(label,))

# 넘버 패드 입력 처리 함수 (on_click 인자로 넘겨줄 수 있도록 수정)
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
    
    # 입력 후 화면 갱신 (on_click을 사용하면 함수가 실행된 후 자동으로 rerun되므로, 명시적인 st.rerun()은 생략 가능하나, 
    # Streamlit이 버튼 클릭 외의 세션 상태 변경을 감지하도록 명시적으로 유지하는 것이 안전합니다.)
    st.rerun()

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
    
    # **수정 사항 2: '처음 화면으로 돌아가기' 버튼 제거**
    # 해당 버튼 코드를 제거했습니다.


# --- 🗺️ 페이지 라우팅 ---
# 현재 세션 상태의 'page' 값에 따라 해당 함수를 호출하여 화면을 그림
if st.session_state.page == 'page_1':
    page_1()
elif st.session_state.page == 'page_2':
    page_2()
elif st.session_state.page == 'page_3':
    page_3()
