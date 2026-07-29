import streamlit as st

def init_state():
    if "pizza" not in st.session_state:
            st.session_state.pizza = ""
    if "dow" not in st.session_state:
        st.session_state.dow = ""
    if "cheeze" not in st.session_state:
        st.session_state.cheeze = ""
    if "toping" not in st.session_state:
        st.session_state.toping = ""
    if "count" not in st.session_state:
            st.session_state.count = 0

init_state()

def clear_state():
        st.session_state.pizza = ""
        st.session_state.count = 0
        st.session_state.dow = "초기화"
        st.session_state.cheeze = "초기화"
        st.session_state.toping = "초기화"

def add():
     st.session_state.count = st.session_state.count + 1

def dec():
     if st.session_state.count == 0:
        return 
     st.session_state.count = st.session_state.count - 1

def  make_p1():
    st.toast("P1 피자 만듭니다.")
    st.session_state.pizza = "pizza1"
    st.session_state.dow = "씬도우"
    st.session_state.cheeze = "모짜렐라"
    st.session_state.toping = "페퍼로니"
def  make_p2():
    st.toast("P2 피자 만듭니다.")
    st.session_state.pizza = "pizza2"
    st.session_state.dow = "치즈크러스트"
    st.session_state.cheeze = "체다"
    st.session_state.toping = "베이컨"
def  make_p3():
    st.toast("P3 피자 만듭니다.")
    st.session_state.pizza = "pizza3"
    st.session_state.dow = "오리지널"
    st.session_state.cheeze = "고다"
    st.session_state.toping = "불고기"

def select_pizza(pizza_name):
    st.session_state["pizza"] = pizza_name
    st.toast(f"{pizza_name} 피자를 선택했습니다.")

# -------------------------------------------------------------

st.title("Pizza")

if st.session_state.pizza != "":
    st.info(f"당신이 선택한 피자는: {st.session_state.pizza}")
    st.info(f"개수:{st.session_state.count}")

    left, right = st.columns(2)
    with left:
         st.button("추가", on_click=add, use_container_width= True)
    with right:
        st.button("감소", on_click=dec, use_container_width= True)

p1, p2, p3 = st.columns(3)
with p1:
    st.button("P1", on_click = make_p1)
with p2:
    st.button("P2", on_click = make_p2)
with p3:
    st.button("P3", on_click = make_p3)

with st.form("pizza_form"):
    input_dow = st.text_input("도우 선택",  key = "dow")
    input_cheeze = st.text_input("치즈 선택", key = "cheeze")
    input_toping = st.text_input("토핑 선택", key = "toping")
    submit = st.form_submit_button("제출")
    reset = st.form_submit_button("초기화", on_click = clear_state)




# ---------------------------------------------------------------------

if submit:
    st.subheader(f"당신이 선택한 피자는 {st.session_state.pizza}")
    st.subheader(f"당신은 {st.session_state.count}개를 주문하였습니다.")
    st.info(f"{input_dow}, {input_cheeze}, {input_toping}")

