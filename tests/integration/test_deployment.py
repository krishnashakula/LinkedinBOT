"""Integration tests for deployment."""

import pytest


class TestDeployment:
    """Test deployment scenarios."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_docker_build(self) -> None:
        """Test Docker build process."""
        # This would test actual Docker build in CI/CD
        # Placeholder for real implementation
        from pathlib import Path

        project_root = Path(__file__).parent.parent.parent
        dockerfile = project_root / "Dockerfile"
        assert dockerfile.exists(), "Dockerfile must exist for Docker build"

    @pytest.mark.integration
    def test_environment_variables_loaded(self, test_env: dict[str, str]) -> None:
        """Test environment variables are loaded."""
        from src.config import Config

        assert Config.N8N_PORT == 5678
        assert Config.N8N_ENCRYPTION_KEY == "test_encryption_key_32_chars__"

    @pytest.mark.integration
    def test_railway_config_exists(self) -> None:
        """Test Railway configuration files exist."""
        from pathlib import Path

        project_root = Path(__file__).parent.parent.parent
        assert (project_root / "railway.json").exists()
        assert (project_root / "railway.toml").exists()
        assert (project_root / "Dockerfile").exists()

    @pytest.mark.integration
    def test_docker_compose_valid(self) -> None:
        """Test docker-compose.yml is valid."""
        from pathlib import Path

        import yaml

        project_root = Path(__file__).parent.parent.parent
        compose_file = project_root / "docker-compose.yml"

        assert compose_file.exists()

        with compose_file.open() as f:
            compose_config = yaml.safe_load(f)

        assert "services" in compose_config
        assert "n8n" in compose_config["services"]
        assert "postgres" in compose_config["services"]
        assert "redis" in compose_config["services"]
