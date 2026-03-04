#!/usr/bin/env python3
"""
Test script to demonstrate source overwrite behavior.
"""
import sys
from pathlib import Path

# Add the package to path
sys.path.insert(0, str(Path(__file__).parent))

from well_log_toolkit import WellDataManager


def test_overwrite_behavior():
    """Test that loading the same source twice overwrites with notification."""
    print("=" * 60)
    print("Test: Source Overwrite Behavior")
    print("=" * 60)

    manager = WellDataManager()

    import glob
    files = glob.glob('WellData/*')[:2]  # Get first 2 files

    if len(files) < 2:
        print("Need at least 2 LAS files in WellData/ directory")
        return False

    # Load first file
    print(f"\n1. Loading first file: {files[0]}")
    manager.load_las(files[0])

    print(f"\nWells: {manager.wells}")
    if manager.wells:
        well_name = manager.wells[0]
        well = getattr(manager, well_name)
        print(f"Well: {well.name}")
        print(f"Sources: {well.sources}")
        initial_source_count = len(well.sources)

        # Load the same file again - should overwrite
        print(f"\n2. Loading same file again: {files[0]}")
        print("   (Expect overwrite notification below)")
        manager.load_las(files[0])

        print(f"\nWell: {well.name}")
        print(f"Sources: {well.sources}")
        after_reload_count = len(well.sources)

        # Verify source count didn't increase
        if initial_source_count != after_reload_count:
            print(f"\n✗ Source count changed! Expected {initial_source_count}, got {after_reload_count}")
            return False

        print(f"\n✓ Source count unchanged ({after_reload_count}), overwrite successful!")

        # Load second file with different data
        print(f"\n3. Loading different file: {files[1]}")
        manager.load_las(files[1])

        print(f"\nWells: {manager.wells}")
        for wn in manager.wells:
            w = getattr(manager, wn)
            print(f"  {w.name}: {len(w.sources)} sources")

        return True

    return False


def test_external_df_overwrite():
    """Test that adding external DataFrames overwrites properly."""
    print("\n" + "=" * 60)
    print("Test: External DataFrame Overwrite")
    print("=" * 60)

    import pandas as pd

    manager = WellDataManager()

    import glob
    files = glob.glob('WellData/*')[:1]

    if not files:
        print("Need at least 1 LAS file in WellData/ directory")
        return False

    manager.load_las(files[0])

    if not manager.wells:
        return False

    well_name = manager.wells[0]
    well = getattr(manager, well_name)

    print(f"\nWell: {well.name}")
    print(f"Initial sources: {well.sources}")

    # Add first DataFrame
    df1 = pd.DataFrame({
        'DEPT': [2800, 2801, 2802],
        'TEST_PROP': [1.0, 2.0, 3.0]
    })

    print("\n1. Adding first external DataFrame...")
    well.add_dataframe(df1, unit_mappings={'TEST_PROP': 'v/v'})
    print(f"Sources: {well.sources}")
    source_count_1 = len(well.sources)

    # Add second DataFrame - should overwrite 'external_df'
    df2 = pd.DataFrame({
        'DEPT': [2800, 2801, 2802],
        'NEW_PROP': [4.0, 5.0, 6.0]
    })

    print("\n2. Adding second external DataFrame...")
    print("   (Expect overwrite notification below)")
    well.add_dataframe(df2, unit_mappings={'NEW_PROP': 'fraction'})
    print(f"Sources: {well.sources}")
    source_count_2 = len(well.sources)

    # Verify source count didn't increase
    if source_count_1 != source_count_2:
        print(f"\n✗ Source count changed! Expected {source_count_1}, got {source_count_2}")
        return False

    print(f"\n✓ Source count unchanged ({source_count_2}), overwrite successful!")

    # Verify new property exists and old one doesn't
    try:
        prop = well.external_df.NEW_PROP
        print(f"✓ New property 'NEW_PROP' found in external_df source")
    except AttributeError:
        print("✗ New property 'NEW_PROP' not found!")
        return False

    try:
        prop = well.external_df.TEST_PROP
        print("✗ Old property 'TEST_PROP' still exists (should have been overwritten)!")
        return False
    except AttributeError:
        print("✓ Old property 'TEST_PROP' correctly removed after overwrite")

    return True


def main():
    """Run all tests."""
    print("Testing Source Overwrite Behavior")
    print("=" * 60)

    tests = [
        test_overwrite_behavior,
        test_external_df_overwrite
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
                print(f"\n✓ {test.__name__} PASSED")
            else:
                failed += 1
                print(f"\n✗ {test.__name__} FAILED")
        except Exception as e:
            failed += 1
            print(f"\n✗ {test.__name__} FAILED with exception:")
            print(f"  {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"Tests: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
