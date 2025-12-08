import pytest
import os
import shutil
from pathlib import Path

@pytest.fixture(autouse=True)
def test_json_env(tmp_path):
    source = Path(__file__).parent / "data"
    assert source.exists(), f"Source folder {source} does not exist"

    test_data = tmp_path / "json"
    test_data.mkdir()
    for file in source.glob("*.json"):
        shutil.copy(file, test_data / file.name)

    os.environ["JSON_PATH"] = str(test_data)

    yield