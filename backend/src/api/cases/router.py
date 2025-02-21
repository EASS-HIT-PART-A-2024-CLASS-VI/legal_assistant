import logging
from typing import List

from fastapi import UploadFile, Form, APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from src.api.cases.model import UploadFileResponse, RagResultInput, RagResultOutPut, CasesListOutput
from src.utils.db_client import FalkorDBClient
from src.utils.logger import setup_logging

from src.api.cases import controller

setup_logging()
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/v1/cases",
    tags=["cases"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/create_new_case", status_code=HTTP_201_CREATED)
async def create_new_case(files: List[UploadFile], case_name: str = Form(...)) -> UploadFileResponse:
    await controller.create_new_case(case_name, files)
    return UploadFileResponse(message="Create case successfully",)


@router.get("/list_cases", status_code=HTTP_200_OK)
async def list_cases(db_client = FalkorDBClient()):
    res = await controller.list_cases(db_client)
    return CasesListOutput(cases=res)



@router.post("/{case_name}/search", status_code=HTTP_200_OK)
async def search(case_name: str, data: RagResultInput) -> RagResultOutPut:
    res = await controller.search(case_name, data.question, data.response_mod)
    return RagResultOutPut(answer=res)

