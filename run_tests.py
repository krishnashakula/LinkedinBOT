#!/usr/bin/env python3
"""Quick start script for testing."""

import subprocess
import sys


def run_command(command: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}\n")

    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"✅ {description} - SUCCESS\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e}\n")
        return False


def main() -> int:
    """Run all tests and checks."""
    print("\n" + "="*60)
    print("🧪 N8N Railway Deployment - Test Suite")
    print("="*60)

    commands = [
        (["ruff", "check", "src/", "tests/"], "Running Ruff Linter"),
        (["ruff", "format", "--check", "src/", "tests/"], "Checking Code Format"),
        (["pytest", "tests/unit/", "-v", "-m", "unit"], "Running Unit Tests"),
        (["pytest", "tests/", "-v", "--cov=src", "--cov-report=term-missing"], "Running Full Test Suite with Coverage"),
    ]

    results = []
    for command, description in commands:
        results.append(run_command(command, description))

    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)

    total = len(results)
    passed = sum(results)
    failed = total - passed

    print(f"\nTotal: {total} | Passed: ✅ {passed} | Failed: ❌ {failed}\n")

    if all(results):
        print("🎉 All checks passed!")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
