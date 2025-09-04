import json
from enum import Enum
from pathlib import Path
import pytest
import yaml

DATA_DIRECTORY = Path(__file__).parent / "data"


def _load_file(file_name):
    if isinstance(file_name, Enum):
        file_name = file_name.value
    path = DATA_DIRECTORY / file_name
    with open(path, encoding='UTF-8') as f:
        if path.suffix == ".json":
            return json.load(f)
        elif path.suffix == ".txt":
            return f.read()
        elif path.suffix in (".yaml", ".yml"):
            return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported file format")



@pytest.fixture(scope='session')
def test_data():
    data = {}
    for file in DATA_DIRECTORY.iterdir():
        data[file.name] = _load_file(file)
    return data
