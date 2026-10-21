from ai_competitiveness import GEOS, __version__
from ai_competitiveness.__main__ import main


def test_geos_are_the_three_first_class_geographies():
    assert GEOS == ("EU27", "US", "CHN")


def test_version_is_set():
    assert __version__


def test_cli_runs(capsys):
    assert main([]) == 0
    assert "EU27" in capsys.readouterr().out
