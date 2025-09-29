# main.py
import ast
import tkinter as tk
from tkinter import messagebox

from calc.operations import add, div, mul, sub


# ----------------- Safe evaluation (supports + - * / and parentheses) -----------------
def _eval_ast(node):
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    if isinstance(node, ast.Constant):           # numbers like 12, 3.5
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Only numbers are allowed")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_ast(node.operand)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
        return +_eval_ast(node.operand)
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        if isinstance(node.op, ast.Add):
            return add(left, right)
        if isinstance(node.op, ast.Sub):
            return sub(left, right)
        if isinstance(node.op, ast.Mult):
            return mul(left, right)
        if isinstance(node.op, ast.Div):
            return div(left, right)  # will raise ZeroDivisionError if right == 0
        raise ValueError("Only + - * / are supported")
    # Parentheses are handled by AST structure; no special-case needed
    raise ValueError("Invalid expression")

def safe_eval(expr: str) -> float:
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError("Malformed expression") from e
    return _eval_ast(tree)

def format_number(x: float) -> str:
    return str(int(x)) if float(x).is_integer() else str(x)

# ----------------- GUI -----------------
class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Calculator")
        self.resizable(False, False)

        self.expr_var = tk.StringVar(value="")
        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # Display
        entry = tk.Entry(self, textvariable=self.expr_var, font=("Arial", 20), justify="right", bd=8, relief="ridge")
        entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        entry.focus_set()

        # Button factory
        def btn(txt, r, c, cmd=None, colspan=1, w=5, h=2):
            b = tk.Button(self, text=txt, font=("Arial", 16), width=w, height=h,
                          command=cmd or (lambda t=txt: self.insert_text(t)))
            b.grid(row=r, column=c, columnspan=colspan, padx=5, pady=5, sticky="nsew")
            return b

        # Row 1: C, ⌫, (, )
        btn("C", 1, 0, cmd=self.clear)
        btn("⌫", 1, 1, cmd=self.backspace)
        btn("(", 1, 2)
        btn(")", 1, 3)

        # Row 2: 7 8 9 /
        btn("7", 2, 0); btn("8", 2, 1); btn("9", 2, 2); btn("÷", 2, 3, cmd=lambda: self.insert_text("/"))

        # Row 3: 4 5 6 *
        btn("4", 3, 0); btn("5", 3, 1); btn("6", 3, 2); btn("×", 3, 3, cmd=lambda: self.insert_text("*"))

        # Row 4: 1 2 3 -
        btn("1", 4, 0); btn("2", 4, 1); btn("3", 4, 2); btn("−", 4, 3, cmd=lambda: self.insert_text("-"))

        # Row 5: 0 . + =
        btn("0", 5, 0); btn(".", 5, 1); btn("+", 5, 2)
        btn("=", 5, 3, cmd=self.equals)

        # Make grid stretchy (nice sizing)
        for r in range(6):
            self.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.grid_columnconfigure(c, weight=1)

    def _bind_keys(self):
        # Digits, operators, parentheses, dot
        for ch in "0123456789+-*/().":
            self.bind(ch, self._on_key)
        # Enter = equals
        self.bind("<Return>", lambda e: self.equals())
        self.bind("<KP_Enter>", lambda e: self.equals())
        # Backspace & Escape
        self.bind("<BackSpace>", lambda e: self.backspace())
        self.bind("<Escape>", lambda e: self.clear())

    def _on_key(self, event):
        self.insert_text(event.char)

    def insert_text(self, text: str):
        self.expr_var.set(self.expr_var.get() + text)

    def clear(self):
        self.expr_var.set("")

    def backspace(self):
        s = self.expr_var.get()
        self.expr_var.set(s[:-1] if s else "")

    def equals(self):
        expr = self.expr_var.get().strip()
        if not expr:
            return
        try:
            value = safe_eval(expr)
            self.expr_var.set(format_number(value))
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    Calculator().mainloop()
