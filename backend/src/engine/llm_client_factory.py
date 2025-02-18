from enum import Enum

from llama_index.embeddings.openai import OpenAIEmbeddingMode
from src.env import configuration


class PlatformType(Enum):
    Gemini = "gemini"
    OPENAI = "openai"


PLATFORM_MODELS = {
    PlatformType.Gemini: {
        "default_embedding": {"model_name": "models/embedding-001"},
        "default_chat": {"model_name": "models/gemini-1.5-flash", "temperature": 0.0, "max_tokens": 2000},
    },
    PlatformType.OPENAI: {
        "default_embedding": {"model_name": "text-embedding-3-large", "model_mode": OpenAIEmbeddingMode.SIMILARITY_MODE, "dimensions": 512},
        "default_client": {"model_name": "gpt-3.5-turbo", "temperature": 0.0, "max_tokens": 2000},
    },
}


def get_client(platform: PlatformType = PlatformType.Gemini):
    client_conf = PLATFORM_MODELS.get(platform, {})["default_client"]
    match platform:
        case PlatformType.Gemini:
            return __get_gemini_client(model_name=client_conf["model_name"], temperature=client_conf["temperature"], max_tokens=client_conf["max_tokens"])
        case PlatformType.OPENAI:
            return __get_openai_client(model_name=client_conf["model_name"], temperature=client_conf["temperature"], max_tokens=client_conf["max_tokens"])
        case _:
            raise Exception(f"Type platform client - {platform} is not supported")


def get_embedding_client(platform: PlatformType = PlatformType.Gemini):
    embedding_conf = PLATFORM_MODELS.get(platform, {})["default_embedding"]
    match platform:
        case PlatformType.Gemini:
            return __get_gemini_embedding(model_name=embedding_conf["model_name"])
        case PlatformType.OPENAI:
            return __get_openai_embedding(model_name=embedding_conf["model_name"], model_mode=embedding_conf["model_mode"], dimensions=embedding_conf["dimensions"])
        case _:
            raise Exception(f"Type platform embedding - {platform} is not supported")


def __get_gemini_embedding(model_name: str):
    from llama_index.embeddings.gemini import GeminiEmbedding

    return GeminiEmbedding(model_name=model_name, api_key=configuration.gemini_key)


def __get_gemini_client(model_name: str, temperature: float, max_tokens: int):
    from llama_index.llms.gemini import Gemini

    return Gemini(model=model_name, api_key=configuration.gemini_key, temperature=temperature, max_tokens=max_tokens)


def __get_openai_embedding(model_name: str, model_mode: str, dimensions: int):
    from llama_index.embeddings.openai import OpenAIEmbedding

    return OpenAIEmbedding(model=model_name, mode=model_mode, dimensions=dimensions, api_key=configuration.openai.api_key)


def __get_openai_client(model_name: str, temperature: float, max_tokens: int):
    from llama_index.llms.openai import OpenAI

    return OpenAI(model=model_name, api_key=configuration.openai_api_key, temperature=temperature, max_tokens=max_tokens)
