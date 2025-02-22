import logging

import streamlit as st

from src.components.cases import cases
from src.utils.case_service import CaseService
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def create_sidebar(case_service: CaseService):
    st.logo("images/logo.png", size="large")
    st.text(f"Welcome, Mor")
    cases(case_service)
    st.sidebar.page_link("pages/add_case.py", label="+Add")
    st.divider()
    st.sidebar.page_link("pages/real_time_recording.py", label="Real time recording")
    st.divider()
    st.sidebar.markdown("**Avatar (Coming Soon)**")
    st.divider()
