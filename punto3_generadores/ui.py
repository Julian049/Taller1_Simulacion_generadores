import tkinter as tk
from tkinter import filedialog
from punto3_generadores.generators import (
    mid_square, congruence, congruence_additive, congruence_multiplicative,
    uniform_mid_square, uniform_distribution_congruence,
    uniform_distribution_additive, uniform_distribution_multiplicative,
    normal_distribution_congruence, normal_distribution_mid_square,
)
from import_seeds import import_parameter_seeds, import_mid_square_seeds

FIELDS = {
    "cuadrados":            ["Semilla (X0)"],
    "congruencial":         ["Semilla (X0)", "Multiplicador (k)", "Incremento (c)", "Módulo (g)"],
    "aditivo":              ["Semilla (X0)", "Incremento (c)", "Módulo (g)"],
    "multiplicativo":       ["Semilla (X0)", "Multiplicador (k)", "Módulo (g)"],
    "uniforme_cuadrados":   ["Semilla (X0)", "Mínimo", "Máximo"],
    "uniforme_congruencial":["Semilla (X0)", "Multiplicador (k)", "Incremento (c)", "Módulo (g)", "Mínimo", "Máximo"],
    "uniforme_aditivo":     ["Semilla (X0)", "Incremento (c)", "Módulo (g)", "Mínimo", "Máximo"],
    "uniforme_multiplicativo": ["Semilla (X0)", "Multiplicador (k)", "Módulo (g)", "Mínimo", "Máximo"],
    # Distribución normal
    "normal_cuadrados":     ["Semilla (X0)", "Media (μ)", "Desv. estándar (σ)"],
    "normal_congruencial":  ["Semilla (X0)", "Multiplicador (k)", "Incremento (c)", "Módulo (g)", "Media (μ)", "Desv. estándar (σ)"],
}

NO_FILE_OPTIONS = {"aditivo", "multiplicativo", "uniforme_aditivo", "uniforme_multiplicativo"}


def select_file():
    file = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=(("CSV", "*.csv"), ("Todos", "*.*"))
    )
    if file:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file)

        filename = file.split("/")[-1]
        file_label.config(text=f"📄 {filename}")
        clear_file_btn.pack(side="left", padx=(0, 5))

        for e in entries.values():
            e.config(state="disabled")
    validate()


def clear_file():
    try:
        file_entry.delete(0, tk.END)
        file_label.config(text="")
        clear_file_btn.pack_forget()
        for e in entries.values():
            e.config(state="normal")
        validate()
    except tk.TclError:
        pass

    validate()


def update_fields(*args):
    for widget in fields_frame.winfo_children():
        widget.destroy()
    entries.clear()

    option = var_option.get()
    for name in FIELDS[option]:
        col = tk.Frame(fields_frame)
        col.pack(side="left", padx=10)
        tk.Label(col, text=f"{name}:").pack()
        e = tk.Entry(col, width=12)
        e.pack()
        entries[name] = e

    if option in NO_FILE_OPTIONS:
        load_btn.config(state="disabled")
    else:
        load_btn.config(state="normal")

    for e in entries.values():
        e.bind("<KeyRelease>", validate)
    clear_file()
    validate()


def validate(*args):
    amount = amount_entry.get().strip()
    file_path = file_entry.get().strip()
    option = var_option.get()

    all_fields_filled = all(e.get().strip() for e in entries.values())

    amount_ok = amount != ""

    inputs_ok = file_path != "" or all_fields_filled

    if option in NO_FILE_OPTIONS:
        inputs_ok = all_fields_filled

    if amount_ok and inputs_ok:
        run_btn.config(state="normal")
    else:
        run_btn.config(state="disabled")


def show_results_window(simulations, algorithm_name, amount):
    win = tk.Toplevel()
    win.title("Resultados")
    win.geometry("350x750")

    canvas = tk.Canvas(win)
    scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    container = tk.Frame(canvas)
    canvas.create_window((0, 0), window=container, anchor="nw")

    tk.Label(container, text="Números generados", font=("Arial", 12, "bold")).pack(pady=(15, 2))
    tk.Label(container, text=f"Algoritmo: {algorithm_name}").pack()
    tk.Label(container, text=f"Cantidad por simulación: {amount}").pack(pady=(0, 10))
    tk.Frame(container, height=1, bg="gray").pack(fill="x", padx=20, pady=5)

    for i, sim in enumerate(simulations, 1):
        block = tk.Frame(container, relief="groove", borderwidth=1)
        block.pack(fill="x", padx=15, pady=8)

        tk.Label(block, text=f"Simulación {i}", font=("Arial", 10, "bold")).pack(anchor="w", padx=8, pady=(5, 2))
        for key, val in sim["params"].items():
            tk.Label(block, text=f"  {key}: {val}").pack(anchor="w", padx=8)

        tk.Frame(block, height=1, bg="lightgray").pack(fill="x", padx=8, pady=4)

        listbox_frame = tk.Frame(block)
        listbox_frame.pack(fill="x", padx=8, pady=(0, 8))

        lb_scroll = tk.Scrollbar(listbox_frame)
        lb_scroll.pack(side="right", fill="y")

        listbox = tk.Listbox(listbox_frame, yscrollcommand=lb_scroll.set,
                             font=("Courier", 10), height=10)
        listbox.pack(fill="x")
        lb_scroll.config(command=listbox.yview)

        for j, num in enumerate(sim["numbers"], 1):
            listbox.insert(tk.END, f"  {j}.  {num}")

    container.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


def run():
    option = var_option.get()
    file_path = file_entry.get()
    amount = int(amount_entry.get())
    simulations = []
    algorithm_name = ""

    match option:
        case "cuadrados":
            algorithm_name = "Cuadrados medios"
            if file_path:
                seeds = import_mid_square_seeds(file_path)
            else:
                seeds = [int(entries["Semilla (X0)"].get())]

            for seed in seeds:
                numbers = mid_square(seed, amount)
                simulations.append({
                    "params": {"Semilla (X0)": seed},
                    "numbers": numbers
                })

        case "congruencial":
            algorithm_name = "Congruencial"
            if file_path:
                params_list = import_parameter_seeds(file_path)
            else:
                params_list = [{
                    "xo": entries["Semilla (X0)"].get(),
                    "k": entries["Multiplicador (k)"].get(),
                    "c": entries["Incremento (c)"].get(),
                    "g": entries["Módulo (g)"].get()
                }]

            for p in params_list:
                numbers = congruence(int(p["xo"]), int(p["k"]), int(p["c"]), int(p["g"]), amount)
                simulations.append({
                    "params": {"Semilla (X0)": p["xo"], "Multiplicador (k)": p["k"],
                               "Incremento (c)": p["c"], "Módulo (g)": p["g"]},
                    "numbers": numbers
                })

        case "aditivo":
            algorithm_name = "Congruencial aditivo"
            seed = int(entries["Semilla (X0)"].get())
            increment = int(entries["Incremento (c)"].get())
            modulus = int(entries["Módulo (g)"].get())
            numbers = congruence_additive(seed, increment, modulus, amount)
            simulations.append({
                "params": {"Semilla (X0)": seed, "Incremento (c)": increment, "Módulo (g)": modulus},
                "numbers": numbers
            })

        case "multiplicativo":
            algorithm_name = "Congruencial multiplicativo"
            seed = int(entries["Semilla (X0)"].get())
            multiplier = int(entries["Multiplicador (k)"].get())
            modulus = int(entries["Módulo (g)"].get())
            numbers = congruence_multiplicative(seed, multiplier, modulus, amount)
            simulations.append({
                "params": {"Semilla (X0)": seed, "Multiplicador (k)": multiplier, "Módulo (g)": modulus},
                "numbers": numbers
            })

        case "uniforme_cuadrados":
            algorithm_name = "Uniforme – Cuadrados medios"

            if file_path:
                params_list = import_parameter_seeds(file_path)
            else:
                params_list = [{
                    "seed": entries["Semilla (X0)"].get(),
                    "min": entries["Mínimo"].get(),
                    "max": entries["Máximo"].get(),
                }]

            for p in params_list:
                seed = int(p["seed"])
                range_min = float(p["min"])
                range_max = float(p["max"])
                numbers = uniform_mid_square(seed, range_min, range_max, amount)
                simulations.append({
                    "params": {"Semilla (X0)": seed, "Mínimo": range_min, "Máximo": range_max},
                    "numbers": numbers
                })

        case "uniforme_congruencial":
            algorithm_name = "Uniforme – Congruencial"

            if file_path:
                params_list = import_parameter_seeds(file_path)
            else:
                params_list = [{
                    "xo": entries["Semilla (X0)"].get(),
                    "k": entries["Multiplicador (k)"].get(),
                    "c": entries["Incremento (c)"].get(),
                    "g": entries["Módulo (g)"].get(),
                    "min": entries["Mínimo"].get(),
                    "max": entries["Máximo"].get(),
                }]

            for p in params_list:
                range_min = float(p["min"])
                range_max = float(p["max"])
                numbers = uniform_distribution_congruence(
                    int(p["xo"]), int(p["k"]), int(p["c"]), int(p["g"]),
                    range_min, range_max, amount
                )
                simulations.append({
                    "params": {
                        "Semilla (X0)": p["xo"], "Multiplicador (k)": p["k"],
                        "Incremento (c)": p["c"], "Módulo (g)": p["g"],
                        "Mínimo": range_min, "Máximo": range_max,
                    },
                    "numbers": numbers
                })

        case "uniforme_aditivo":
            algorithm_name = "Uniforme – Congruencial aditivo"
            seed = int(entries["Semilla (X0)"].get())
            increment = int(entries["Incremento (c)"].get())
            modulus = int(entries["Módulo (g)"].get())
            range_min = float(entries["Mínimo"].get())
            range_max = float(entries["Máximo"].get())
            numbers = uniform_distribution_additive(seed, increment, modulus, range_min, range_max, amount)
            simulations.append({
                "params": {
                    "Semilla (X0)": seed, "Incremento (c)": increment, "Módulo (g)": modulus,
                    "Mínimo": range_min, "Máximo": range_max,
                },
                "numbers": numbers
            })

        case "uniforme_multiplicativo":
            algorithm_name = "Uniforme – Congruencial multiplicativo"
            seed = int(entries["Semilla (X0)"].get())
            multiplier = int(entries["Multiplicador (k)"].get())
            modulus = int(entries["Módulo (g)"].get())
            range_min = float(entries["Mínimo"].get())
            range_max = float(entries["Máximo"].get())
            numbers = uniform_distribution_multiplicative(seed, multiplier, modulus, range_min, range_max, amount)
            simulations.append({
                "params": {
                    "Semilla (X0)": seed, "Multiplicador (k)": multiplier, "Módulo (g)": modulus,
                    "Mínimo": range_min, "Máximo": range_max,
                },
                "numbers": numbers
            })

        case "normal_cuadrados":
            algorithm_name = "Normal – Cuadrados medios (Box-Muller)"
            if file_path:
                params_list = import_parameter_seeds(file_path)
            else:
                params_list = [{
                    "seed":    entries["Semilla (X0)"].get(),
                    "mean":    entries["Media (μ)"].get(),
                    "std_dev": entries["Desv. estándar (σ)"].get(),
                }]

            for p in params_list:
                seed = int(p["seed"])
                mean = float(p["mean"])
                std_dev = float(p["std_dev"])
                numbers = normal_distribution_mid_square(seed, mean, std_dev, amount)
                simulations.append({
                    "params": {
                        "Semilla (X0)": seed,
                        "Media (μ)": mean,
                        "Desv. estándar (σ)": std_dev,
                    },
                    "numbers": numbers
                })

        case "normal_congruencial":
            algorithm_name = "Normal – Congruencial (Box-Muller)"
            if file_path:
                params_list = import_parameter_seeds(file_path)
            else:
                params_list = [{
                    "xo":      entries["Semilla (X0)"].get(),
                    "k":       entries["Multiplicador (k)"].get(),
                    "c":       entries["Incremento (c)"].get(),
                    "g":       entries["Módulo (g)"].get(),
                    "mean":    entries["Media (μ)"].get(),
                    "std_dev": entries["Desv. estándar (σ)"].get(),
                }]

            for p in params_list:
                mean = float(p["mean"])
                std_dev = float(p["std_dev"])
                numbers = normal_distribution_congruence(
                    int(p["xo"]), int(p["k"]), int(p["c"]), int(p["g"]),
                    mean, std_dev, amount
                )
                simulations.append({
                    "params": {
                        "Semilla (X0)": p["xo"], "Multiplicador (k)": p["k"],
                        "Incremento (c)": p["c"], "Módulo (g)": p["g"],
                        "Media (μ)": mean, "Desv. estándar (σ)": std_dev,
                    },
                    "numbers": numbers
                })

    show_results_window(simulations, algorithm_name, amount)


def main():
    global fields_frame, entries, file_entry, var_option, amount_entry, load_btn, run_btn, file_label, clear_file_btn

    root = tk.Tk()
    root.title("Generadores de números pseudoaleatorios")
    root.geometry("980x380")

    entries = {}

    selector_frame = tk.Frame(root)
    selector_frame.pack(pady=(10, 0), anchor="w", padx=20)

    var_option = tk.StringVar(value="cuadrados")

    # ── Generadores base ──────────────────────────────────────────────────────
    base_frame = tk.LabelFrame(selector_frame, text="Generadores base", padx=8, pady=4)
    base_frame.pack(side="left", padx=(0, 15), anchor="n")

    base_options = [
        ("Cuadrados medios",           "cuadrados"),
        ("Congruencial",               "congruencial"),
        ("Congruencial aditivo",       "aditivo"),
        ("Congruencial multiplicativo","multiplicativo"),
    ]
    for label, value in base_options:
        tk.Radiobutton(base_frame, text=label, variable=var_option,
                       value=value, command=update_fields).pack(anchor="w")

    # ── Distribución uniforme ─────────────────────────────────────────────────
    uni_frame = tk.LabelFrame(selector_frame, text="Distribución uniforme", padx=8, pady=4)
    uni_frame.pack(side="left", padx=(0, 15), anchor="n")

    uni_options = [
        ("Cuadrados medios",           "uniforme_cuadrados"),
        ("Congruencial",               "uniforme_congruencial"),
        ("Congruencial aditivo",       "uniforme_aditivo"),
        ("Congruencial multiplicativo","uniforme_multiplicativo"),
    ]
    for label, value in uni_options:
        tk.Radiobutton(uni_frame, text=label, variable=var_option,
                       value=value, command=update_fields).pack(anchor="w")

    # ── Distribución normal (Box-Muller) ──────────────────────────────────────
    norm_frame = tk.LabelFrame(selector_frame, text="Distribución normal", padx=8, pady=4)
    norm_frame.pack(side="left", anchor="n")

    norm_options = [
        ("Cuadrados medios", "normal_cuadrados"),
        ("Congruencial",     "normal_congruencial"),
    ]
    for label, value in norm_options:
        tk.Radiobutton(norm_frame, text=label, variable=var_option,
                       value=value, command=update_fields).pack(anchor="w")

    # ── Cantidad ──────────────────────────────────────────────────────────────
    amount_frame = tk.Frame(root)
    amount_frame.pack(pady=(8, 0))
    tk.Label(amount_frame, text="Cantidad de números a generar:").pack(side="left", padx=(0, 5))
    amount_entry = tk.Entry(amount_frame, width=6)
    amount_entry.pack(side="left")
    amount_entry.bind("<KeyRelease>", validate)

    fields_frame = tk.Frame(root)
    fields_frame.pack(pady=10)

    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=6)

    file_entry = tk.Entry(root)
    file_entry.pack_forget()

    load_btn = tk.Button(buttons_frame, text="Cargar archivo", command=select_file, width=15)
    load_btn.pack(side="left", padx=10)
    run_btn = tk.Button(buttons_frame, text="Ejecutar", command=run, width=15, state="disabled")
    run_btn.pack(side="left", padx=10)

    file_status_frame = tk.Frame(root)
    file_status_frame.pack(pady=(0, 5))

    file_label = tk.Label(file_status_frame, text="", fg="green")
    file_label.pack(side="left", padx=(0, 5))

    clear_file_btn = tk.Button(file_status_frame, text="✕", command=clear_file,
                               width=2, fg="red", relief="flat")

    update_fields()
    root.mainloop()


if __name__ == "__main__":
    main()