import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"


@pytest.fixture(scope="session")
def repo_root():
    return REPO_ROOT


@pytest.fixture(scope="session")
def baseline_population():
    return 1_499_549


@pytest.fixture(scope="session")
def population_projections_json():
    with (DATA_DIR / "population_projections.json").open() as f:
        return json.load(f)


@pytest.fixture(scope="session")
def infrastructure_analysis_json():
    with (DATA_DIR / "infrastructure_analysis.json").open() as f:
        return json.load(f)


@pytest.fixture(scope="session")
def sources_json():
    with (DATA_DIR / "sources.json").open() as f:
        return json.load(f)
