from pathlib import Path  # 파일과 폴더 경로를 안전하게 다루기 위해 pathlib의 Path를 가져옵니다.

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("Streamlit 사용 실습")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

st.divider()

st.header("귀여운 햄토리 출력")  

current_file = Path(__file__).resolve()
image_dir = current_file.parent.parent / "imgs"

image_files = sorted(
    list(image_dir.glob("*.png"))
    + list(image_dir.glob("*.jpg"))
    + list(image_dir.glob("*.jpeg"))
)

if not image_files:  # 이미지 파일이 하나도 없으면, 화면에 오류 대신 안내 메시지를 보여 줍니다.
    st.warning(f"이미지 파일을 찾을 수 없습니다: {image_dir}")
    st.write("imgs 폴더에 png, jpg, jpeg 파일을 넣은 뒤 다시 실행해 보세요.")
else:
    # 이미지가 여러 개 있을 수도 있으므로 selectbox로 어떤 이미지를 보여 줄지 선택하게 합니다.
    # 이미지가 내려오는 게 아님
    selected_name = st.selectbox(
        "화면에 출력할 이미지를 선택하세요",
        [image_file.name for image_file in image_files],
    )

    selected_image = image_dir / selected_name

    st.caption(f"이미지 경로: {selected_image}")  # 현재 어떤 파일을 출력하는지 작은 설명으로 보여 줍니다.

    st.image(
        selected_image,
        caption=f"{selected_name} 파일을 Streamlit 화면에 출력했습니다용.",
        use_container_width=True,
    )

st.divider()

st.header("오늘의 행복지수는?")  

name = st.text_input("이름")  # 사용자가 입력한 이름을 문자열로 저장합니다.
score = st.number_input("오늘의 행복지수", min_value=-1000000000, max_value=100, value=70)  # 0부터 100 사이의 숫자를 행복지수로 저장합니다.
comment = st.text_area("오늘 하루에 대한 한줄평")  # 여러 줄 입력창에서 한줄평 내용을 문자열로 저장합니다.

if score >= 80:  # 이해도 점수가 80점 이상이면 다음 단계로 넘어갈 수 있다는 메시지를 준비합니다.
    message = "좋습니다. 좋은 하루를 보내셨군요 찡긋."  # 화면에 출력할 피드백 문장을 변수에 저장합니다.
elif score >= 50:  # 80점 미만이지만 50점 이상이면 복습을 권장하는 메시지를 준비합니다.
    message = "아쉽네요. 남은 하루는 더 행복하시길 바랍니다."  # 화면에 출력할 피드백 문장을 변수에 저장합니다.
else:  # 50점 미만이면 기초 예제를 다시 확인하라는 메시지를 준비합니다.
    message = "괜찮아요. 우리에겐 내일도 있잖아요~"  # 화면에 출력할 피드백 문장을 변수에 저장합니다.

if name and comment:  # 이름과 학습 정리가 모두 입력되었을 때만 결과 영역을 표시합니다.
    st.success(f"{name}님의 행복지수")  # 결과 영역의 제목을 성공 메시지 형태로 표시합니다.
    st.write(message)  # 점수 조건에 따라 준비한 피드백 문장을 출력합니다.
    st.caption(f"오늘의 한줄평: {comment}")  # 사용자가 작성한 학습 정리를 작은 글씨로 표시합니다.
else:  # 필수 입력값이 부족하면 결과 대신 안내 메시지를 표시합니다.
    st.warning("이름과 오늘의 행복지수를 입력하세요.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.

st.divider()

st.header("내일의 행복지수 미리보기") 

score = st.number_input("오늘의 행복지수를 입력하세요", min_value=0, max_value=100, value=70)  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
next_year_score = score + 7  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.write(f"오늘의 행복지수는 {score}점 입니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
st.write(f"내일은 행운의 7이 함께해서 {next_year_score}점이 될겁니다!")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

st.divider()

st.header("내일을 행복하게 보내시겠습니까?!") 

ok = st.selectbox("정말요?", ["네에!", "네에엥!!!!!!"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
okok = st.radio("정말 정말요?", ["네에 정말요!!!", "네에 진짜요!!!"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.write(f"대답: {ok}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
st.write(f"한번더: {okok}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

if ok == "네에!" and okok == "네에 정말요!!!":  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.info("네 꼭 이뤄지길 바랍니당~")  # 다음 행동을 안내하는 정보 메시지를 표시합니다.
