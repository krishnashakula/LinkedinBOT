"""Unit tests for health check."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.health_check import HealthChecker


class TestHealthChecker:
    """Test health check functionality."""

    @pytest.fixture
    def health_checker(self, mock_n8n_url: str) -> HealthChecker:
        """Create health checker instance."""
        return HealthChecker(base_url=mock_n8n_url, timeout=5)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_health_check_success(self, health_checker: HealthChecker) -> None:
        """Test successful health check."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.05

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_instance.get = AsyncMock(return_value=mock_response)
            mock_client.return_value = mock_instance

            result = await health_checker.check_health()

            assert result["status"] == "healthy"
            assert result["status_code"] == 200
            assert "response_time_ms" in result

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self, health_checker: HealthChecker) -> None:
        """Test unhealthy status."""
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.elapsed.total_seconds.return_value = 0.1

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_instance.get = AsyncMock(return_value=mock_response)
            mock_client.return_value = mock_instance

            result = await health_checker.check_health()

            assert result["status"] == "unhealthy"
            assert result["status_code"] == 503

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_health_check_timeout(self, health_checker: HealthChecker) -> None:
        """Test health check timeout."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_instance.get = AsyncMock(side_effect=httpx.TimeoutException("Timeout"))
            mock_client.return_value = mock_instance

            result = await health_checker.check_health()

            assert result["status"] == "unhealthy"
            assert result["error"] == "timeout"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_health_check_request_error(self, health_checker: HealthChecker) -> None:
        """Test health check request error."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_instance.get = AsyncMock(
                side_effect=httpx.RequestError("Connection error")
            )
            mock_client.return_value = mock_instance

            result = await health_checker.check_health()

            assert result["status"] == "unhealthy"
            assert "error" in result

    @pytest.mark.unit
    def test_database_check_not_postgres(self, health_checker: HealthChecker) -> None:
        """Test database check when not using PostgreSQL."""
        with patch("src.config.config.DB_TYPE", "sqlite"):
            result = health_checker.check_database()

            assert result["status"] == "not_applicable"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_full_health_check(self, health_checker: HealthChecker) -> None:
        """Test full health check."""
        with patch.object(
            health_checker, "check_health", return_value={"status": "healthy"}
        ), patch.object(
            health_checker, "check_database", return_value={"status": "healthy"}
        ):
            result = await health_checker.full_health_check()

            assert result["status"] == "healthy"
            assert "checks" in result
            assert "n8n" in result["checks"]
            assert "database" in result["checks"]
