
import streamlit as st

st.title("자기소개")

st.divider()

st.header("이름은?")  

name = st.text_input("이름을 입력하세요")

if name:  # name에 빈 문자열이 아닌 값이 들어 있으면 인사말을 표시합니다.
    st.write(f"안녕하세요, {name}님!")  # 입력받은 이름을 포함해 인사말을 화면에 출력합니다.
else:  # 아직 이름을 입력하지 않은 상태라면 안내 메시지를 표시합니다.
    st.warning("이름을 입력하면 인사말이 표시됩니다.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.

st.divider()

st.header("관심분야는?")

interest = st.selectbox("관심 있는 분야를 선택해주세요", ["Python", "JavaScript", "SQL"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.write(f"선택한 언어: {interest}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

st.divider()

st.header("한 줄로 자기소개를 한다면?")

comment = st.text_area("간단하게 작성해주세요")  # 자기소개.

if comment:  # 이름과 학습 정리가 모두 입력되었을 때만 결과 영역을 표시합니다.
    st.success(f"한 줄의 자기소개: {comment}")  # 사용자가 작성한 자기 소개를 작은 글씨로 표시합니다.
    st.warning("내용을 입력하세요.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.

st.divider()

st.header("결과")

if name and interest and comment:
    st.success("입력이 완료되었습니다!")

    with st.container():
        st.subheader("📋 자기소개 카드")
        st.write(f"**이름** : {name}")
        st.write(f"**관심 분야** : {interest}")
        st.write(f"**자기소개**")
        st.write(comment)
else:
    st.warning("모든 항목을 입력해주세요.")