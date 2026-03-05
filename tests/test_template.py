"""Tests for logsuite.visualization.template.Template."""

import pytest

from logsuite import Template


class TestTemplateInit:
    def test_empty_template(self):
        t = Template()
        assert t.name == "default"
        assert t.tracks == []
        assert t.tops == []

    def test_named_template(self):
        t = Template("reservoir")
        assert t.name == "reservoir"

    def test_init_with_tracks(self):
        tracks = [{"type": "depth", "logs": [], "width": 0.5}]
        t = Template("t", tracks=tracks)
        assert len(t.tracks) == 1
        assert t.tracks[0]["type"] == "depth"


class TestAddTrack:
    def test_continuous(self):
        t = Template()
        t.add_track(
            track_type="continuous",
            logs=[{"name": "GR", "x_range": [0, 150], "color": "green"}],
            title="GR",
        )
        assert len(t.tracks) == 1
        assert t.tracks[0]["type"] == "continuous"
        assert t.tracks[0]["logs"][0]["name"] == "GR"
        assert t.tracks[0]["title"] == "GR"

    def test_discrete(self):
        t = Template()
        t.add_track(track_type="discrete", logs=[{"name": "Zone"}], title="Zones")
        assert t.tracks[0]["type"] == "discrete"

    def test_depth(self):
        t = Template()
        t.add_track(track_type="depth", width=0.3)
        assert t.tracks[0]["type"] == "depth"
        assert t.tracks[0]["width"] == 0.3

    def test_chaining(self):
        t = Template()
        result = t.add_track(track_type="depth").add_track(track_type="continuous")
        assert result is t
        assert len(t.tracks) == 2

    def test_fill_dict_normalized_to_list(self):
        t = Template()
        t.add_track(fill={"left": "PHIE", "right": 0, "color": "blue"})
        assert isinstance(t.tracks[0]["fill"], list)
        assert len(t.tracks[0]["fill"]) == 1

    def test_fill_list_kept_as_list(self):
        t = Template()
        fills = [
            {"left": "PHIE", "right": 0, "color": "blue"},
            {"left": "SW", "right": 1, "color": "red"},
        ]
        t.add_track(fill=fills)
        assert len(t.tracks[0]["fill"]) == 2

    def test_no_fill(self):
        t = Template()
        t.add_track()
        assert t.tracks[0]["fill"] is None

    def test_no_logs(self):
        t = Template()
        t.add_track()
        assert t.tracks[0]["logs"] == []

    def test_log_scale(self):
        t = Template()
        t.add_track(log_scale=True)
        assert t.tracks[0]["log_scale"] is True

    def test_default_width(self):
        t = Template()
        t.add_track()
        assert t.tracks[0]["width"] == 1.0


class TestRemoveTrack:
    def test_remove_first(self):
        t = Template()
        t.add_track(title="A").add_track(title="B")
        t.remove_track(0)
        assert len(t.tracks) == 1
        assert t.tracks[0]["title"] == "B"

    def test_remove_out_of_range(self):
        t = Template()
        t.add_track()
        with pytest.raises(IndexError):
            t.remove_track(5)

    def test_remove_chaining(self):
        t = Template()
        t.add_track().add_track()
        result = t.remove_track(0)
        assert result is t


class TestEditTrack:
    def test_edit_title(self):
        t = Template()
        t.add_track(title="Old")
        t.edit_track(0, title="New")
        assert t.tracks[0]["title"] == "New"

    def test_edit_out_of_range(self):
        t = Template()
        with pytest.raises(IndexError):
            t.edit_track(0, title="X")

    def test_edit_chaining(self):
        t = Template()
        t.add_track()
        result = t.edit_track(0, title="X")
        assert result is t


class TestGetTrack:
    def test_get_returns_copy(self):
        t = Template()
        t.add_track(title="Original")
        track = t.get_track(0)
        track["title"] = "Modified"
        assert t.tracks[0]["title"] == "Original"

    def test_get_out_of_range(self):
        t = Template()
        with pytest.raises(IndexError):
            t.get_track(0)


class TestSaveLoad:
    def test_roundtrip(self, tmp_path):
        t = Template("test_tmpl")
        t.add_track(
            track_type="continuous",
            logs=[{"name": "GR", "x_range": [0, 150]}],
            title="GR",
            width=2.0,
        )
        t.add_track(track_type="depth", width=0.3)

        filepath = tmp_path / "template.json"
        t.save(filepath)

        loaded = Template.load(filepath)
        assert loaded.name == "test_tmpl"
        assert len(loaded.tracks) == 2
        assert loaded.tracks[0]["title"] == "GR"
        assert loaded.tracks[1]["type"] == "depth"

    def test_roundtrip_with_tops(self, tmp_path):
        t = Template("tops_tmpl")
        t.add_tops(tops_dict={2850.0: "Reservoir", 2920.0: "Seal"})
        t.add_track(track_type="depth")

        filepath = tmp_path / "template.json"
        t.save(filepath)

        loaded = Template.load(filepath)
        assert len(loaded.tops) == 1
        assert loaded.tops[0]["tops_dict"]["2850.0"] == "Reservoir"


class TestDictConversion:
    def test_to_dict(self):
        t = Template("d")
        t.add_track(track_type="depth")
        d = t.to_dict()
        assert d["name"] == "d"
        assert len(d["tracks"]) == 1
        assert "tops" in d

    def test_from_dict_roundtrip(self):
        t = Template("rt")
        t.add_track(track_type="continuous", logs=[{"name": "PHIE"}])
        d = t.to_dict()
        t2 = Template.from_dict(d)
        assert t2.name == "rt"
        assert len(t2.tracks) == 1
        assert t2.tracks[0]["logs"][0]["name"] == "PHIE"


class TestAddTops:
    def test_tops_dict(self):
        t = Template()
        t.add_tops(tops_dict={2850.0: "Res"})
        assert len(t.tops) == 1
        assert t.tops[0]["tops_dict"][2850.0] == "Res"

    def test_property_name(self):
        t = Template()
        t.add_tops(property_name="Zone")
        assert t.tops[0]["property_name"] == "Zone"

    def test_both_raises(self):
        t = Template()
        with pytest.raises(ValueError):
            t.add_tops(property_name="Zone", tops_dict={2850.0: "A"})

    def test_neither_raises(self):
        t = Template()
        with pytest.raises(ValueError):
            t.add_tops()

    def test_chaining(self):
        t = Template()
        result = t.add_tops(property_name="Zone")
        assert result is t


class TestRepr:
    def test_repr(self):
        t = Template("my_tmpl")
        t.add_track().add_track()
        assert "my_tmpl" in repr(t)
        assert "2" in repr(t)
