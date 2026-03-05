"""Tests for _ManagerPropertyProxy result caching."""

import numpy as np
import pandas as pd
import pytest

from logsuite import WellDataManager


@pytest.fixture
def manager():
    """Manager with 2 wells and discrete Zone property."""
    mgr = WellDataManager()
    depth = np.arange(1000.0, 1010.0, 1.0)

    for wname, phie_base in [("Well_A", 0.18), ("Well_B", 0.22)]:
        df = pd.DataFrame(
            {
                "DEPT": depth,
                "PHIE": np.linspace(phie_base - 0.03, phie_base + 0.03, len(depth)),
                "SW": np.linspace(0.30, 0.40, len(depth)),
                "Zone": [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
            }
        )
        mgr.load_properties(
            df,
            well_col=None,
            well_name=wname,
            source_name="petrophysics",
            unit_mappings={"PHIE": "v/v", "SW": "v/v"},
            type_mappings={"Zone": "discrete"},
            label_mappings={"Zone": {0: "NonReservoir", 1: "Reservoir"}},
        )

    return mgr


class TestCacheHit:
    def test_mean_cached(self, manager):
        proxy = manager.PHIE
        result1 = proxy.mean()
        result2 = proxy.mean()
        assert result1 == result2
        assert len(proxy._cache) == 1

    def test_filtered_mean_cached(self, manager):
        proxy = manager.PHIE.filter("Zone")
        result1 = proxy.mean()
        result2 = proxy.mean()
        assert result1 == result2
        assert len(proxy._cache) == 1

    def test_min_cached(self, manager):
        proxy = manager.PHIE
        result1 = proxy.min()
        result2 = proxy.min()
        assert result1 == result2

    def test_max_cached(self, manager):
        proxy = manager.PHIE
        result1 = proxy.max()
        result2 = proxy.max()
        assert result1 == result2

    def test_std_cached(self, manager):
        proxy = manager.PHIE
        result1 = proxy.std()
        result2 = proxy.std()
        assert result1 == result2

    def test_median_cached(self, manager):
        proxy = manager.PHIE
        result1 = proxy.median()
        result2 = proxy.median()
        assert result1 == result2

    def test_sums_avg_cached(self, manager):
        proxy = manager.PHIE.filter("Zone")
        result1 = proxy.sums_avg()
        result2 = proxy.sums_avg()
        assert result1 is result2


class TestCacheIsolation:
    def test_different_params_different_cache_entries(self, manager):
        proxy = manager.PHIE
        proxy.mean(weighted=True)
        proxy.mean(weighted=False)
        # Two distinct cache entries for different params
        assert len(proxy._cache) == 2
        assert ("mean", True, False, False) in proxy._cache
        assert ("mean", False, False, False) in proxy._cache

    def test_filter_creates_fresh_cache(self, manager):
        proxy = manager.PHIE
        proxy.mean()
        assert len(proxy._cache) == 1

        filtered = proxy.filter("Zone")
        assert len(filtered._cache) == 0

    def test_separate_proxies_separate_caches(self, manager):
        proxy1 = manager.PHIE
        proxy2 = manager.PHIE
        proxy1.mean()
        assert len(proxy1._cache) == 1
        assert len(proxy2._cache) == 0
