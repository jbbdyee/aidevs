import streamlit as st

#  상태 초기화 ------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "survey_submitted" not in st.session_state:
    st.session_state.survey_submitted = False

if "survey_result" not in st.session_state:
    st.session_state.survey_result = {}

#  로그인 ------------------------------------------

if not st.session_state.logged_in:
    st.title("로그인")

    with st.form("login_form"):
        user_id = st.text_input("ID입력")
        password = st.text_input("PWD입력", type="password")
        login_button = st.form_submit_button("로그인")

        if login_button:
            if user_id == "id01" and password == "pwd01":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 틀렸습니다.")

#  설문 조사 ------------------------------------------------------

elif not st.session_state.survey_submitted:
    st.title("설문 조사")

    st.divider()

    st.subheader("이름")
    name = st.text_input("이름을 입력하세요")  # 사용자가 입력한 이름 문자열을 name 변수에 저장합니다.

    st.subheader("나이")
    age = st.number_input("나이를 입력하세요", min_value=0, max_value=120, value=20)

    st.subheader("관심 카테고리")
    style = st.selectbox("관심 있는 카테고리를 선택하세요", ["상의", "하의", "악세사리"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    level = st.radio("평소 쇼핑 수준을 선택하세요", ["적음", "중간", "많음"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

    st.subheader("쇼핑 금액")

    show_detail = st.checkbox("상세 설명 보기")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    score = st.slider("쇼핑 금액", min_value=0, max_value=100, value=0)  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

    if show_detail:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
        st.write("쇼핑 금액의 기간은 1개월 기준입니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
        st.write("단위는 만원 입니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

    st.subheader("선호하는 쇼핑몰 플랫폼")

    shopping_mall = st.multiselect(
    "자주 이용하는 쇼핑몰을 모두 선택하세요.",
    [
        "무신사",
        "29CM",
        "지그재그",
        "에이블리",
        "쿠팡",
        "ZARA"
    ]
)
    st.subheader("당신에게 패션이란..")

    fashion_comment = st.text_area(
    "평소 쇼핑할 때 가장 중요하게 생각하는 것은 무엇인가요?"
)

    submitted = st.button("설문 제출")

#  확인 및 저장 ----------------------------------------------------------

    if submitted:
        if not name:
            st.error("이름을 입력해주세요.")

        elif not shopping_mall:
            st.error("쇼핑몰을 한 개 이상 선택해주세요.")

        elif not fashion_comment:
            st.error("패션에 대한 생각을 입력해주세요.")

        else:
            st.session_state.survey_result = {
                "name": name,
                "age": age,
                "style": style,
                "level": level,
                "score": score,
                "shopping_mall": shopping_mall,
                "fashion_comment": fashion_comment,
            }

            st.session_state.survey_submitted = True
            st.rerun()

# 설문 조사 결과 -----------------------------------------------------

else:
    st.title("설문 조사 결과")

    result = st.session_state.survey_result

    st.success(f"{result['name']}님의 설문이 완료되었습니다!")

    st.divider()

    st.write(f"**이름:** {result['name']}")
    st.write(f"**나이:** {result['age']}세")

    st.write(f"**관심 카테고리:** {result['style']}")
    st.write(f"**평소 쇼핑 수준:** {result['level']}")
    st.write(f"**한 달 쇼핑 금액:** {result['score']}만 원")

    st.write("선호하는 쇼핑몰은: ", ", ".join(result["shopping_mall"]))
    st.write("패션에 대한 한마디: ", result["fashion_comment"])

    st.divider()

    st.info("고생하셨습니다!")

#  ----------------------------------------------