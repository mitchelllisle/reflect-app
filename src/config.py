from pydantic import BaseSettings, SecretStr


class ColourConfig:
    primary = "#50E3C2"
    secondary = "#F8F9F9"
    orange = "#FEB33A"
    dark = "#292123"
    highlight = "#BFADFD"

    good = "#BFEA53"
    wondering = "#FFC666"
    bad = "#F574A2"


class AssetConfig:
    logo = "/assets/logo.png"
    missing = "/assets/404.gif"


class AppConfig:
    # postgres = PostgresConfig()
    colour = ColourConfig()
    assets = AssetConfig()
