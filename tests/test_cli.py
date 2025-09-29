from calc.cli import HELP_TEXT, parse_line, process_line, repl


def test_parse_line():
    assert parse_line("") == (None, [])
    assert parse_line("add 2 3") == ("add", ["2", "3"])
    assert parse_line("  DIV  10  2 ") == ("div", ["10", "2"])

def test_process_line_unknown_and_help():
    assert process_line("help", []) == HELP_TEXT
    msg = process_line("bogus", [])
    assert "unknown command" in msg

def test_process_line_validation():
    assert "expected two numbers" in process_line("add", [])
    assert "arguments must be numbers" in process_line("add", ["a", "2"])

def test_process_line_success_and_errors():
    assert process_line("add", ["2", "3"]) == "5"
    assert process_line("sub", ["5", "3"]) == "2"
    assert process_line("mul", ["2", "3"]) == "6"
    assert process_line("div", ["6", "3"]) == "2"
    assert process_line("div", ["1", "0"]).startswith("Error: division by zero")

def test_repl_flow(monkeypatch):
    inputs = iter(["add 2 3", "div 4 0", "unknown", "help", "quit"])
    def fake_input(prompt):
        return next(inputs)
    outputs = []
    def fake_print(msg=""):
        outputs.append(msg)
    repl(input_func=fake_input, output_func=fake_print)
    out = "\n".join(outputs)
    assert "Calculator ready" in out
    assert "5" in out
    assert "division by zero" in out
    assert "unknown command" in out
    assert "Commands:" in out
    assert "Bye!" in out
def test_repl_handles_eof(monkeypatch):
    # input() raises EOFError immediately (e.g., Ctrl-D)
    def fake_input(prompt):
        raise EOFError
    outputs = []
    def fake_print(msg=""):
        outputs.append(msg)
    from calc.cli import repl
    repl(input_func=fake_input, output_func=fake_print)
    # Last line should be a Bye path triggered by EOF
    assert outputs[-1].strip() == "Bye!"

def test_process_line_exit_alias():
    from calc.cli import process_line
    assert process_line("exit", []) == "QUIT"

def test_process_line_non_integer_formatting():
    # Ensure _format_number path for non-integers is covered (e.g., 1/2 = 0.5)
    from calc.cli import process_line
    assert process_line("div", ["1", "2"]) == "0.5"

def test_empty_line_is_ignored_in_repl(monkeypatch):
    # "" should produce no output (other than banner and eventual Bye)
    inputs = iter(["", "quit"])
    def fake_input(prompt):
        return next(inputs)
    outputs = []
    def fake_print(msg=""):
        outputs.append(msg)
    from calc.cli import repl
    repl(input_func=fake_input, output_func=fake_print)
    text = "\n".join(outputs)
    # We should see banner and Bye, but no error for the empty line
    assert "Calculator ready" in text
    assert "Bye!" in text
