import streamlit as st
from src.utils.case_service import CaseService

questions = [
    "Contradictions",
    "Expert Outline",
    "Timeline",
    "Entities",
    "Final Outline",
]


# Function to render the suggested questions
def suggested_questions(case_service: CaseService):
    st.markdown(
        """
        <style>
        .custom-button {
            display: block;
            width: 100%;
            height: 50px;
            font-size: 18px;
            margin: 5px 0;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.write("Below are some suggested questions you might find useful:")

    cols = st.columns(len(questions))

    for col, question in zip(cols, questions):
        with col:
            if st.button(question, key=question, help=question, use_container_width=True):
                with st.spinner("Processing request..."):
                    response = case_service.answer_question(question, st.session_state.selected_case, st.session_state.selected_mod)
                    if response.get("error"):
                        st.session_state.answer = "We are sorry something went wrong. Please try again later."
                        st.stop()
                    st.session_state.answer = response["answer"]
