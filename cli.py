#!/usr/bin/env python3
"""CLI for n8n Railway deployment management."""

import argparse
import asyncio
import sys
from pathlib import Path

from src.config import Config
from src.health_check import HealthChecker


def setup_parser() -> argparse.ArgumentParser:
    """Setup CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="n8n Railway Deployment CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Health check command
    health_parser = subparsers.add_parser("health", help="Check n8n health status")
    health_parser.add_argument(
        "--url", type=str, help="n8n base URL (default: from config)"
    )
    health_parser.add_argument(
        "--timeout", type=int, default=10, help="Timeout in seconds (default: 10)"
    )

    # Config validation command
    subparsers.add_parser("validate", help="Validate configuration")

    # Environment info command
    subparsers.add_parser("info", help="Display environment information")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument(
        "--unit", action="store_true", help="Run only unit tests"
    )
    test_parser.add_argument(
        "--integration", action="store_true", help="Run only integration tests"
    )
    test_parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report"
    )

    # Lint command
    lint_parser = subparsers.add_parser("lint", help="Run linter")
    lint_parser.add_argument("--fix", action="store_true", help="Auto-fix issues")

    # Format command
    subparsers.add_parser("format", help="Format code")

    return parser


async def health_command(args: argparse.Namespace) -> int:
    """Execute health check command."""
    print("🏥 Checking n8n health...")
    print("=" * 60)

    checker = HealthChecker(base_url=args.url, timeout=args.timeout)

    try:
        result = await checker.full_health_check()

        print(f"\nOverall Status: {result['status'].upper()}")
        print("\nChecks:")

        for check_name, check_result in result["checks"].items():
            status = check_result.get("status", "unknown")
            emoji = "✅" if status == "healthy" else "❌" if status == "unhealthy" else "ℹ️"
            print(f"  {emoji} {check_name}: {status}")

            if "error" in check_result:
                print(f"     Error: {check_result['error']}")
            if "response_time_ms" in check_result:
                print(f"     Response time: {check_result['response_time_ms']:.2f}ms")

        return 0 if result["status"] == "healthy" else 1

    except Exception as e:
        print(f"\n❌ Health check failed: {e}")
        return 1


def validate_command() -> int:
    """Execute config validation command."""
    print("✅ Validating configuration...")
    print("=" * 60)

    errors = Config.validate()

    if not errors:
        print("\n✅ Configuration is valid!")
        print("\nKey Settings:")
        print(f"  • Port: {Config.N8N_PORT}")
        print(f"  • Protocol: {Config.N8N_PROTOCOL}")
        print(f"  • Database: {Config.DB_TYPE}")
        print(f"  • Auth Active: {Config.N8N_BASIC_AUTH_ACTIVE}")
        print(f"  • Execution Mode: {Config.EXECUTIONS_MODE}")
        print(f"  • Log Level: {Config.N8N_LOG_LEVEL}")
        return 0
    else:
        print("\n❌ Configuration errors found:\n")
        for error in errors:
            print(f"  • {error}")
        return 1


def info_command() -> int:
    """Display environment information."""
    print("ℹ️  n8n Railway Deployment Information")
    print("=" * 60)

    print("\n📋 Configuration:")
    print(f"  • N8N Port: {Config.N8N_PORT}")
    print(f"  • N8N Protocol: {Config.N8N_PROTOCOL}")
    print(f"  • Webhook URL: {Config.WEBHOOK_URL or 'Not set'}")
    print(f"  • Database Type: {Config.DB_TYPE}")
    print(f"  • Database Host: {Config.DB_POSTGRESDB_HOST or 'Not set'}")
    print(f"  • Basic Auth: {'Enabled' if Config.N8N_BASIC_AUTH_ACTIVE else 'Disabled'}")
    print(f"  • Execution Mode: {Config.EXECUTIONS_MODE}")
    print(f"  • Timezone: {Config.GENERIC_TIMEZONE}")
    print(f"  • Log Level: {Config.N8N_LOG_LEVEL}")

    if Config.QUEUE_BULL_REDIS_HOST:
        print(f"\n🔴 Redis Queue:")
        print(f"  • Host: {Config.QUEUE_BULL_REDIS_HOST}")
        print(f"  • Port: {Config.QUEUE_BULL_REDIS_PORT}")

    print("\n🔒 Security:")
    print(f"  • Encryption Key: {'✅ Set' if Config.N8N_ENCRYPTION_KEY else '❌ Not set'}")
    print(f"  • JWT Secret: {'✅ Set' if Config.N8N_JWT_SECRET else '❌ Not set'}")
    print(f"  • Secure Cookie: {Config.N8N_SECURE_COOKIE}")

    return 0


def run_tests(args: argparse.Namespace) -> int:
    """Execute test command."""
    import subprocess

    print("🧪 Running tests...")
    print("=" * 60)

    cmd = ["python", "-m", "pytest", "tests/"]

    if args.unit:
        cmd.extend(["unit/", "-m", "unit"])
    elif args.integration:
        cmd.extend(["integration/", "-m", "integration"])

    cmd.append("-v")

    if args.coverage:
        cmd.extend(["--cov=src", "--cov-report=term-missing", "--cov-report=html"])

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        return 1


def run_lint(args: argparse.Namespace) -> int:
    """Execute lint command."""
    import subprocess

    print("🔍 Running linter...")
    print("=" * 60)

    cmd = ["python", "-m", "ruff", "check", "src/", "tests/"]

    if args.fix:
        cmd.append("--fix")

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"\n❌ Linter execution failed: {e}")
        return 1


def run_format() -> int:
    """Execute format command."""
    import subprocess

    print("🎨 Formatting code...")
    print("=" * 60)

    commands = [
        ["python", "-m", "ruff", "format", "src/", "tests/"],
        ["python", "-m", "ruff", "check", "--fix", "src/", "tests/"],
    ]

    for cmd in commands:
        try:
            result = subprocess.run(cmd, check=False)
            if result.returncode != 0:
                return result.returncode
        except Exception as e:
            print(f"\n❌ Format execution failed: {e}")
            return 1

    print("\n✅ Code formatted successfully!")
    return 0


def main() -> int:
    """Main CLI entry point."""
    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "health":
            return asyncio.run(health_command(args))
        elif args.command == "validate":
            return validate_command()
        elif args.command == "info":
            return info_command()
        elif args.command == "test":
            return run_tests(args)
        elif args.command == "lint":
            return run_lint(args)
        elif args.command == "format":
            return run_format()
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
