import json
import os
import pytest
from src.config_manager import load_config, save_config


@pytest.fixture
def config_path(tmp_path):
    return str(tmp_path / "config.json")


@pytest.fixture
def sample_config():
    return {
        "visit_schedule_path": "C:/Users/test/VisitSchedule.xlsx",
        "vendor_directory_path": "C:/Users/test/VendorDirectory.xlsx",
        "user_email": "test@digitalrealty.com",
    }


def test_save_creates_file(config_path, sample_config):
    save_config(sample_config, config_path)
    assert os.path.exists(config_path)


def test_save_and_load_roundtrip(config_path, sample_config):
    save_config(sample_config, config_path)
    loaded = load_config(config_path)
    assert loaded == sample_config


def test_load_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent/config.json")


def test_save_overwrites_existing(config_path, sample_config):
    save_config(sample_config, config_path)
    updated = sample_config.copy()
    updated["user_email"] = "new@digitalrealty.com"
    save_config(updated, config_path)
    loaded = load_config(config_path)
    assert loaded["user_email"] == "new@digitalrealty.com"