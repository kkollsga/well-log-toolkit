# Changelog Fragments

This directory contains changelog entries managed by [towncrier](https://towncrier.readthedocs.io/).

## Adding an entry

Create a file named `<identifier>.<type>` with a short description of the change.

**Identifier:** PR number, issue number, or a short descriptive slug (e.g., `fix-export`).

**Types:**

| Type | Directory | Description |
|------|-----------|-------------|
| feature | `feature` | New functionality |
| bugfix | `bugfix` | Bug fixes |
| breaking | `breaking` | Breaking API changes |
| deprecation | `deprecation` | Deprecated features |
| doc | `doc` | Documentation changes |
| misc | `misc` | Internal changes (refactors, CI, tests) |

## Examples

```bash
# New feature (PR #42)
echo "Added geometric mean to statistics module." > changes/42.feature

# Bug fix
echo "Fixed off-by-one in zone interval truncation." > changes/fix-zone-intervals.bugfix

# Internal change
echo "Split visualization.py into subpackage." > changes/split-viz.misc
```

## Building the changelog

At release time, run:

```bash
towncrier build --version X.Y.Z
```

This collects all fragments, adds them to `CHANGELOG.md`, and removes the fragment files.
