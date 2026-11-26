"""Лабораторна робота №8. Варіант 9."""
import warnings
import tkinter as tk
from tkinter import messagebox

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

BG_COLOR = "#F1F5F9"

COLORS = {
    "синій": "tab:blue",
    "помаранчевий": "tab:orange",
    "зелений": "tab:green",
    "червоний": "tab:red",
    "фіолетовий": "tab:purple",
    "чорний": "black",
}

# Дозволений простір імен для безпечного виклику eval()
SAFE_NAMES = {
    "np": np,
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "atan": np.arctan,
    "exp": np.exp,
    "sqrt": np.sqrt,
    "abs": np.abs,
    "log": np.log,
    "ln": np.log,
    "log10": np.log10,
    "lg": np.log10,
    "pi": np.pi,
    "e": np.e,
}


def evaluate_function(x_array, formula_str):
    """Повертає numpy-масив значень функції для масиву x_array.
    У разі синтаксичної або математичної помилки (ділення на 0, корінь із від'ємного числа тощо) виводить messagebox.showerror() i повертає None"""
    formula_str = formula_str.strip()
    if not formula_str:
        messagebox.showerror(
            "Помилка введення",
            "Поле формули функції не може бути порожнім!")
        return None

    safe_env = dict(SAFE_NAMES)
    z = np.empty(x_array.size, dtype=float)
    for i in range(len(x_array)):
        safe_env["x"] = x_array[i]
        with warnings.catch_warnings():
            # Перетворюємо попередження NumPy у винятки Python
            warnings.filterwarnings("error")
            try:
                z[i] = eval(formula_str, {"__builtins__": None}, safe_env)
            except Exception as err:
                messagebox.showerror(
                    "Помилка обчислення",
                    f"Помилка ({err})\nпід час розрахунку значень "
                    f"функції:\nf(x) = {formula_str}\n"
                    f"(при x = {x_array[i]:.4f})")
                return None
    return z


def read_line_width():
    """Зчитує товщину лінії зі Spinbox; при помилці повертає None"""
    try:
        width = float(spin_width.get().strip())
    except ValueError:
        messagebox.showerror(
            "Помилка введення",
            "Товщина лінії повинна бути числом!")
        return None
    if width <= 0:
        messagebox.showerror(
            "Помилка введення",
            "Товщина лінії повинна бути більшою за нуль!")
        return None
    return width


def build_plots():
    """Обробник кнопки ПОБУДУВАТИ ГРАФІКИ"""
    try:
        a = float(entry_a.get().strip())
        b = float(entry_b.get().strip())
    except ValueError:
        messagebox.showerror(
            "Помилка введення",
            "Межі інтервалу a та b повинні бути дійсними числами!")
        return

    if not (np.isfinite(a) and np.isfinite(b)):
        messagebox.showerror(
            "Помилка введення",
            "Межі інтервалу a та b повинні бути скінченними числами!")
        return

    if a >= b:
        messagebox.showerror(
            "Помилка інтервалу",
            "Ліва межа 'a' повинна бути строго меншою за праву 'b'!")
        return

    width = read_line_width()
    if width is None:
        return

    x = np.linspace(a, b, 500)
    y1 = evaluate_function(x, entry_f1.get())
    if y1 is None:
        return
    y2 = evaluate_function(x, entry_f2.get())
    if y2 is None:
        return

    #очищення попереднього графіка та побудова нових кривих
    ax.clear()
    ax.plot(x, y1, label=f"f1(x) = {entry_f1.get().strip()}",
            color=COLORS[color1_var.get()], linewidth=width)
    ax.plot(x, y2, label=f"f2(x) = {entry_f2.get().strip()}",
            color=COLORS[color2_var.get()], linewidth=width)
    ax.grid(grid_var.get(), linestyle="--", alpha=0.7)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Графіки функцій користувача")
    ax.legend(fontsize=7)
    canvas.draw()


#Створення графічного інтерфейсу
window = tk.Tk()
window.title("Лабораторна робота №8 - Побудова графіків функцій")
window.geometry("820x640")

# Верхня панель керування (Frame + grid)
control_frame = tk.Frame(window, bg=BG_COLOR, padx=12, pady=10)
control_frame.pack(fill="x")

tk.Label(control_frame, text="Межа a:", bg=BG_COLOR).grid(
    row=0, column=0, sticky="e", padx=5, pady=4)
entry_a = tk.Entry(control_frame, width=12)
entry_a.insert(0, "3")
entry_a.grid(row=0, column=1, sticky="w", padx=5, pady=4)

tk.Label(control_frame, text="Межа b:", bg=BG_COLOR).grid(
    row=0, column=2, sticky="e", padx=5, pady=4)
entry_b = tk.Entry(control_frame, width=12)
entry_b.insert(0, "10")
entry_b.grid(row=0, column=3, sticky="w", padx=5, pady=4)

tk.Label(control_frame, text="f1(x) =", bg=BG_COLOR).grid(
    row=1, column=0, sticky="e", padx=5, pady=4)
entry_f1 = tk.Entry(control_frame, width=32)
entry_f1.insert(0, "(x**3 - 2) / (3 * log(x))")
entry_f1.grid(row=1, column=1, columnspan=3, sticky="we", padx=5, pady=4)

tk.Label(control_frame, text="f2(x) =", bg=BG_COLOR).grid(
    row=2, column=0, sticky="e", padx=5, pady=4)
entry_f2 = tk.Entry(control_frame, width=32)
entry_f2.insert(
    0, "0.3 * log10(exp(-x)) + (atan(x) - sin(x)**2) / "
       "(4 * sqrt(log(abs(x - 1))))")
entry_f2.grid(row=2, column=1, columnspan=3, sticky="we", padx=5, pady=4)

# Додаткові елементи керування: колір, товщина лінії, сітка
tk.Label(control_frame, text="Колір f1:", bg=BG_COLOR).grid(
    row=3, column=0, sticky="e", padx=5, pady=4)
color1_var = tk.StringVar(value="синій")
tk.OptionMenu(control_frame, color1_var, *COLORS.keys()).grid(
    row=3, column=1, sticky="we", padx=5, pady=4)

tk.Label(control_frame, text="Колір f2:", bg=BG_COLOR).grid(
    row=3, column=2, sticky="e", padx=5, pady=4)
color2_var = tk.StringVar(value="помаранчевий")
tk.OptionMenu(control_frame, color2_var, *COLORS.keys()).grid(
    row=3, column=3, sticky="we", padx=5, pady=4)

tk.Label(control_frame, text="Товщина:", bg=BG_COLOR).grid(
    row=4, column=0, sticky="e", padx=5, pady=4)
spin_width = tk.Spinbox(control_frame, from_=0.5, to=6, increment=0.5,
                        width=10)
spin_width.delete(0, "end")
spin_width.insert(0, "2")
spin_width.grid(row=4, column=1, sticky="w", padx=5, pady=4)

grid_var = tk.BooleanVar(value=True)
tk.Checkbutton(control_frame, text="Показувати сітку", variable=grid_var,
            bg=BG_COLOR).grid(row=4, column=2, columnspan=2,
                                sticky="w", padx=5, pady=4)

btn_plot = tk.Button(control_frame, text="ПОБУДУВАТИ ГРАФІКИ",
                    bg="#DCFCE7", command=build_plots)
btn_plot.grid(row=0, column=4, rowspan=3, padx=(15, 5), pady=4,
            sticky="nswe")

btn_exit = tk.Button(control_frame, text="ЗАВЕРШИТИ РОБОТУ",
                    bg="#FEE2E2", command=window.destroy)
btn_exit.grid(row=3, column=4, rowspan=2, padx=(15, 5), pady=4,
            sticky="nswe")

# Вбудоване полотно Matplotlib
fig = Figure(figsize=(7.0, 4.2), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

window.mainloop()