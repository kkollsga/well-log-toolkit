"""Tests for logsuite.utils utility functions."""

import pytest

from logsuite.utils import (
    filter_names,
    parse_las_line,
    sanitize_property_name,
    sanitize_well_name,
    suggest_similar_names,
)


class TestSanitizeWellName:
    def test_standard(self):
        assert sanitize_well_name("36/7-5 A") == "36_7_5_A"

    def test_keep_hyphens(self):
        assert sanitize_well_name("36/7-5 A", keep_hyphens=True) == "36_7-5_A"

    def test_consecutive_underscores(self):
        result = sanitize_well_name("a//b")
        assert "__" not in result
        assert result == "a_b"

    def test_trailing_underscores(self):
        result = sanitize_well_name("test_")
        assert not result.endswith("_")

    def test_leading_underscores(self):
        result = sanitize_well_name("_test")
        assert not result.startswith("_")

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            sanitize_well_name("")

    def test_none_raises(self):
        with pytest.raises(ValueError):
            sanitize_well_name(None)

    def test_simple_name(self):
        assert sanitize_well_name("WellA") == "WellA"

    def test_hyphen_replaced_by_default(self):
        assert sanitize_well_name("Well-A") == "Well_A"

    def test_hyphen_kept(self):
        assert sanitize_well_name("Well-A", keep_hyphens=True) == "Well-A"


class TestSanitizePropertyName:
    def test_standard(self):
        assert sanitize_property_name("PHIE") == "PHIE"

    def test_starts_with_digit(self):
        assert sanitize_property_name("2025_PERM") == "prop_2025_PERM"

    def test_special_chars(self):
        result = sanitize_property_name("PHIE-2025")
        assert result == "PHIE_2025"

    def test_parentheses(self):
        result = sanitize_property_name("SW (v/v)")
        # Special chars replaced with underscore, consecutive underscores collapsed
        assert "(" not in result
        assert "/" not in result

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            sanitize_property_name("")

    def test_none_raises(self):
        with pytest.raises(ValueError):
            sanitize_property_name(None)

    def test_quotes(self):
        result = sanitize_property_name("Zoneloglinkedto'CerisaTops'")
        assert "'" not in result


class TestParseLasLine:
    def test_standard(self):
        assert parse_las_line("DEPT .m : DEPTH") == ("DEPT", "m", "DEPTH")

    def test_no_unit(self):
        mnem, val, desc = parse_las_line("WELL.  12/3-2 B   : WELL")
        assert mnem == "WELL"
        assert "12/3-2 B" in val
        assert desc == "WELL"

    def test_null_value(self):
        mnem, val, desc = parse_las_line("NULL .  -999.25 : NULL VALUE")
        assert mnem == "NULL"
        assert "-999.25" in val
        assert desc == "NULL VALUE"

    def test_complex_unit(self):
        mnem, unit, desc = parse_las_line("PhiTLam_2025.m3/m3 : Porosity")
        assert mnem == "PhiTLam_2025"
        assert unit == "m3/m3"
        assert desc == "Porosity"

    def test_no_colon(self):
        mnem, val, desc = parse_las_line("DEPT .m")
        assert mnem == "DEPT"
        assert desc == ""

    def test_empty_string(self):
        mnem, val, desc = parse_las_line("")
        assert mnem == ""


class TestFilterNames:
    def test_include_only(self):
        result = filter_names(["A", "B", "C", "D"], include=["A", "B"])
        assert result == ["A", "B"]

    def test_exclude_only(self):
        result = filter_names(["A", "B", "C", "D"], exclude=["D"])
        assert result == ["A", "B", "C"]

    def test_both(self):
        result = filter_names(["A", "B", "C", "D"], include=["A", "B", "C"], exclude=["C"])
        assert result == ["A", "B"]

    def test_none_returns_none(self):
        result = filter_names(["A", "B"])
        assert result is None

    def test_single_string_include(self):
        result = filter_names(["A", "B", "C"], include="A")
        assert result == ["A"]

    def test_single_string_exclude(self):
        result = filter_names(["A", "B", "C"], exclude="C")
        assert result == ["A", "B"]


class TestSuggestSimilarNames:
    def test_close_match(self):
        result = suggest_similar_names("PHEI", ["PHIE", "SW", "GR"])
        assert "PHIE" in result

    def test_no_match(self):
        result = suggest_similar_names("ZZZZZ", ["PHIE", "SW", "GR"])
        assert result == []

    def test_empty_available(self):
        result = suggest_similar_names("PHIE", [])
        assert result == []

    def test_max_results(self):
        available = ["PHIE", "PHIE2", "PHIE3", "PHIE4", "PHIE5"]
        result = suggest_similar_names("PHIE", available, n=2)
        assert len(result) <= 2
