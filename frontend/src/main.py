import logging
import os

import streamlit as st
from src.components.side_bar import create_sidebar
from src.components.suggested_questions import suggested_questions
from src.utils.case_service import CaseService
from src.utils.logger import setup_logging
from src.utils.utils import stream_data

setup_logging()
logger = logging.getLogger(__name__)

FASTAPI_URI = os.getenv("FASTAPI_URI", "http://localhost:8000")

st.set_page_config(
    page_title="Legal-Assistant",
    page_icon="images/logo.png",
    layout="centered",
)


def main():
    with st.sidebar:
        create_sidebar(case_service)

    methods_explanations = {
        "refine": "Good for more detailed answers, but take time",
        "compact": "Like refine, but faster",
        "tree_summarize": "Good for summarization purposes ",
    }

    methods = ["tree_summarize", "compact", "refine"]

    st.title(st.session_state.selected_case)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption("*Experimental - under research")
    with col2:
        graph_button = st.button("Go to graph", type="primary")
        if graph_button:
            st.switch_page("pages/graph.py")

    user_question = st.text_area("Your Question", value=st.session_state.selected_question)
    submit_button = st.button("Submit", type="primary")
    suggested_questions(case_service)
    st.session_state.selected_mod = st.selectbox("Choose a method", methods)
    st.markdown(
        f'<p style="color:gray; font-size:12px;">{methods_explanations[st.session_state.selected_mod]}</p>',
        unsafe_allow_html=True,
    )
    st.divider()

    if submit_button:
        with st.spinner("Processing request..."):
            response = case_service.answer_question(
                user_question, st.session_state.selected_case, st.session_state.selected_mod
            )
            if response.get("error"):
                st.error("We are sorry something went wrong. Please try again later.")
                st.stop()
            st.session_state.answer = response["answer"]

    st.write_stream(stream_data)


if __name__ == "__main__":

    case_service = CaseService(fastapi_uri=FASTAPI_URI)

    if "selected_case" not in st.session_state:
        st.session_state.selected_case = ""

    if "selected_question" not in st.session_state:
        st.session_state.selected_question = ""

    if "answer" not in st.session_state:
        st.session_state.answer = ""

    main()
