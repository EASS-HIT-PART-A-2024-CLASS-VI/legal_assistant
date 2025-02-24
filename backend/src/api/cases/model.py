from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel


class RagResponseMod(str, Enum):
    REFINE = "refine"
    COMPACT = "compact"
    TREE_SUMMARIZE = "tree_summarize"
    ACCUMULATE = "accumulate"
    COMPACT_ACCUMULATE = "compact_accumulate"


class RagResultInput(BaseModel):
    question: str
    response_mod: Optional[RagResponseMod] = RagResponseMod.TREE_SUMMARIZE


class RagResultOutPut(BaseModel):
    answer: str


class CasesListOutput(BaseModel):
    cases: List[str]


class UploadFileResponse(BaseModel):
    message: str = "Create case successfully"


class Node(BaseModel):
    labels: List[str]
    id: str
    properties: Dict


class Relationship(BaseModel):
    relation: str
    src_node: str
    dest_node: str


class GraphData(BaseModel):
    relationships: List[Relationship]
    entities: List[Node]