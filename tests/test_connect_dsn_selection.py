"""
generate_labels.connect() - which plant's Label Traxx to talk to. See
TestConnectDsnSelection in tests/test_barbell_gui.py for the GUI equivalent
(BarBellApp._connect()).
"""

from generate_labels import connect
from src.db.readonly_connection import ReadOnlyConnection
from src.demo_data import DemoConnection
from src.settings import Settings


def test_connect_passes_label_traxx_dsn_through_to_readonly_connection():
    settings = Settings(demo_mode=False, label_traxx_dsn="LCJ JAM")
    conn = connect(settings)
    assert isinstance(conn, ReadOnlyConnection)
    assert conn._dsn == "LCJ JAM"


def test_connect_falls_back_to_env_when_label_traxx_dsn_unset(monkeypatch):
    monkeypatch.setenv("LT_DSN", "LT64")
    monkeypatch.setenv("LT_USER", "designer")
    monkeypatch.setenv("LT_PASSWORD", "unused")

    settings = Settings(demo_mode=False, label_traxx_dsn="")
    conn = connect(settings)
    assert conn._dsn == "LT64"


def test_connect_returns_demo_connection_when_demo_mode_is_on():
    settings = Settings(demo_mode=True, label_traxx_dsn="LCJ JAM")
    assert isinstance(connect(settings), DemoConnection)
