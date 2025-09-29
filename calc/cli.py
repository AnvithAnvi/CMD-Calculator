from .operations import add, div, mul, sub

HELP_TEXT = (
    "Commands:\n"
    "  add x y   -> x + y\n"
    "  sub x y   -> x - y\n"
    "  mul x y   -> x * y\n"
    "  div x y   -> x / y (y != 0)\n"
    "  help      -> show this help\n"
    "  quit/exit -> leave the program\n"
)

def parse_line(line):
    line = (line or "").strip()
    if not line:
        return None, []
    parts = line.split()
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args

def _format_number(x):
    return str(int(x)) if float(x).is_integer() else str(x)

def process_line(cmd, args):
    if cmd in (None, ""):
        return None
    if cmd in ("quit", "exit"):
        return "QUIT"
    if cmd == "help":
        return HELP_TEXT
    if cmd not in {"add", "sub", "mul", "div"}:
        return f"Error: unknown command '{cmd}'. Type 'help' for options."
    if len(args) != 2:
        return "Error: expected two numbers, e.g. 'add 2 3'"
    try:
        a = float(args[0])
        b = float(args[1])
    except (TypeError, ValueError):
        return "Error: arguments must be numbers"
    try:
        if cmd == "add":
            return _format_number(add(a, b))
        if cmd == "sub":
            return _format_number(sub(a, b))
        if cmd == "mul":
            return _format_number(mul(a, b))
        if cmd == "div":
            return _format_number(div(a, b))
    except ZeroDivisionError as e:
        return f"Error: {e}"


def repl(input_func=input, output_func=print):
    output_func("Calculator ready. Type 'help' for commands.")
    while True:
        try:
            line = input_func("> ")
        except EOFError:
            output_func("\nBye!")
            break
        cmd, args = parse_line(line)
        result = process_line(cmd, args)
        if result is None:
            continue
        if result == "QUIT":
            output_func("Bye!")
            break
        output_func(result)

def main():
    repl()

if __name__ == "__main__":
    main()
