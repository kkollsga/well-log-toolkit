"""Tests for logsuite.visualization.wellview.WellView initialization (non-visual)."""

import numpy as np
import pandas as pd
import pytest

from logsuite import Property, Template, Well, WellView


@pytest.fixture
def simple_well():
    """Minimal well with one continuous property."""
    well = Well(name="Test", sanitized_name="test")
    df = pd.DataFrame({
        "DEPT": np.arange(2800.0, 2810.0, 1.0),
        "GR": np.linspace(30, 80, 10),
        "PHIE": np.linspace(0.10, 0.25, 10),
    })
    well.add_dataframe(df)
    return well


@pytest.fixture
def simple_template():
    """Template with one continuous track."""
    t = Template("test")
    t.add_track(
        track_type="continuous",
        logs=[{"name": "GR", "x_range": [0, 150]}],
        title="GR",
    )
    return t


class TestWellViewInit:
    def test_with_template(self, simple_well, simple_template):
        view = WellView(simple_well, template=simple_template)
        assert view.well is simple_well
        assert view.template is simple_template

    def test_default_template(self, simple_well):
        view = WellView(simple_well)
        assert view.template is not None
        assert len(view.template.tracks) > 0

    def test_depth_range(self, simple_well, simple_template):
        view = WellView(simple_well, template=simple_template, depth_range=(2802, 2808))
        assert view.depth_range == (2802, 2808)

    def test_full_depth_range(self, simple_well, simple_template):
        view = WellView(simple_well, template=simple_template)
        assert view.depth_range[0] == pytest.approx(2800.0)
        assert view.depth_range[1] == pytest.approx(2809.0)

    def test_explicit_figsize(self, simple_well, simple_template):
        view = WellView(simple_well, template=simple_template, figsize=(12, 8))
        assert view.figsize == (12, 8)

    def test_auto_figsize(self, simple_well, simple_template):
        view = WellView(simple_well, template=simple_template)
        assert view.figsize is not None
        assert len(view.figsize) == 2
        assert view.figsize[0] > 0
        assert view.figsize[1] > 0

    def test_dpi(self, simple_well, simple_template):
        view = WellView(simple_well, template=simple_template, dpi=150)
        assert view.dpi == 150

    def test_no_properties_raises(self):
        empty_well = Well(name="Empty", sanitized_name="empty")
        with pytest.raises(ValueError, match="no properties"):
            WellView(empty_well)
