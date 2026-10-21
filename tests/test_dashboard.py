"""Run the Streamlit app headlessly against the real processed dataset."""

import pytest

from ai_competitiveness.catalog import INDICATORS
from ai_competitiveness.schema import PROCESSED_PATH, REPO_ROOT

AppTest = pytest.importorskip("streamlit.testing.v1").AppTest
APP = str(REPO_ROOT / "app" / "dashboard.py")

pytestmark = pytest.mark.skipif(not PROCESSED_PATH.exists(), reason="dataset not built")


def run(index: int = 0):
    app = AppTest.from_file(APP, default_timeout=60).run()
    if index:
        app.sidebar.radio[0].set_value(list(INDICATORS)[index]).run()
    return app


@pytest.mark.parametrize("index", range(len(INDICATORS)))
def test_every_metric_renders_without_error(index):
    app = run(index)
    assert not app.exception, app.exception
    assert app.header[0].value == list(INDICATORS.values())[index].name


def test_context_metric_is_flagged_and_explains_missing_geographies():
    index = [i.scope for i in INDICATORS.values()].index("context")
    app = run(index)
    assert any("Context only" in w.value for w in app.warning)
    captions = " ".join(c.value for c in app.caption)
    assert "Not comparable" in captions and "Not available" in captions


def test_single_year_metric_warns_it_is_not_a_trend():
    app = run(0)  # AI VC by destination: 2025 only
    assert any("not a trend" in i.value for i in app.info)
