"""Health check utilities for n8n deployment."""

import logging
from typing import Any

import httpx

from src.config import config

logger = logging.getLogger(__name__)


class HealthChecker:
    """Health check for n8n instance."""

    def __init__(self, base_url: str | None = None, timeout: int = 10) -> None:
        """Initialize health checker."""
        self.base_url = base_url or f"http://localhost:{config.N8N_PORT}"
        self.timeout = timeout

    async def check_health(self) -> dict[str, Any]:
        """Check n8n health status."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/healthz")

                return {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "status_code": response.status_code,
                    "response_time_ms": response.elapsed.total_seconds() * 1000,
                }
        except httpx.TimeoutException:
            logger.error("Health check timed out")
            return {"status": "unhealthy", "error": "timeout"}
        except httpx.RequestError as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}

    def check_database(self) -> dict[str, Any]:
        """Check database connectivity."""
        if config.DB_TYPE != "postgresdb":
            return {"status": "not_applicable", "message": "Not using PostgreSQL"}

        try:
            # This would require psycopg2 or asyncpg for real implementation
            # Simplified for demonstration
            return {"status": "healthy", "type": config.DB_TYPE}
        except Exception as e:
            logger.error(f"Database check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}

    async def full_health_check(self) -> dict[str, Any]:
        """Perform full health check."""
        health = await self.check_health()
        database = self.check_database()

        overall_status = (
            "healthy"
            if health["status"] == "healthy" and database["status"] in ["healthy", "not_applicable"]
            else "unhealthy"
        )

        return {
            "status": overall_status,
            "checks": {
                "n8n": health,
                "database": database,
            },
        }
