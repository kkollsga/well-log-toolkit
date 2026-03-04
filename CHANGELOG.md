# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

Future entries are managed by [towncrier](https://towncrier.readthedocs.io/).
To add a changelog entry, create a file in the `changes/` directory.

<!-- towncrier release notes start -->

## [0.1.153] - 2026-03-04

### Internal Changes

- Moved test directory from `pytest/` to `tests/` to match standard Python conventions.
- CI now runs the full pytest suite across Python 3.10-3.13 instead of a smoke import.
- Dropped Python 3.9 support; minimum version is now 3.10.
- Added towncrier-based changelog system for fragment-based release notes.
- Updated project classifier from Alpha to Beta.
- Updated project description to reflect full petrophysical analysis capabilities.
- Fixed issues URL in README (was pointing to `yourusername` placeholder).
- Added PyPI and CI status badges to README.

## [0.1.152] - 2024-12-29

### Summary

This is a retrospective entry covering the cumulative state of the library at v0.1.152.

### Features

- Lazy LAS 2.0 file reader with header-only parsing and on-demand data loading.
- `Property` class with depth-weighted statistics (mean, sum, std, percentile, mode).
- Chained hierarchical filtering: `well.PHIE.filter('Zone').filter('Facies').sums_avg()`.
- Numpy-style operator overloading on Property objects (24 operators).
- `WellDataManager` for multi-well orchestration with property broadcasting.
- `_ManagerPropertyProxy` for cross-well operations: `manager.PHIE.filter('Zone').mean()`.
- `SumsAvgResult.report()` with arithmetic, geometric, pooled, and sum aggregation.
- Template-driven well log visualization (`Template`, `WellView`).
- Interactive crossplots with multi-dimensional mapping (`Crossplot`).
- 6 regression types: linear, polynomial, exponential, logarithmic, power, polynomial-exponential.
- Parameter locking for regression coefficients.
- Discrete property support with label/color/style/thickness mappings.
- Source-aware property storage for round-trip LAS export.
- Computed property creation via `well.HC = well.PHIE * (1 - well.SW)`.
- Project save/load to JSON with full metadata preservation.
- Depth interval computation using midpoint method with zone boundary truncation.
- Property resampling with configurable methods (linear, nearest, forward-fill).
- Strict depth alignment enforcement with detailed error guidance.
