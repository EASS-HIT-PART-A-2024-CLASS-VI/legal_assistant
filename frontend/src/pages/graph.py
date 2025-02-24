import logging
import os

import streamlit as st
from src.utils.case_service import CaseService
from streamlit_agraph import Config, Edge, Node, agraph
from streamlit_agraph.config import ConfigBuilder

from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

FASTAPI_URI = os.getenv("FASTAPI_URI", "http://localhost:8000")

case_service = CaseService(fastapi_uri=FASTAPI_URI)



with st.sidebar:
    home_page_button = st.button("Home Page", type="primary")
    if home_page_button:
        st.switch_page("main.py")

config_builder = ConfigBuilder()
config = config_builder.build()
config.save("config.json")
config = Config(from_json="config.json")


def create_graph(graph_data):
    edges = []
    nodes_ids = []
    nodes = []

    if "entities" in graph_data:
        for item in graph_data["entities"]:
            item_id = item.get("id", None)

            if "labels" in item and item_id not in nodes_ids:
                if "properties" in item:
                    node_id = item_id
                    node_label = item.get("properties", {}).get("id") or item.get("properties", {}).get("name")
                    nodes_ids.append(node_id)
                    nodes.append(
                        Node(
                            id=node_id,
                            label=node_label,
                            size=25,
                        )
                    )

    if "relationships" in graph_data:
        for item in graph_data["relationships"]:
            src_node = item.get("src_node", None)
            dest_node = item.get("dest_node", None)
            relation = item.get("relation", None)
            edges.append(Edge(source=src_node, label=relation, target=dest_node))

    if not nodes or not edges:
        st.error("Sorry, we couldn't process the graph. Please try again later.")
        st.stop()
    agraph(nodes=nodes, edges=edges, config=config)


st.title("Case Graph")

with st.spinner("Processing Graph..."):
    response = case_service.get_graph(st.session_state.selected_case)
    primary_graph_data = response
    logger.info("Creating graph case")
    create_graph(primary_graph_data)
