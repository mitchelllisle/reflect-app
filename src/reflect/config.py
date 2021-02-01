from pydantic import BaseSettings, SecretStr, Field
from reflect.utils import get_file
import json


class MySQLConfig(BaseSettings):
    HOST: str = Field(..., env="DB_HOST")
    PORT: str = Field(..., env="DB_PORT")
    USERNAME: SecretStr = Field(..., env="DB_USERNAME")
    PASSWORD: SecretStr = Field(..., env="DB_PASSWORD")
    DATABASE: str = Field(..., env="DB")

    DB_POOL_SIZE: int = Field(
        default=10,
        env="DB_POOL_SIZE",
        description="The number of connections we'll open and reserve for project tasks"
    )
    RUN_MIGRATIONS: bool = Field(default=True, env="RUN_MIGRATIONS")
    MIGRATIONS_FILE: str = Field(default="migrations/projects.sql", env="MIGRATIONS_FILE")


class ColourConfig:
    primary = "#50E3C2"
    secondary = "#F8F9F9"
    orange = "#FEB33A"
    dark = "#292123"
    highlight = "#BFADFD"

    good = "#BFEA53"
    wondering = "#FFC666"
    bad = "#F574A2"

    def __getitem__(self, item):
        return getattr(self, item)


class AssetConfig:
    logo = "/assets/favicon.ico"
    missing = "/assets/404.gif"

    good = "😀"
    wondering = "🤔"
    bad = "😓"

    def __getitem__(self, item):
        return getattr(self, item)


class SemanticProjectNameConfig:
    def __init__(self):
        self.adjectives = self._open_json("assets/data/adjectives.json")
        self.animals = self._open_json("assets/data/animals.json")

    @staticmethod
    def _open_json(file: str):
        with open(get_file(file)) as f:
            data = json.load(f)
        return data


class DashConfig(BaseSettings):
    debug: bool = Field(env="DEBUG", default=False)


class AppConfig:
    mysql = MySQLConfig()
    colour = ColourConfig()
    assets = AssetConfig()
    semantic_naming = SemanticProjectNameConfig()
    dash = DashConfig()
