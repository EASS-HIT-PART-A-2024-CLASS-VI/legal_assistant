import logging

from fastapi import FastAPI
from fastapi.security import HTTPBearer
from src.api.cases import router as cases_router
from src.utils.logger import setup_logging
from starlette.responses import RedirectResponse

setup_logging()
logger = logging.getLogger(__name__)

logger.info("Initializing App")

app = FastAPI(title="Legal assistant service")


bearer_scheme = HTTPBearer()
app.include_router(cases_router.router)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
