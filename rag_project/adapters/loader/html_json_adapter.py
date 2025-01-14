
from bs4 import BeautifulSoup
import json
from typing import Any


def extract_html_text(file_path: str) -> Any:
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, "html.parser")
    return soup.get_text()


def extract_json_text(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: Any = json.load(file)
    return json.dumps(data, indent=2)
