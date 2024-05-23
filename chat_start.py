import streamlit as st
from openai import OpenAI

openai_key = st.secrets["openai_key"]
client = OpenAI(api_key=openai_key, base_url="https://openai.maosuyu.com/v1")

st.set_page_config(page_title="Chat with LLM", page_icon=":smiley:", layout="wide")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示聊天记录
for item in st.session_state.messages:
    st.chat_message(item["name"]).write(item["message"])

# 底部输入框
prompt = st.chat_input(placeholder="说点什么吧...", disabled=False)

# 如果有输入，将输入添加到聊天记录中
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"name": "user", "message": prompt})
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": m["name"], "content": m["message"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        # ev = sse.event_stream()
        # st.write_stream(ev)
        res = st.write_stream(stream)
    st.session_state.messages.append({"name": "assistant", "message": res})
