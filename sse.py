import json
import streamlit as st

import requests

def event_stream():
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url="http://127.0.0.1:10000/webapi/chat/chat",
        stream=True,
        data=json.dumps({"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}),
        headers=headers)
    for line in response.iter_lines():
        if line:
            res: str = line.decode('utf-8').split(":", 1)[1].strip()
            st.session_state.data_res += res
            yield res  # decode from bytes to string
