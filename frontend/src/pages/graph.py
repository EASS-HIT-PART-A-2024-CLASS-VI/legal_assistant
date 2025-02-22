import logging
import os

import streamlit as st
from src.logger import setup_logging
from src.utils.case_service import CaseService
from streamlit_agraph import Config, Edge, Node, agraph
from streamlit_agraph.config import ConfigBuilder

setup_logging()
logger = logging.getLogger(__name__)

FASTAPI_URI = os.getenv("FASTAPI_URI", "http://localhost:8000")

case_service = CaseService(
    fastapi_uri=FASTAPI_URI, access_token=st.session_state.access_token, refresh_token=st.session_state.refresh_token, id_token=st.session_state.id_token
)


def has_required_properties(dictionary):
    required_properties = ["id", "properties"]
    return all(prop in dictionary for prop in required_properties)


with st.sidebar:
    home_page_button = st.button("Home Page", type="primary")
    if home_page_button:
        st.switch_page("ui_app.py")

config_builder = ConfigBuilder()
config = config_builder.build()
config.save("config.json")
config = Config(from_json="config.json")


def create_graph(graph_data):
    edges = []
    nodes_ids = []
    nodes = []

    for graph in graph_data:
        for item in graph:
            item_id = item.get("id", None)

            if "labels" in item and item_id not in nodes_ids:
                if has_required_properties(item):
                    node_id = item_id
                    node_label = (item.get("properties") or {}).get("id") or (item.get("properties") or {}).get("name")
                    nodes_ids.append(node_id)
                    nodes.append(
                        Node(
                            id=node_id,
                            label=node_label,
                            size=25,
                        )
                    )

            elif "relation" in item:
                src_node = item.get("src_node", None)
                dest_node = item.get("dest_node", None)
                relation = item.get("relation", None)
                edges.append(Edge(source=src_node, label=relation, target=dest_node))

    if not nodes or not edges:
        st.error("Sorry, we couldn't process the graph. Please try again later.")
        st.stop()
    agraph(nodes=nodes, edges=edges, config=config)


primary_graph, secondary_graph = st.tabs(["Case Graph", "Answer Graph"])

with primary_graph:
    st.header("Case Graph")
    with st.spinner("Processing Graph..."):
        response = case_service.get_graph(st.session_state.selected_case)
        primary_graph_data = response["result"]
        logger.info("Creating graph case")
        create_graph(primary_graph_data)

with secondary_graph:
    st.header("Answer Graph")
    with st.spinner("Processing Graph..."):
        response_secondary_graph = case_service.get_generate_answer_graph(
            answer=st.session_state.answer, question=st.session_state.selected_question, case_name=st.session_state.selected_case
        )
        if response_secondary_graph.get("error"):
            st.error("We are sorry something went wrong. Please try again later.")
            st.stop()
        secondary_graph_data = [response_secondary_graph.get("entities", []) + response_secondary_graph.get("relationships", [])]
        logger.info("Creating answer case")
        create_graph(secondary_graph_data)
