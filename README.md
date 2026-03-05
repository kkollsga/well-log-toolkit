# logSuite

Fast, intuitive Python library for petrophysical well log analysis. Load LAS files, filter by zones, compute depth-weighted statistics, and create publication-quality log displays—all in just a few lines.

[![PyPI version](https://img.shields.io/pypi/v/logsuite.svg)](https://pypi.org/project/logsuite/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/kkollsga/logsuite/actions/workflows/build-and-publish.yml/badge.svg)](https://github.com/kkollsga/logsuite/actions)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://readthedocs.org/projects/logsuite/badge/?version=latest)](https://logsuite.readthedocs.io)

## Key Features

- **Lazy Loading** — Parse headers instantly, load data on demand
- **Numpy-Style Operations** — `well.HC_Volume = well.PHIE * (1 - well.SW)`
- **Hierarchical Filtering** — Chain filters: `well.PHIE.filter('Zone').filter('Facies').sums_avg()`
- **Depth-Weighted Statistics** — Proper averaging for irregular sampling
- **Multi-Well Analytics** — Cross-well statistics: `manager.PHIE.filter('Zone').percentile(50)`
- **Professional Visualization** — Customizable well log displays with templates
- **Interactive Crossplots** — Scatter plots with color/size/shape mapping by property
- **Regression Analysis** — Linear, polynomial, exponential, logarithmic, and power regression
- **Project Persistence** — Save/load entire projects with metadata and templates

## Installation

```bash
pip install logsuite
```

**Requirements:** Python 3.10+, numpy, pandas, scipy, matplotlib

## Quick Start

### 1-Minute Tutorial

```python
from logsuite import WellDataManager

# Load and analyze
manager = WellDataManager()
manager.load_las('well.las')

well = manager.well_12_3_4_A
stats = well.PHIE.filter('Zone').sums_avg()

print(stats['Top_Brent']['mean'])  # → 0.182 (depth-weighted)
```

Three lines to go from LAS file to zonal statistics.

### 5-Minute Quick Start

**Load data:**

```python
from logsuite import WellDataManager
import pandas as pd

manager = WellDataManager()
manager.load_las('well_A.las')
manager.load_las('well_B.las')

# Load formation tops from DataFrame
tops_df = pd.DataFrame({
    'Well': ['12/3-4 A', '12/3-4 A', '12/3-4 B'],
    'Surface': ['Top_Brent', 'Top_Statfjord', 'Top_Brent'],
    'MD': [2850.0, 3100.0, 2900.0]
})
manager.load_tops(tops_df, well_col='Well', discrete_col='Surface', depth_col='MD')
```

**Access wells and properties:**

```python
well = manager.well_12_3_4_A

phie = well.PHIE
sw = well.SW

print(well.properties)  # ['PHIE', 'SW', 'PERM', 'Zone', ...]
print(well.sources)     # ['Petrophysics', 'Imported_Tops']
```

**Compute statistics:**

```python
# Single filter — group by Zone
stats = well.PHIE.filter('Zone').sums_avg()

# Chain filters — hierarchical grouping
stats = well.PHIE.filter('Zone').filter('Facies').sums_avg()
```

**Create computed properties:**

```python
well.HC_Volume = well.PHIE * (1 - well.SW)
well.Reservoir = (well.PHIE > 0.15) & (well.SW < 0.35)

# Apply to all wells at once
manager.PHIE_percent = manager.PHIE * 100
```

**Visualize:**

```python
from logsuite import Template

template = Template("basic")
template.add_track(
    track_type="continuous",
    logs=[{"name": "GR", "x_range": [0, 150], "color": "green"}],
    title="Gamma Ray"
)
template.add_track(track_type="depth", width=0.3)

view = well.WellView(depth_range=[2800, 3000], template=template)
view.show()
```

**Save your work:**

```python
manager.save('my_project/')
manager = WellDataManager('my_project/')  # Load later
```

## Documentation

For detailed guides, API reference, and examples, visit the full documentation:

**[logsuite.readthedocs.io](https://logsuite.readthedocs.io)**

- [Quick Start](https://logsuite.readthedocs.io/en/latest/quickstart.html) — Get up and running
- [Loading Data](https://logsuite.readthedocs.io/en/latest/user-guide/loading-data.html) — LAS files, tops, and data import
- [Wells & Properties](https://logsuite.readthedocs.io/en/latest/user-guide/wells-properties.html) — Property types, filtering, computed logs
- [Statistics](https://logsuite.readthedocs.io/en/latest/user-guide/statistics.html) — Depth-weighted statistics and sums/averages
- [Visualization](https://logsuite.readthedocs.io/en/latest/user-guide/visualization.html) — Well log displays and templates
- [Regression](https://logsuite.readthedocs.io/en/latest/user-guide/regression.html) — Trend fitting and crossplots
- [Multi-Well Analysis](https://logsuite.readthedocs.io/en/latest/user-guide/multi-well.html) — Cross-well workflows
- [API Reference](https://logsuite.readthedocs.io/en/latest/api/index.html) — Complete class and method documentation

## License

MIT — see [LICENSE](LICENSE) for details.
