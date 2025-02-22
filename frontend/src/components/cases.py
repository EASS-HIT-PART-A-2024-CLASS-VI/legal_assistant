import logging

import streamlit as st
from src.utils.case_service import CaseService
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def cases(case_service: CaseService):
    st.markdown(
        """
        <style>
        .custom-button {
            display: block;
            width: 50%;
            height: 50px;
            font-size: 18px;
            margin: 5px 0;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Cases")

    if "cases" not in st.session_state:
        st.session_state.cases = case_service.get_names_cases().get("cases", [])

    if st.session_state.selected_case == "":
        if len(st.session_state.cases) > 0:
            st.session_state.selected_case = st.session_state.cases[0]

    for label in st.session_state.cases:
        col1, col2 = st.columns([0.9, 0.1])

        with col1:
            if st.button(label, key=label, help=label, use_container_width=True):
                st.session_state.selected_case = label
                if st.session_state["is_main_page"] is False:
                    st.session_state.is_main_page = True
                    st.session_state.answer = ""
                    st.switch_page("main.py")

        with col2:
            if st.button("X", key=f"delete_{label}", help=f"Delete {label}", use_container_width=True):
                st.session_state.cases.remove(label)
                case_service.delete_case(label)
                st.rerun()
