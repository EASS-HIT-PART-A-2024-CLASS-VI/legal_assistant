import logging
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from starlette.responses import RedirectResponse

from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

logger.info("Initializing App")

app = FastAPI(title="Legal assistant service")


bearer_scheme = HTTPBearer()


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
