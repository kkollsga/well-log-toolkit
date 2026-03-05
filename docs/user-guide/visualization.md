# Visualization

## Template

A `Template` defines the track layout for well log plots:

```python
from logsuite import Template

template = Template()

# Add tracks with logs
template.add_track(track_type="depth", width=0.5)
template.add_track(
    track_type="continuous",
    logs=[{"name": "GR", "color": "green", "x_range": [0, 150]}],
    title="GR",
    width=2,
)
template.add_track(
    track_type="continuous",
    logs=[{"name": "PHIE", "color": "blue", "x_range": [0, 0.4]}],
    title="Porosity",
    width=2,
)
template.add_track(
    track_type="continuous",
    logs=[{"name": "SW", "color": "red", "x_range": [0, 1]}],
    title="Saturation",
    width=2,
)
```

## WellView

`WellView` renders a well log display using a template:

```python
from logsuite import WellView

view = WellView(well, template=template)
view.show()

# With depth range
view = WellView(well, template=template, depth_range=(2800, 3200))
view.show()
```

## Crossplot

Create crossplots with optional regression:

```python
from logsuite import Crossplot

xplot = Crossplot(
    wells=well,
    x="PHIE",
    y="PERM",
    color="Zone",
)
xplot.show()
```

### With Regression

```python
from logsuite import Crossplot

xplot = Crossplot(wells=well, x="PHIE", y="PERM")
xplot.add_regression("exponential")
xplot.show()
```
