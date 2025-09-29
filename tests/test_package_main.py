import runpy

import calc.cli as cli


def test_package_main_executes(monkeypatch):
    called = {"ok": False}

    def fake_main():
        called["ok"] = True

    # Replace cli.main with fake_main so we can check it’s called
    monkeypatch.setattr(cli, "main", fake_main)

    # This simulates running: python -m calc
    runpy.run_module("calc", run_name="__main__")

    assert called["ok"] is True
