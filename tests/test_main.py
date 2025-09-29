import importlib


def test_module_main_invokes_repl(monkeypatch):
    mod = importlib.import_module("calc.cli")
    called = {"ok": False}
    def fake_repl(input_func=None, output_func=None):
        called["ok"] = True
    monkeypatch.setattr(mod, "repl", fake_repl)
    mod.main()
    assert called["ok"] is True
    
import builtins
import runpy


def test_cli_main_guard_executes(monkeypatch):
    # When run as a script, make input() immediately raise EOF so REPL exits.
    def fake_input(_):  # noqa: ARG001
        raise EOFError
    monkeypatch.setattr(builtins, "input", fake_input)
    # This executes the module as if run via: python -m calc.cli
    runpy.run_module("calc.cli", run_name="__main__")
