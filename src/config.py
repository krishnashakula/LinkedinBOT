"""Configuration management for n8n deployment."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    # N8N Settings
    N8N_PORT: int = int(os.getenv("N8N_PORT", "5678"))
    N8N_PROTOCOL: str = os.getenv("N8N_PROTOCOL", "https")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")

    # Authentication
    N8N_BASIC_AUTH_ACTIVE: bool = os.getenv("N8N_BASIC_AUTH_ACTIVE", "true").lower() == "true"
    N8N_BASIC_AUTH_USER: str = os.getenv("N8N_BASIC_AUTH_USER", "admin")
    N8N_BASIC_AUTH_PASSWORD: str = os.getenv("N8N_BASIC_AUTH_PASSWORD", "")

    # Database
    DB_TYPE: str = os.getenv("DB_TYPE", "postgresdb")
    DB_POSTGRESDB_HOST: str = os.getenv("DB_POSTGRESDB_HOST", "")
    DB_POSTGRESDB_PORT: int = int(os.getenv("DB_POSTGRESDB_PORT", "5432"))
    DB_POSTGRESDB_DATABASE: str = os.getenv("DB_POSTGRESDB_DATABASE", "n8n")
    DB_POSTGRESDB_USER: str = os.getenv("DB_POSTGRESDB_USER", "")
    DB_POSTGRESDB_PASSWORD: str = os.getenv("DB_POSTGRESDB_PASSWORD", "")

    # Security
    N8N_ENCRYPTION_KEY: str = os.getenv("N8N_ENCRYPTION_KEY", "")
    N8N_JWT_SECRET: str = os.getenv("N8N_JWT_SECRET", "")
    N8N_SECURE_COOKIE: bool = os.getenv("N8N_SECURE_COOKIE", "true").lower() == "true"

    # Execution
    EXECUTIONS_MODE: str = os.getenv("EXECUTIONS_MODE", "regular")
    EXECUTIONS_TIMEOUT: int = int(os.getenv("EXECUTIONS_TIMEOUT", "3600"))
    EXECUTIONS_TIMEOUT_MAX: int = int(os.getenv("EXECUTIONS_TIMEOUT_MAX", "7200"))

    # Redis Queue
    QUEUE_BULL_REDIS_HOST: str | None = os.getenv("QUEUE_BULL_REDIS_HOST")
    _redis_port = os.getenv("QUEUE_BULL_REDIS_PORT")
    QUEUE_BULL_REDIS_PORT: int | None = int(_redis_port) if _redis_port is not None else None
    QUEUE_BULL_REDIS_PASSWORD: str | None = os.getenv("QUEUE_BULL_REDIS_PASSWORD")

    # Logging
    N8N_LOG_LEVEL: str = os.getenv("N8N_LOG_LEVEL", "info")
    N8N_LOG_OUTPUT: str = os.getenv("N8N_LOG_OUTPUT", "console")

    # Timezone
    GENERIC_TIMEZONE: str = os.getenv("GENERIC_TIMEZONE", "UTC")

    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration."""
        errors = []

        if not cls.N8N_ENCRYPTION_KEY:
            errors.append("N8N_ENCRYPTION_KEY is required")

        if not cls.N8N_JWT_SECRET:
            errors.append("N8N_JWT_SECRET is required")

        if cls.N8N_BASIC_AUTH_ACTIVE and not cls.N8N_BASIC_AUTH_PASSWORD:
            errors.append("N8N_BASIC_AUTH_PASSWORD is required when basic auth is active")

        if cls.DB_TYPE == "postgresdb":
            if not cls.DB_POSTGRESDB_HOST:
                errors.append("DB_POSTGRESDB_HOST is required for PostgreSQL")
            if not cls.DB_POSTGRESDB_USER:
                errors.append("DB_POSTGRESDB_USER is required for PostgreSQL")
            if not cls.DB_POSTGRESDB_PASSWORD:
                errors.append("DB_POSTGRESDB_PASSWORD is required for PostgreSQL")

        return errors


config = Config()
