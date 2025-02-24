import pytest
from llama_index.llms.gemini import Gemini
from llama_index.llms.openai import OpenAI

from src.engine.llm_client_factory import PlatformType, get_client


@pytest.mark.parametrize("platform_type, expected_client_type", [
    (PlatformType.OPENAI, OpenAI),
    (PlatformType.Gemini, Gemini)
])
def test_llm_client_creation(platform_type, expected_client_type):
    client = get_client(platform=platform_type)

    assert client is not None
    assert isinstance(client, expected_client_type)
