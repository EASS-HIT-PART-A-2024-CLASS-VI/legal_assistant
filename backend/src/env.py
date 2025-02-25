from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

config = SettingsConfigDict(env_file=".env", protected_namespaces=("settings_",), extra="allow")


class Config(BaseSettings):
    openai_api_key: str = Field(..., description="API key for accessing the OpenAI API.")
    falkordb_host: str = Field(default="localhost", description="Host for connecting to the FalkorDB instance.")
    falkordb_rag_uri: str = Field(description="URI for connecting to the FalkorDB instance.")
    falkordb_password: str = Field(..., description="Password for authenticating with FalkorDB.")
    model_config = config


configuration = Config()
