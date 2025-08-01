import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import os

HISTORY_FILE = "calc_history.txt"

# Logging function with timestamp
def log(entry):
    time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{time} {entry}"
    with open(HISTORY_FILE, "a") as f:
        f.write(line + "\n")
    history.insert(tk.END, line + "\n")

# Evaluate expression
def calculate():
    try:
        expr = entry.get()
        result = eval(expr)
        log(f"{expr} = {result}")
        entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid expression:\n{e}")

# Input helpers
def insert(val): entry.insert(tk.END, val)
def clear(): entry.delete(0, tk.END)

# History functions
def load_history():
    history.delete(1.0, tk.END)
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            history.insert(tk.END, f.read())

def clear_history():
    if messagebox.askyesno("Clear History", "Are you sure?"):
        open(HISTORY_FILE, "w").close()
        history.delete(1.0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Calculator")
root.geometry("400x600")
root.resizable(False, False)

entry = tk.Entry(root, font=("Arial", 18), justify="right")
entry.pack(padx=10, pady=10, fill=tk.X)

# Keypad layout
buttons = [
    ['7','8','9','/'],
    ['4','5','6','*'],
    ['1','2','3','-'],
    ['0','.','=','+'],
    ['C','(',')','**']
]

# Create buttons dynamically
frame = tk.Frame(root); frame.pack()
for r, row in enumerate(buttons):
    for c, val in enumerate(row):
        cmd = (
            calculate if val == '=' else
            clear if val == 'C' else
            lambda v=val: insert(v)
        )
        tk.Button(frame, text=val, width=5, height=2, font=("Arial", 14), command=cmd)\
          .grid(row=r, column=c, padx=2, pady=2)

# History area
tk.Label(root, text="History").pack()
history = scrolledtext.ScrolledText(root, width=40, height=8, font=("Courier", 10))
history.pack(padx=10, pady=5)

# History control buttons
btns = tk.Frame(root)
btns.pack(pady=5)
tk.Button(btns, text="🗑 Clear History", command=clear_history).pack(side=tk.RIGHT, padx=5)

load_history()
root.mainloop()
