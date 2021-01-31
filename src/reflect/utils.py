import os
from pathlib import Path
import logging
from urllib.parse import parse_qs, urlparse
from typing import Dict

logger = logging.getLogger("reflect-app")


def get_file(name: str) -> str:
    return os.path.join(Path(__file__).parent, name)


def _get_query_params(url: str) -> Dict:
    return parse_qs(urlparse(url).query)
