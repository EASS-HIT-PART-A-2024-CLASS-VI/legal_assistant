from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel


class ResponseMod(str, Enum):
    REFINE = "refine"
    COMPACT = "compact"
    TREE_SUMMARIZE = "tree_summarize"
    ACCUMULATE = "accumulate"
    COMPACT_ACCUMULATE = "compact_accumulate"


class Question(BaseModel):
    text: str
    response_mod: Optional[ResponseMod] = ResponseMod.TREE_SUMMARIZE


class Case(BaseModel):
    case_name: str
    version: str = "1.0"


class UploadFileResponse(BaseModel):
    message: str = "Create case successfully"
