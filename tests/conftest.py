"""Pytest configuration and fixtures."""

from collections.abc import Generator
import os
from typing import Any

from dotenv import load_dotenv
import pytest

# Load test environment
load_dotenv(".env.test")


@pytest.fixture(scope="session")
def test_env() -> dict[str, str]:
    """Provide test environment variables."""
    return {
        "N8N_PORT": "5678",
        "N8N_PROTOCOL": "http",
        "N8N_BASIC_AUTH_ACTIVE": "true",
        "N8N_BASIC_AUTH_USER": "test_user",
        "N8N_BASIC_AUTH_PASSWORD": "test_password",
        "N8N_ENCRYPTION_KEY": "test_encryption_key_32_chars__",
        "N8N_JWT_SECRET": "test_jwt_secret_key",
        "DB_TYPE": "postgresdb",
        "DB_POSTGRESDB_HOST": "localhost",
        "DB_POSTGRESDB_PORT": "5432",
        "DB_POSTGRESDB_DATABASE": "n8n_test",
        "DB_POSTGRESDB_USER": "test_user",
        "DB_POSTGRESDB_PASSWORD": "test_password",
    }


@pytest.fixture(autouse=True)
def setup_test_env(test_env: dict[str, str]) -> Generator[None, None, None]:
    """Setup test environment variables."""
    old_environ = dict(os.environ)
    os.environ.update(test_env)
    yield
    os.environ.clear()
    os.environ.update(old_environ)


@pytest.fixture
def mock_n8n_url() -> str:
    """Provide mock n8n URL."""
    return "http://localhost:5678"


@pytest.fixture
def sample_workflow() -> dict[str, Any]:
    """Provide sample workflow data."""
    return {
        "id": "1",
        "name": "Test Workflow",
        "active": True,
        "nodes": [],
        "connections": {},
    }


@pytest.fixture
def sample_execution() -> dict[str, Any]:
    """Provide sample execution data."""
    return {
        "id": "exec_1",
        "finished": True,
        "mode": "manual",
        "startedAt": "2025-12-29T10:00:00.000Z",
        "stoppedAt": "2025-12-29T10:00:05.000Z",
        "workflowId": "1",
    }
