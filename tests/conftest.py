import pytest
import json
from pathlib import Path

DATA_DIRECTORY = Path(__file__).parent / "data"

@pytest.fixture()
def load_json_txt():
    def wrapper(file_name):
        path = DATA_DIRECTORY / file_name
        with open(path, encoding='UTF-8') as f:
            if path.suffix == ".json":
                return json.load(f)
            elif path.suffix == ".txt":
                return f.read()
            else:
                raise ValueError("Unsupported file format")
    return wrapper
