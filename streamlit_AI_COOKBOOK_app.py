import streamlit as st
import sys
# Font Awesome 아이콘을 사용하기 위해 라이브러리를 import
import streamlit.components.v1 as components

sys.path.append("dist")
import openai
# Use this way
from dist import ffchat as ffc
# ...or this way
from dist.ffchat import (
    set_embeddings,
    download_embeddings,
    remove_embeddings,
    load_mydata_from_embeddings,
    load_mydata_from_source,
)



set_embeddings(load_mydata_from_embeddings("embeddings/레시피_질의응답_통합1_embeddings.csv"))
set_embeddings(load_mydata_from_embeddings("embeddings/질의응답2_요리재료ver_embeddings.csv"))
set_embeddings(load_mydata_from_embeddings("embeddings/recipes_embeddings.csv"))
print(f"loaded embeddings: {ffc.embedding_names()}\n\n")


# 사이드바에 사용자 입력을 받기
user_api_key = st.sidebar.text_input("OpenAI API Key:", "API Key Here!")

# 사이드바에서 선택할 수 있는 옵션
chef_cre_option = st.sidebar.selectbox("요리사의 창의성", ["사실적인 요리사", "밸런스 있는 요리사", "창의적인 요리사"])

if chef_cre_option == "사실적인 요리사":
    chef_level = 1
if chef_cre_option == "밸런스 있는 요리사":
    chef_level = 4
if chef_cre_option == "창의적인 요리사":
    chef_level = 8

# 사이드바 버튼 및 적용
if st.sidebar.button("적용"):
    st.sidebar.write("적용되었습니다\n")
    st.sidebar.write("요리사의 성격: {}".format(chef_cre_option))
    st.sidebar.write("요리사의 창의성 레벨: {}".format(chef_level))

# Test queries
def test(query):
    informed = '*' if ffc.is_informed() else ''
    print(f"[{query}]{informed}\n")
    try:
        return ffc.ask(query)
    except Exception as e:
        return "*** 사이드바에 API KEY를 입력해주시거나 다시 확인해주세요! ***"
    
# Level setting
ffc.set_model('gpt-3.5 (long)')  # 'gpt-3.5 (short)', 'gpt-4'
print(f"Model: {ffc.get_model()}\n")
ffc.set_creativity(chef_level)
ffc.set_expertise("Chef")

# Set OPENAI_API_KEY
openai.api_key = user_api_key

st.markdown(
        """
        <style>
            .user-message {
                background-color: #F2F2F2;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 10px;
                color: #000;
                text-align: left;
                font-family: Kalam;
                font-size: 15px;
                font-style: normal;
                font-weight: 400;
                line-height: 40px;
                letter-spacing: -0.32px;
            }
            .bot-message {
                background-color: #FFFFFF;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 10px;
                color: #000;
                text-align: left;
                font-family: Kalam;
                font-size: 15px;
                font-style: normal;
                font-weight: 400;
                line-height: 40px;
                letter-spacing: -0.32px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def initialize_seesion_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "bot_prompt" not in st.session_state:
        st.session_state.bot_prompt = []

def on_click_callback():
    user_prompt = st.session_state.user_prompt
    st.session_state.history.append(user_prompt)
    bot_prompt = get_bot_prompt(user_prompt)
    st.session_state.bot_prompt.append(bot_prompt)

def get_bot_prompt(user_input):
    bot_answer = test(user_input)
    return bot_answer

initialize_seesion_state()

st.title("AI COOKBOOK")

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")
credit_card_placeholder = st.empty()

with chat_placeholder:
    for i, chat in enumerate(st.session_state.history):
        st.markdown(f'<div class="user-message"><i class="fas fa-user"></i> {chat}</div>', unsafe_allow_html=True)
        if i < len(st.session_state.bot_prompt):
            bot_prompt = st.session_state.bot_prompt[i]
            st.markdown(f'<div class="bot-message"><i class="fas fa-robot"></i> {bot_prompt}</div>', unsafe_allow_html=True)

with prompt_placeholder:
    st.markdown("**Chat** - _press Enter to Submit_")
    cols = st.columns((6,1))
    cols[0].text_input(
        "Chat",
        value="Hello, bot",
        label_visibility="collapsed",
        key="user_prompt",
    )
    cols[1].form_submit_button(
        "Submit",
        type="primary",
        on_click=on_click_callback
    )