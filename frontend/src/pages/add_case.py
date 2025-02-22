import logging
import os

import streamlit as st
from src.components.side_bar import create_sidebar

from src.utils.case_service import CaseService
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

FASTAPI_URI = os.getenv("FASTAPI_URI", "http://localhost:8000")

case_service = CaseService(fastapi_uri=FASTAPI_URI)


def validate_case_name(user_input):
    if not user_input:
        return "you must specify case name"
    return None


def validate_file(uploaded_file):
    supported_extensions = ["txt", "docx", "pdf"]
    if not uploaded_file:
        return "No file uploaded."
    for file in uploaded_files:
        if not file.name.split(".")[-1] in supported_extensions:
            return f"Unsupported file type: {file.name}. Please upload txt, docx, or pdf files only."

    return None


with st.sidebar:
    create_sidebar(case_service)

st.title("Upload files to create a new case")
st.session_state.is_main_page = False
placeholder = st.empty()
with placeholder.container():
    new_case_name = st.text_input("*Please enter the name of the case", "")
    uploaded_files = st.file_uploader("*Choose a file", accept_multiple_files=True)
    submit_button_files = st.button("Create case")

if submit_button_files:
    case_name_error = validate_case_name(new_case_name)
    logger.info(f"uploaded_files - {uploaded_files}")
    file_error = validate_file(uploaded_files)
    logger.info(f"case_name_error - {case_name_error}")
    logger.info(f"file_error - {file_error}")
    if case_name_error:
        st.error(case_name_error)
    elif file_error:
        st.error(file_error)
    else:
        placeholder.empty()
        try:
            with st.spinner("Processing request..."):
                logger.info(f"new_case_name - {new_case_name}")
                logger.info(f"Creating case - {uploaded_files}")
                files = [("files", (uploaded_file.name, uploaded_file, uploaded_file.type)) for uploaded_file in uploaded_files]
                response = case_service.upload_case(new_case_name, files)
                logger.info(f"response - {response}")
                if isinstance(response, dict):
                    if response.get("error"):
                        st.error("We are sorry something went wrong. Please verify that the file is valid.")
                        st.stop()
                st.success("Case uploaded successfully!")
                st.write(response)
                st.session_state.cases.append(new_case_name)
                logger.info(f"selected_case_name - {st.session_state.cases}")
                st.rerun()

        except Exception as e:
            logger.error(f"Error uploading case: {e}")
            st.error(f"An error occurred: {e}")
