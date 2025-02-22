import time
import streamlit as st

def stream_data():
    for word in st.session_state.answer.split(" "):
        yield word + " "
        time.sleep(0.02)
