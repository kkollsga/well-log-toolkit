"""Tests for LAS 3.0 file support: reading, writing, and roundtrip."""
import numpy as np
import pytest
from pathlib import Path

from logsuite.io import LasFile


@pytest.fixture
def las3_path():
    """Path to the LAS 3.0 test fixture."""
    return Path(__file__).parent / "fixtures" / "test_las3.las"


@pytest.fixture
def las3_file(las3_path):
    """Load the LAS 3.0 test fixture."""
    return LasFile(str(las3_path))


class TestLas3Loading:
    """Tests for loading LAS 3.0 files."""

    def test_version_detected(self, las3_file):
        assert las3_file._las_version == '3.0'
        assert las3_file.version_info['VERS'] == '3.0'

    def test_well_name(self, las3_file):
        assert las3_file.well_info['WELL'] == 'Test-3'

    def test_curves_parsed(self, las3_file):
        assert 'DEPT' in las3_file.curves
        assert 'PHIE' in las3_file.curves
        assert 'SW' in las3_file.curves
        assert len(las3_file.curves) == 3

    def test_curve_units(self, las3_file):
        assert las3_file.curves['DEPT']['unit'] == 'm'
        assert las3_file.curves['PHIE']['unit'] == 'v/v'

    def test_data_loads(self, las3_file):
        df = las3_file.data()
        assert len(df) == 5
        assert list(df.columns) == ['DEPT', 'PHIE', 'SW']

    def test_data_values(self, las3_file):
        df = las3_file.data()
        assert np.isclose(df['DEPT'].iloc[0], 1000.0)
        assert np.isclose(df['PHIE'].iloc[0], 0.20)
        assert np.isclose(df['SW'].iloc[3], 0.35)

    def test_depth_range(self, las3_file):
        df = las3_file.data()
        assert np.isclose(df['DEPT'].min(), 1000.0)
        assert np.isclose(df['DEPT'].max(), 1004.0)


class TestLasFileOpen:
    """Tests for LasFile.open() factory method."""

    def test_open_las3(self, las3_path):
        las = LasFile.open(str(las3_path))
        assert las._las_version == "3.0"
        assert "PHIE" in las.curves

    def test_open_las2(self, tmp_las_file):
        las = LasFile.open(str(tmp_las_file))
        assert las._las_version == "2.0"
        assert "PHIE" in las.curves


class TestLas3Export:
    """Tests for LAS 3.0 export."""

    def test_export_v3_creates_file(self, las3_file, tmp_path):
        las3_file.data()  # Load data first
        out = tmp_path / "out.las"
        las3_file.export(str(out), version="3.0")
        assert out.exists()

    def test_export_v3_section_names(self, las3_file, tmp_path):
        las3_file.data()
        out = tmp_path / "out.las"
        las3_file.export(str(out), version="3.0")
        content = out.read_text()
        assert "~Log_Definition" in content
        assert "~Log_Data" in content
        assert "3.0" in content

    def test_export_v3_tab_separated(self, las3_file, tmp_path):
        las3_file.data()
        out = tmp_path / "out.las"
        las3_file.export(str(out), version="3.0")
        content = out.read_text()
        # Data lines (after ~Log_Data) should be tab-separated
        in_data = False
        for line in content.splitlines():
            if line.startswith("~Log_Data"):
                in_data = True
                continue
            if in_data and line.strip():
                assert "\t" in line
                break

    def test_export_v2_no_tabs(self, las3_file, tmp_path):
        las3_file.data()
        out = tmp_path / "out.las"
        las3_file.export(str(out), version="2.0")
        content = out.read_text()
        assert "~Curve Information" in content
        assert "~Ascii" in content


class TestLas3Roundtrip:
    """Tests for LAS 3.0 export → reimport roundtrip."""

    def test_v3_roundtrip(self, las3_file, tmp_path):
        df_original = las3_file.data()
        out = tmp_path / "rt.las"
        las3_file.export(str(out), version="3.0")

        reloaded = LasFile(str(out))
        assert reloaded._las_version == "3.0"
        df_reloaded = reloaded.data()

        assert list(df_reloaded.columns) == list(df_original.columns)
        np.testing.assert_array_almost_equal(
            df_reloaded["DEPT"].values, df_original["DEPT"].values, decimal=4
        )
        np.testing.assert_array_almost_equal(
            df_reloaded["PHIE"].values, df_original["PHIE"].values, decimal=4
        )

    def test_v2_to_v3_roundtrip(self, tmp_las_file, tmp_path):
        las2 = LasFile(str(tmp_las_file))
        df_original = las2.data()

        # Export as LAS 3.0
        v3_path = tmp_path / "converted.las"
        las2.export(str(v3_path), version="3.0")

        # Reimport
        las3 = LasFile(str(v3_path))
        assert las3._las_version == "3.0"
        df_reimported = las3.data()

        np.testing.assert_array_almost_equal(
            df_reimported["DEPT"].values, df_original["DEPT"].values, decimal=4
        )
        np.testing.assert_array_almost_equal(
            df_reimported["PHIE"].values, df_original["PHIE"].values, decimal=4
        )

    def test_v3_to_v2_roundtrip(self, las3_file, tmp_path):
        df_original = las3_file.data()

        # Export as LAS 2.0
        v2_path = tmp_path / "converted.las"
        las3_file.export(str(v2_path), version="2.0")

        # Reimport
        las2 = LasFile(str(v2_path))
        assert las2._las_version == "2.0"
        df_reimported = las2.data()

        np.testing.assert_array_almost_equal(
            df_reimported["PHIE"].values, df_original["PHIE"].values, decimal=4
        )
