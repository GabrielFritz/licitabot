#!/usr/bin/env python3
"""
Test runner for PNCP Ingestion Service.
Runs all tests in the tests folder.
Expects PostgreSQL and RabbitMQ to be running via docker-compose.
"""

import os
import sys
import subprocess
import asyncio
import importlib.util
from pathlib import Path

# Add the ingestor directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ingestor"))


def run_python_test(test_file: str) -> bool:
    """Run a Python test file and return success status."""
    print(f"\n🧪 Running {test_file}...")
    print("=" * 50)

    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(test_file),
        )

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status}: {test_file}")

        return success

    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False


async def run_async_test(test_file: str) -> bool:
    """Run an async Python test file and return success status."""
    print(f"\n🧪 Running {test_file}...")
    print("=" * 50)

    try:
        # Import and run the async test
        spec = importlib.util.spec_from_file_location("test_module", test_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "main"):
            await module.main()
            print(f"\n✅ PASSED: {test_file}")
            return True
        else:
            print(f"\n❌ FAILED: {test_file} - no main() function found")
            return False

    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 PNCP Ingestion Service - Test Suite")
    print("=" * 50)
    print("💡 Make sure PostgreSQL and RabbitMQ are running:")
    print("   docker-compose up -d postgres rabbitmq")
    print()

    # Get the tests directory
    tests_dir = Path(__file__).parent
    test_files = []

    # Find all test files
    for test_file in tests_dir.glob("test_*.py"):
        if test_file.name != "run_all_tests.py":
            test_files.append(str(test_file))

    print(f"Found {len(test_files)} test files:")
    for test_file in test_files:
        print(f"  - {Path(test_file).name}")

    # Run tests
    results = []

    for test_file in test_files:
        if "test_local.py" in test_file or "test_rabbitmq.py" in test_file:
            # These are async tests that require RabbitMQ
            success = asyncio.run(run_async_test(test_file))
        else:
            # These are sync tests (including database tests)
            success = run_python_test(test_file)

        results.append((test_file, success))

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)

    passed = 0
    failed = 0

    for test_file, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {Path(test_file).name}")
        if success:
            passed += 1
        else:
            failed += 1

    print(f"\n📈 Total: {len(results)} tests")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")

    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed!")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
