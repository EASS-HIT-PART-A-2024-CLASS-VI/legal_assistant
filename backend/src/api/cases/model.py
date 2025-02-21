from enum import Enum
from typing import List, Optional

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
