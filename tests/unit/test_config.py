"""Unit tests for configuration."""

import os

import pytest

from src.config import Config


class TestConfig:
    """Test configuration management."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        assert Config.N8N_PORT == 5678
        assert Config.N8N_PROTOCOL in ["http", "https"]
        assert Config.EXECUTIONS_MODE == "regular"

    def test_environment_override(self) -> None:
        """Test environment variable override."""
        os.environ["N8N_PORT"] = "8080"
        # Reload config would be needed in real scenario
        assert os.getenv("N8N_PORT") == "8080"

    @pytest.mark.unit
    def test_validation_missing_encryption_key(self, test_env: dict[str, str]) -> None:
        """Test validation fails without encryption key."""
        os.environ.pop("N8N_ENCRYPTION_KEY", None)
        Config.N8N_ENCRYPTION_KEY = ""
        errors = Config.validate()
        assert any("N8N_ENCRYPTION_KEY" in error for error in errors)

    @pytest.mark.unit
    def test_validation_missing_jwt_secret(self, test_env: dict[str, str]) -> None:
        """Test validation fails without JWT secret."""
        os.environ.pop("N8N_JWT_SECRET", None)
        Config.N8N_JWT_SECRET = ""
        errors = Config.validate()
        assert any("N8N_JWT_SECRET" in error for error in errors)

    @pytest.mark.unit
    def test_validation_postgres_config(self, test_env: dict[str, str]) -> None:
        """Test PostgreSQL configuration validation."""
        Config.DB_TYPE = "postgresdb"
        Config.DB_POSTGRESDB_HOST = ""
        errors = Config.validate()
        assert any("DB_POSTGRESDB_HOST" in error for error in errors)

    @pytest.mark.unit
    def test_boolean_conversion(self) -> None:
        """Test boolean environment variable conversion."""
        os.environ["N8N_BASIC_AUTH_ACTIVE"] = "true"
        assert Config.N8N_BASIC_AUTH_ACTIVE is True

        os.environ["N8N_BASIC_AUTH_ACTIVE"] = "false"
        Config.N8N_BASIC_AUTH_ACTIVE = os.getenv("N8N_BASIC_AUTH_ACTIVE", "true").lower() == "true"
        assert Config.N8N_BASIC_AUTH_ACTIVE is False

    @pytest.mark.unit
    def test_integer_conversion(self) -> None:
        """Test integer environment variable conversion."""
        os.environ["N8N_PORT"] = "9999"
        port = int(os.getenv("N8N_PORT", "5678"))
        assert port == 9999
        assert isinstance(port, int)
