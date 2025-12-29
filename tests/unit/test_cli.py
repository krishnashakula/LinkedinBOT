"""Unit tests for CLI."""

import argparse
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cli import (
    health_command,
    info_command,
    run_format,
    run_lint,
    run_tests,
    setup_parser,
    validate_command,
)


class TestCLIParser:
    """Test CLI argument parser."""

    @pytest.mark.unit
    def test_parser_setup(self) -> None:
        """Test parser is set up correctly."""
        parser = setup_parser()
        assert parser is not None
        assert isinstance(parser, argparse.ArgumentParser)

    @pytest.mark.unit
    def test_health_command_args(self) -> None:
        """Test health command arguments."""
        parser = setup_parser()
        args = parser.parse_args(["health", "--url", "http://localhost:5678", "--timeout", "5"])
        assert args.command == "health"
        assert args.url == "http://localhost:5678"
        assert args.timeout == 5

    @pytest.mark.unit
    def test_test_command_args(self) -> None:
        """Test test command arguments."""
        parser = setup_parser()
        args = parser.parse_args(["test", "--unit", "--coverage"])
        assert args.command == "test"
        assert args.unit is True
        assert args.coverage is True

    @pytest.mark.unit
    def test_lint_command_args(self) -> None:
        """Test lint command arguments."""
        parser = setup_parser()
        args = parser.parse_args(["lint", "--fix"])
        assert args.command == "lint"
        assert args.fix is True


class TestCLICommands:
    """Test CLI commands."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_health_command_success(self) -> None:
        """Test health command with healthy status."""
        args = argparse.Namespace(url=None, timeout=10)

        mock_result = {
            "status": "healthy",
            "checks": {
                "n8n": {"status": "healthy", "response_time_ms": 50.0},
                "database": {"status": "healthy"},
            },
        }

        with patch("cli.HealthChecker") as mock_checker:
            mock_instance = MagicMock()
            mock_instance.full_health_check = AsyncMock(return_value=mock_result)
            mock_checker.return_value = mock_instance

            result = await health_command(args)
            assert result == 0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_health_command_unhealthy(self) -> None:
        """Test health command with unhealthy status."""
        args = argparse.Namespace(url=None, timeout=10)

        mock_result = {
            "status": "unhealthy",
            "checks": {
                "n8n": {"status": "unhealthy", "error": "Connection failed"},
            },
        }

        with patch("cli.HealthChecker") as mock_checker:
            mock_instance = MagicMock()
            mock_instance.full_health_check = AsyncMock(return_value=mock_result)
            mock_checker.return_value = mock_instance

            result = await health_command(args)
            assert result == 1

    @pytest.mark.unit
    def test_validate_command_success(self) -> None:
        """Test validate command with valid config."""
        with patch("cli.Config.validate", return_value=[]):
            result = validate_command()
            assert result == 0

    @pytest.mark.unit
    def test_validate_command_errors(self) -> None:
        """Test validate command with config errors."""
        with patch("cli.Config.validate", return_value=["Error 1", "Error 2"]):
            result = validate_command()
            assert result == 1

    @pytest.mark.unit
    def test_info_command(self) -> None:
        """Test info command."""
        result = info_command()
        assert result == 0

    @pytest.mark.unit
    def test_run_tests_command(self) -> None:
        """Test test command execution."""
        args = argparse.Namespace(unit=True, integration=False, coverage=False)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = run_tests(args)
            assert result == 0
            mock_run.assert_called_once()

    @pytest.mark.unit
    def test_run_lint_command(self) -> None:
        """Test lint command execution."""
        args = argparse.Namespace(fix=False)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = run_lint(args)
            assert result == 0
            mock_run.assert_called_once()

    @pytest.mark.unit
    def test_run_format_command(self) -> None:
        """Test format command execution."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = run_format()
            assert result == 0
            assert mock_run.call_count == 2
