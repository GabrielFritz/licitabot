#!/usr/bin/env python3
"""
Test script for PNCP ingestion service utilities.
"""

import sys
import os

# Add the ingestor directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ingestor"))

# Import from the utils.py file, not the utils package
import ingestor.utils.ingestor_utils as utils


def test_parse_numero_controle():
    """Test the parse_numero_controle function."""
    test_cases = [
        ("07854402000100-1-000054/2025", ("07854402000100", "2025", "000054")),
        ("12345678901234-1-000001/2024", ("12345678901234", "2024", "000001")),
    ]

    print("Testing parse_numero_controle...")
    for input_str, expected in test_cases:
        try:
            result = utils.parse_numero_controle(input_str)
            if result == expected:
                print(f"✓ {input_str} → {result}")
            else:
                print(f"✗ {input_str} → {result} (expected {expected})")
        except Exception as e:
            print(f"✗ {input_str} → Error: {e}")


def test_iso_to_ymd():
    """Test the iso_to_ymd function."""
    test_cases = [
        ("2025-01-10T12:00:00", "20250110"),
        ("2024-12-31T23:59:59", "20241231"),
    ]

    print("\nTesting iso_to_ymd...")
    for input_str, expected in test_cases:
        try:
            result = utils.iso_to_ymd(input_str)
            if result == expected:
                print(f"✓ {input_str} → {result}")
            else:
                print(f"✗ {input_str} → {result} (expected {expected})")
        except Exception as e:
            print(f"✗ {input_str} → Error: {e}")


def test_validate_iso_date():
    """Test the validate_iso_date function."""
    test_cases = [
        ("2025-01-10T12:00:00", True),
        ("2024-12-31T23:59:59", True),
        ("invalid-date", False),
        ("2025-13-01T12:00:00", False),  # Invalid month
    ]

    print("\nTesting validate_iso_date...")
    for input_str, expected in test_cases:
        result = utils.validate_iso_date(input_str)
        if result == expected:
            print(f"✓ {input_str} → {result}")
        else:
            print(f"✗ {input_str} → {result} (expected {expected})")


if __name__ == "__main__":
    print("🧪 Testing PNCP Ingestion Service Utils\n")

    test_parse_numero_controle()
    test_iso_to_ymd()
    test_validate_iso_date()

    print("\n✅ All tests completed!")
