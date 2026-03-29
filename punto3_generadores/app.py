"""
=============================================================
SIMULACIÓN POR COMPUTADOR - UPTC
Módulo integrado: Generadores + Validación Estadística
=============================================================
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import threading
import csv
import os

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False

try:
    from scipy.stats import chi2 as scipy_chi2, norm as scipy_norm
    SCIPY_OK = True
except ImportError:
    SCIPY_OK = False

from generators import (
    mid_square, congruence, congruence_additive,
    congruence_multiplicative, general_uniform,
    normal_distribution_congruence, normal_distribution_mid_square
)
from import_seeds import import_parameter_seeds, import_mid_square_seeds

# ══════════════════════════════════════════════════════════
#  PRUEBAS ESTADÍSTICAS
# ══════════════════════════════════════════════════════════

from prueba_medias import prueba_medias
from prueba_varianza import prueba_varianza
from prueba_chi_cuadrado import prueba_chi_cuadrado
from prueba_ks import prueba_ks
from prueba_poker import prueba_poker
from prueba_rachas import prueba_rachas

# ══════════════════════════════════════════════════════════
#  PALETA
# ══════════════════════════════════════════════════════════
BG      = "#0D1117"
SIDEBAR = "#161B22"
CARD    = "#21262D"
CARD2   = "#2D333B"
ACCENT  = "#58A6FF"
GREEN   = "#3FB950"
RED     = "#F85149"
YELLOW  = "#D29922"
TEXT    = "#E6EDF3"
SUBTEXT = "#8B949E"
BORDER  = "#30363D"
WHITE   = "#FFFFFF"

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_HEADER = ("Segoe UI", 12, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_MONO   = ("Consolas", 10)
FONT_SMALL  = ("Consolas", 9)


# ══════════════════════════════════════════════════════════
#  SCROLLABLE FRAME
# ══════════════════════════════════════════════════════════
class ScrollFrame(tk.Frame):
    def __init__(self, parent, bg=SIDEBAR, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self._canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self.inner = tk.Frame(self._canvas, bg=bg)

        self.inner.bind("<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self._canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._canvas.bind("<MouseWheel>",
            lambda e: self._canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.inner.bind("<MouseWheel>",
            lambda e: self._canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def refresh(self):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))


# ══════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════
def make_entry(parent, default="", width=12, bg=CARD):
    e = tk.Entry(parent, font=FONT_MONO, bg=bg, fg=TEXT,
                 insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightcolor=ACCENT,
                 highlightbackground=BORDER, width=width)
    e.insert(0, default)
    return e

def make_btn(parent, text, cmd, color=ACCENT, fg=WHITE):
    return tk.Button(parent, text=text, command=cmd, bg=color, fg=fg,
                     font=("Segoe UI", 10, "bold"), relief="flat",
                     cursor="hand2", activebackground=color,
                     activeforeground=fg, pady=7, padx=14)

def sep(parent, bg=BORDER, pad=8):
    tk.Frame(parent, bg=bg, height=1).pack(fill="x", padx=16, pady=pad)

def section_label(parent, text):
    tk.Label(parent, text=text, bg=SIDEBAR, fg=ACCENT,
             font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=16, pady=(10, 2))


# ══════════════════════════════════════════════════════════
#  APP
# ══════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SimLab · UPTC — Generadores Pseudoaleatorios")
        self.geometry("1300x840")
        self.minsize(1100, 700)
        self.configure(bg=BG)

        self._secuencia        = []
        self._secuencias_gen   = []
        self._resultados       = {}
        self._resultados_por_seq = []
        self._nombre_gen       = ""
        self._file_path  = tk.StringVar()
        self._entries    = {}

        self._build()

    # ──────────────────────────────────────────────────────
    def _build(self):
        # Topbar
        topbar = tk.Frame(self, bg="#1C2128", height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Label(topbar, text="◈  SimLab", bg="#1C2128", fg=ACCENT,
                 font=("Segoe UI", 16, "bold")).pack(side="left", padx=20, pady=10)
        tk.Label(topbar,
                 text="Generadores Pseudoaleatorios  ·  Validación Estadística  ·  UPTC",
                 bg="#1C2128", fg=SUBTEXT, font=FONT_BODY).pack(side="left")

        # Cuerpo
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar_wrap = tk.Frame(body, bg=SIDEBAR, width=330)
        sidebar_wrap.pack(side="left", fill="y")
        sidebar_wrap.pack_propagate(False)

        self._scroll = ScrollFrame(sidebar_wrap, bg=SIDEBAR)
        self._scroll.pack(fill="both", expand=True)
        self._panel = self._scroll.inner

        self._build_sidebar()

        # Contenido
        content = tk.Frame(body, bg=BG)
        content.pack(side="left", fill="both", expand=True, padx=12, pady=12)
        self._build_content(content)

    # ──────────────────────────────────────────────────────
    def _build_sidebar(self):
        p = self._panel

        tk.Label(p, text="Configuración", bg=SIDEBAR, fg=WHITE,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=16, pady=(16, 6))
        sep(p, pad=0)

        # ① Generador
        section_label(p, "① Generador")
        gen_f = tk.Frame(p, bg=SIDEBAR)
        gen_f.pack(fill="x", padx=16, pady=(4, 8))

        self._gen_var = tk.StringVar(value="congruencial")
        for txt, val in [
            ("Congruencial Mixto",              "congruencial"),
            ("Cuadrados Medios",                "cuadrados"),
            ("Uniforme Congruencial",           "uniforme_cong"),
            ("Uniforme Cuadrados Medios",       "uniforme_ms"),
            ("Normal Congruencial",             "normal_cong"),
            ("Normal Cuadrados Medios",         "normal_ms"),
        ]:
            tk.Radiobutton(gen_f, text=txt, variable=self._gen_var, value=val,
                           command=self._update_params,
                           bg=SIDEBAR, fg=TEXT, selectcolor=ACCENT,
                           activebackground=SIDEBAR, font=FONT_BODY,
                           anchor="w").pack(fill="x", pady=2)

        sep(p)

        # ② Parámetros
        section_label(p, "② Parámetros")
        self._params_container = tk.Frame(p, bg=SIDEBAR)
        self._params_container.pack(fill="x", padx=16, pady=(4, 8))
        self._update_params()

        sep(p)

        # ③ Cantidad
        section_label(p, "③ Cantidad de números (N)")
        qf = tk.Frame(p, bg=SIDEBAR)
        qf.pack(fill="x", padx=16, pady=(4, 8))
        self._n_entry = make_entry(qf, "300", width=14)
        self._n_entry.pack(anchor="w")

        sep(p)

        # ④ Archivo
        section_label(p, "④ Semillas desde archivo")
        ff = tk.Frame(p, bg=SIDEBAR)
        ff.pack(fill="x", padx=16, pady=(4, 8))
        self._file_lbl = tk.Label(ff, text="Sin archivo cargado",
                                  bg=SIDEBAR, fg=SUBTEXT, font=FONT_SMALL)
        self._file_lbl.pack(anchor="w", pady=(0, 6))
        row = tk.Frame(ff, bg=SIDEBAR)
        row.pack(fill="x")
        make_btn(row, "📂 Cargar", self._load_file, CARD2, TEXT).pack(side="left")
        make_btn(row, "✕ Quitar", self._clear_file, RED).pack(side="left", padx=(6, 0))

        sep(p)

        # ⑤ Pruebas
        section_label(p, "⑤ Pruebas estadísticas")
        pf = tk.Frame(p, bg=SIDEBAR)
        pf.pack(fill="x", padx=16, pady=(4, 8))

        ctrl = tk.Frame(pf, bg=SIDEBAR)
        ctrl.pack(fill="x", pady=(0, 6))
        for txt, val in [("Todas", True), ("Ninguna", False)]:
            tk.Button(ctrl, text=txt,
                      command=lambda v=val: self._toggle_pruebas(v),
                      bg=CARD2, fg=TEXT, font=FONT_SMALL,
                      relief="flat", cursor="hand2",
                      padx=8, pady=3).pack(side="left", padx=(0, 4))

        self._prueba_vars = {}
        for p_name in ["Medias", "Varianza", "Chi-Cuadrado",
                       "Kolmogorov-Smirnov", "Póker", "Rachas"]:
            v = tk.BooleanVar(value=True)
            self._prueba_vars[p_name] = v
            f = tk.Frame(pf, bg=CARD, pady=5, padx=10)
            f.pack(fill="x", pady=2)
            tk.Checkbutton(f, text=p_name, variable=v,
                           bg=CARD, fg=TEXT, selectcolor=ACCENT,
                           activebackground=CARD,
                           font=FONT_BODY).pack(anchor="w")

        sep(p)

        # Botones
        bf = tk.Frame(p, bg=SIDEBAR)
        bf.pack(fill="x", padx=16, pady=(4, 6))
        make_btn(bf, "▶  Ejecutar simulación",
                 self._ejecutar, GREEN).pack(fill="x", pady=(0, 6))
        make_btn(bf, "⬇  Exportar secuencia CSV",
                 self._exportar_csv, CARD2, TEXT).pack(fill="x")

        # Status
        self._status_lbl = tk.Label(p, text="Listo para ejecutar.",
                                    bg=SIDEBAR, fg=SUBTEXT, font=FONT_SMALL,
                                    wraplength=290, justify="left")
        self._status_lbl.pack(padx=16, pady=(8, 20), anchor="w")

        self._scroll.refresh()

    # ──────────────────────────────────────────────────────
    def _build_content(self, parent):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("T.TNotebook", background=BG, borderwidth=0)
        style.configure("T.TNotebook.Tab", background=CARD,
                        foreground=SUBTEXT, font=("Segoe UI", 10), padding=[16, 8])
        style.map("T.TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", WHITE)])

        self._nb = ttk.Notebook(parent, style="T.TNotebook")
        self._nb.pack(fill="both", expand=True)

        # Pestaña Generador (nueva — primera)
        self._tab_gen = tk.Frame(self._nb, bg=BG)
        self._nb.add(self._tab_gen, text="  🎲 Generador  ")
        self._gen_scroll = ScrollFrame(self._tab_gen, bg=BG)
        self._gen_scroll.pack(fill="both", expand=True)
        self._gen_inner = self._gen_scroll.inner
        tk.Label(self._gen_inner,
                 text="Ejecuta una simulación para ver los resultados del generador.",
                 bg=BG, fg=SUBTEXT, font=FONT_BODY).pack(pady=60)

        # Pestaña Resumen
        self._tab_res = tk.Frame(self._nb, bg=BG)
        self._nb.add(self._tab_res, text="  📊 Resumen  ")
        self._res_scroll = ScrollFrame(self._tab_res, bg=BG)
        self._res_scroll.pack(fill="both", expand=True)
        self._res_inner = self._res_scroll.inner
        tk.Label(self._res_inner,
                 text="Ejecuta una simulación para ver los resultados.",
                 bg=BG, fg=SUBTEXT, font=FONT_BODY).pack(pady=60)

        # Pestaña Secuencia
        self._tab_seq = tk.Frame(self._nb, bg=BG)
        self._nb.add(self._tab_seq, text="  🔢 Secuencia  ")
        self._build_tab_seq(self._tab_seq)

        # Pestaña Gráficos
        self._tab_graf = tk.Frame(self._nb, bg=BG)
        self._nb.add(self._tab_graf, text="  📈 Gráficos  ")

        # Canvas con scroll vertical y horizontal
        self._graf_canvas = tk.Canvas(self._tab_graf, bg=BG,
                                      highlightthickness=0, bd=0)
        _sby = tk.Scrollbar(self._tab_graf, orient="vertical",
                            command=self._graf_canvas.yview)
        _sbx = tk.Scrollbar(self._tab_graf, orient="horizontal",
                            command=self._graf_canvas.xview)
        self._graf_inner = tk.Frame(self._graf_canvas, bg=BG)

        self._graf_inner.bind(
            "<Configure>",
            lambda e: self._graf_canvas.configure(
                scrollregion=self._graf_canvas.bbox("all")))

        self._graf_canvas.create_window((0, 0), window=self._graf_inner, anchor="nw")
        self._graf_canvas.configure(yscrollcommand=_sby.set,
                                    xscrollcommand=_sbx.set)

        _sby.pack(side="right", fill="y")
        _sbx.pack(side="bottom", fill="x")
        self._graf_canvas.pack(side="left", fill="both", expand=True)

        # Scroll con rueda del ratón (vertical)
        self._graf_canvas.bind(
            "<MouseWheel>",
            lambda e: self._graf_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self._graf_inner.bind(
            "<MouseWheel>",
            lambda e: self._graf_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        tk.Label(self._graf_inner,
                 text="Los gráficos aparecerán aquí.",
                 bg=BG, fg=SUBTEXT, font=FONT_BODY).pack(pady=60)

    def _build_tab_seq(self, parent):
        tk.Label(parent, text="Secuencia generada — primeros 500 números",
                 bg=BG, fg=SUBTEXT, font=FONT_SMALL).pack(anchor="w", padx=16, pady=(10, 4))
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        sy = tk.Scrollbar(frame); sy.pack(side="right", fill="y")
        sx = tk.Scrollbar(frame, orient="horizontal"); sx.pack(side="bottom", fill="x")
        self._seq_text = tk.Text(frame, bg=CARD, fg=TEXT, font=FONT_MONO,
                                 yscrollcommand=sy.set, xscrollcommand=sx.set,
                                 relief="flat", state="disabled",
                                 selectbackground=ACCENT)
        self._seq_text.pack(fill="both", expand=True)
        sy.config(command=self._seq_text.yview)
        sx.config(command=self._seq_text.xview)

    # ──────────────────────────────────────────────────────
    def _update_params(self):
        for w in self._params_container.winfo_children():
            w.destroy()
        self._entries.clear()

        defs = {
            "congruencial":  [("Semilla (X0)", "7"), ("Multiplicador k", "100"),
                              ("Incremento c", "21"), ("Módulo g", "12")],
            "cuadrados":     [("Semilla", "5678")],
            "uniforme_cong": [("Semilla (X0)", "7"), ("Multiplicador k", "100"),
                              ("Incremento c", "21"), ("Módulo g", "12"),
                              ("Mínimo", "4"), ("Máximo", "100")],
            "uniforme_ms":   [("Semilla", "5678"),
                              ("Mínimo", "4"), ("Máximo", "100")],
            "normal_cong":   [("Semilla (X0)", "7"), ("Multiplicador k", "100"),
                              ("Incremento c", "21"), ("Módulo g", "12"),
                              ("Media (μ)", "3.5"), ("Desv. estándar (σ)", "0.4")],
            "normal_ms":     [("Semilla", "5678"),
                              ("Media (μ)", "3.5"), ("Desv. estándar (σ)", "0.4")],
        }
        for label, default in defs.get(self._gen_var.get(), []):
            row = tk.Frame(self._params_container, bg=SIDEBAR)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, bg=SIDEBAR, fg=SUBTEXT,
                     font=FONT_SMALL, width=20, anchor="w").pack(side="left")
            e = make_entry(row, default, width=10)
            e.pack(side="left")
            self._entries[label] = e

        self._scroll.refresh()

    def _toggle_pruebas(self, estado):
        for v in self._prueba_vars.values():
            v.set(estado)

    # Columnas requeridas por generador
    _CSV_COLS = {
        "congruencial":  {"xo", "k", "c", "g"},
        "cuadrados":     {"seed"},
        "uniforme_cong": {"xo", "k", "c", "g", "min", "max"},
        "uniforme_ms":   {"seed", "min", "max"},
        "normal_cong":   {"xo", "k", "c", "g", "mean", "std_dev"},
        "normal_ms":     {"seed", "mean", "std_dev"},
    }

    def _load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("CSV / TXT", "*.csv *.txt"), ("Todos", "*.*")])
        if not path:
            return
        # Validar columnas del CSV contra el generador seleccionado
        try:
            import csv as _csv
            with open(path, newline="", encoding="utf-8") as f:
                cols = set(next(_csv.DictReader(f)).keys())
            gen = self._gen_var.get()
            required = self._CSV_COLS.get(gen, set())
            missing = required - cols
            if missing:
                messagebox.showerror(
                    "Archivo incompatible",
                    "Requiere columnas: " + str(sorted(required)) +
                    "\nTiene: " + str(sorted(cols)) +
                    "\nFaltan: " + str(sorted(missing)))
                return
        except Exception as ve:
            messagebox.showerror("Error al leer archivo", str(ve))
            return
        self._file_path.set(path)
        self._file_lbl.config(text=f"📄 {os.path.basename(path)}", fg=GREEN)

    def _clear_file(self):
        self._file_path.set("")
        self._file_lbl.config(text="Sin archivo cargado", fg=SUBTEXT)

    def _status(self, msg, color=SUBTEXT):
        self._status_lbl.config(text=msg, fg=color)

    # ──────────────────────────────────────────────────────
    def _ejecutar(self):
        self._status("⏳ Generando secuencia...", YELLOW)
        self.update()
        threading.Thread(target=self._run_logic, daemon=True).start()

    def _run_logic(self):
        try:
            n   = int(self._n_entry.get())
            gen = self._gen_var.get()
            e   = self._entries
            fp  = self._file_path.get()

            # ── Construir lista de secuencias: [(etiqueta, seq), ...]
            secuencias = []

            # ── congruence.csv: xo, k, c, g
            if gen == "congruencial":
                self._nombre_gen = "Congruencial Mixto"
                if fp:
                    params = import_parameter_seeds(fp)
                    for p in params:
                        seq = congruence(int(p["xo"]), int(p["k"]),
                                         int(p["c"]), int(p["g"]), n)
                        secuencias.append(
                            (f"xo={p['xo']} k={p['k']} c={p['c']} g={p['g']}", seq))
                else:
                    seq = congruence(int(e["Semilla (X0)"].get()),
                                     int(e["Multiplicador k"].get()),
                                     int(e["Incremento c"].get()),
                                     int(e["Módulo g"].get()), n)
                    secuencias.append(("Secuencia", seq))

            # ── mid_square.csv: seed
            elif gen == "cuadrados":
                self._nombre_gen = "Cuadrados Medios"
                if fp:
                    params = import_parameter_seeds(fp)
                    for p in params:
                        seq = mid_square(int(p["seed"]), n)
                        secuencias.append((f"Semilla {p['seed']}", seq))
                else:
                    seq = mid_square(int(e["Semilla"].get()), n)
                    secuencias.append(("Secuencia", seq))

            # ── uniform_congruence.csv: xo, k, c, g, min, max
            elif gen == "uniforme_cong":
                self._nombre_gen = "Uniforme Congruencial"
                if fp:
                    params = import_parameter_seeds(fp)
                    for p in params:
                        base = congruence(int(p["xo"]), int(p["k"]),
                                          int(p["c"]), int(p["g"]), n)
                        seq = general_uniform(base, float(p["min"]), float(p["max"]))
                        secuencias.append(
                            (f"xo={p['xo']} [{p['min']},{p['max']}]", seq))
                else:
                    base = congruence(int(e["Semilla (X0)"].get()),
                                      int(e["Multiplicador k"].get()),
                                      int(e["Incremento c"].get()),
                                      int(e["Módulo g"].get()), n)
                    seq = general_uniform(base, float(e["Mínimo"].get()),
                                          float(e["Máximo"].get()))
                    secuencias.append(("Secuencia", seq))

            # ── uniform_mid_square.csv: seed, min, max
            elif gen == "uniforme_ms":
                self._nombre_gen = "Uniforme Cuadrados Medios"
                if fp:
                    params = import_parameter_seeds(fp)
                    for p in params:
                        base = mid_square(int(p["seed"]), n)
                        seq = general_uniform(base, float(p["min"]), float(p["max"]))
                        secuencias.append(
                            (f"seed={p['seed']} [{p['min']},{p['max']}]", seq))
                else:
                    base = mid_square(int(e["Semilla"].get()), n)
                    seq = general_uniform(base, float(e["Mínimo"].get()),
                                          float(e["Máximo"].get()))
                    secuencias.append(("Secuencia", seq))

            # ── normal_congruence.csv: xo, k, c, g, mean, std_dev
            elif gen == "normal_cong":
                self._nombre_gen = "Normal Congruencial (Box-Muller)"
                n_par = n if n % 2 == 0 else n + 1
                if fp:
                    params = import_parameter_seeds(fp)
                    for p in params:
                        seq_n = normal_distribution_congruence(
                            int(p["xo"]), int(p["k"]), int(p["c"]), int(p["g"]),
                            float(p["mean"]), float(p["std_dev"]), n_par)[:n]
                        mn, mx = min(seq_n), max(seq_n)
                        seq = [(x-mn)/(mx-mn) for x in seq_n] if mx != mn else seq_n
                        secuencias.append(
                            (f"xo={p['xo']} μ={p['mean']} σ={p['std_dev']}", seq))
                else:
                    seq_n = normal_distribution_congruence(
                        int(e["Semilla (X0)"].get()),
                        int(e["Multiplicador k"].get()),
                        int(e["Incremento c"].get()),
                        int(e["Módulo g"].get()),
                        float(e["Media (μ)"].get()),
                        float(e["Desv. estándar (σ)"].get()),
                        n_par)[:n]
                    mn, mx = min(seq_n), max(seq_n)
                    seq = [(x-mn)/(mx-mn) for x in seq_n] if mx != mn else seq_n
                    secuencias.append(("Secuencia", seq))

            # ── normal_mid_square.csv: seed, mean, std_dev
            elif gen == "normal_ms":
                self._nombre_gen = "Normal Cuadrados Medios (Box-Muller)"
                n_par = n if n % 2 == 0 else n + 1
                if fp:
                    params = import_parameter_seeds(fp)
                    for p in params:
                        seq_n = normal_distribution_mid_square(
                            int(p["seed"]),
                            float(p["mean"]), float(p["std_dev"]), n_par)[:n]
                        mn, mx = min(seq_n), max(seq_n)
                        seq = [(x-mn)/(mx-mn) for x in seq_n] if mx != mn else seq_n
                        secuencias.append(
                            (f"seed={p['seed']} μ={p['mean']} σ={p['std_dev']}", seq))
                else:
                    seq_n = normal_distribution_mid_square(
                        int(e["Semilla"].get()),
                        float(e["Media (μ)"].get()),
                        float(e["Desv. estándar (σ)"].get()),
                        n_par)[:n]
                    mn, mx = min(seq_n), max(seq_n)
                    seq = [(x-mn)/(mx-mn) for x in seq_n] if mx != mn else seq_n
                    secuencias.append(("Secuencia", seq))

            # ── Usar la primera secuencia para la pestaña Secuencia/Gráficos
            self._secuencia = secuencias[0][1] if secuencias else []
            self._secuencias_gen = secuencias  # todas las (lbl, seq) para la pestana generador
            total_nums = sum(len(s) for _, s in secuencias)
            self._status(
                f"✅ {total_nums:,} números en {len(secuencias)} secuencia(s). "
                f"Ejecutando pruebas...", GREEN)
            self.update()

            # ── Correr pruebas por cada secuencia
            # _resultados_por_seq: lista de (etiqueta, dict_resultados)
            self._resultados_por_seq = []
            for lbl, seq in secuencias:
                res = {}
                if self._prueba_vars["Medias"].get():
                    res["Medias"] = prueba_medias(seq)
                if self._prueba_vars["Varianza"].get():
                    res["Varianza"] = prueba_varianza(seq)
                if self._prueba_vars["Chi-Cuadrado"].get():
                    res["Chi-Cuadrado"] = prueba_chi_cuadrado(seq)
                if self._prueba_vars["Kolmogorov-Smirnov"].get():
                    res["Kolmogorov-Smirnov"] = prueba_ks(seq)
                if self._prueba_vars["Póker"].get():
                    res["Póker"] = prueba_poker(seq)
                if self._prueba_vars["Rachas"].get():
                    res["Rachas"] = prueba_rachas(seq)
                self._resultados_por_seq.append((lbl, res))

            # Mantener _resultados apuntando a la primera para compatibilidad con gráficos
            self._resultados = self._resultados_por_seq[0][1] if self._resultados_por_seq else {}
            self.after(0, self._mostrar_resultados)

        except Exception as ex:
            import traceback
            tb = traceback.format_exc()
            def _show_err(msg=str(ex), detail=tb):
                self._status(f"❌ Error: {msg}", RED)
                from tkinter import messagebox
                messagebox.showerror("Error al ejecutar", detail)
            self.after(0, _show_err)

    # ──────────────────────────────────────────────────────
    def _mostrar_resultados(self):
        for w in self._res_inner.winfo_children():
            w.destroy()

        n_seqs = len(self._resultados_por_seq)

        # Totales globales
        total_aprobadas = sum(
            sum(1 for r in res.values() if r["aprueba"])
            for _, res in self._resultados_por_seq)
        total_pruebas = sum(
            len(res) for _, res in self._resultados_por_seq)
        color_tot = GREEN if total_aprobadas == total_pruebas else (
                    YELLOW if total_aprobadas >= total_pruebas // 2 else RED)

        # Header global
        hdr = tk.Frame(self._res_inner, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(16, 4))
        tk.Label(hdr, text=self._nombre_gen, bg=BG, fg=WHITE,
                 font=FONT_TITLE).pack(anchor="w")
        info = (f"{n_seqs} secuencia(s)  ·  N = {len(self._secuencia):,} por secuencia"
                if n_seqs > 1 else
                f"N = {len(self._secuencia):,} números generados")
        tk.Label(hdr, text=info, bg=BG, fg=SUBTEXT, font=FONT_BODY).pack(anchor="w")

        sf = tk.Frame(self._res_inner, bg=BG)
        sf.pack(fill="x", padx=20, pady=(8, 4))
        tk.Label(sf, text=f"{total_aprobadas}/{total_pruebas} pruebas aprobadas (total)",
                 bg=BG, fg=color_tot,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w")

        bar_bg = tk.Frame(self._res_inner, bg=CARD, height=8)
        bar_bg.pack(fill="x", padx=20, pady=(0, 16))
        bar_bg.pack_propagate(False)
        if total_pruebas > 0:
            tk.Frame(bar_bg, bg=color_tot, height=8).place(
                relwidth=total_aprobadas / total_pruebas, relheight=1)

        tk.Frame(self._res_inner, bg=BORDER, height=1).pack(
            fill="x", padx=20, pady=(0, 8))

        # Una sección por cada secuencia
        for seq_idx, (lbl, resultados) in enumerate(self._resultados_por_seq):
            aprobadas = sum(1 for r in resultados.values() if r["aprueba"])
            total     = len(resultados)
            c_sec = GREEN if aprobadas == total else (
                    YELLOW if aprobadas >= total // 2 else RED)

            # Encabezado de la secuencia
            sec_hdr = tk.Frame(self._res_inner, bg=CARD2, padx=16, pady=8)
            sec_hdr.pack(fill="x", padx=16, pady=(8, 2))
            tk.Label(sec_hdr,
                     text=f"{'📄 ' if n_seqs > 1 else ''}Secuencia {seq_idx+1}  —  {lbl}",
                     bg=CARD2, fg=ACCENT,
                     font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(sec_hdr,
                     text=f"{aprobadas}/{total} aprobadas",
                     bg=CARD2, fg=c_sec,
                     font=("Segoe UI", 10, "bold")).pack(side="right")

            # Tarjetas de pruebas
            grid = tk.Frame(self._res_inner, bg=BG)
            grid.pack(fill="x", padx=16, pady=(2, 4))

            for i, (nombre, res) in enumerate(resultados.items()):
                col = i % 3
                row = i // 3
                grid.columnconfigure(col, weight=1)

                c_borde = GREEN if res["aprueba"] else RED
                estado  = "✅  APRUEBA" if res["aprueba"] else "❌  FALLA"

                card = tk.Frame(grid, bg=CARD, padx=14, pady=12,
                                highlightthickness=1,
                                highlightbackground=c_borde)
                card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

                tk.Label(card, text=nombre, bg=CARD, fg=SUBTEXT,
                         font=("Segoe UI", 9)).pack(anchor="w")
                tk.Label(card, text=estado, bg=CARD, fg=c_borde,
                         font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(2, 8))
                tk.Frame(card, bg=BORDER, height=1).pack(fill="x", pady=(0, 8))

                for linea in self._detalle(nombre, res):
                    tk.Label(card, text=linea, bg=CARD, fg=TEXT,
                             font=FONT_SMALL, anchor="w").pack(anchor="w")

            if seq_idx < n_seqs - 1:
                tk.Frame(self._res_inner, bg=BORDER, height=1).pack(
                    fill="x", padx=20, pady=(8, 0))

        self._res_scroll.refresh()

        # Pestaña Secuencia — muestra la primera secuencia
        self._seq_text.config(state="normal")
        self._seq_text.delete("1.0", "end")
        lbl0 = self._resultados_por_seq[0][0] if self._resultados_por_seq else ""
        self._seq_text.insert("end", f"{'#':>7}   {'Ri':>16}   {lbl0}\n")
        self._seq_text.insert("end", "─" * 60 + "\n")
        for i, v in enumerate(self._secuencia[:500], 1):
            self._seq_text.insert("end",
                f"{i:>7}   {v:>16.8f}   {self._nombre_gen}\n")
        if len(self._secuencia) > 500:
            self._seq_text.insert("end",
                f"\n  ... mostrando primeros 500 de {len(self._secuencia):,}\n")
        self._seq_text.config(state="disabled")

        # Gráficos — primera secuencia
        if MATPLOTLIB_OK:
            self._generar_graficos()

        self._status(
            f"✅ Listo · {total_aprobadas}/{total_pruebas} pruebas aprobadas "
            f"en {n_seqs} secuencia(s)", GREEN)

        # Actualizar pestaña Generador
        self._mostrar_generador()
        self._nb.select(0)

    # ──────────────────────────────────────────────────────
    def _mostrar_generador(self):
        """Pestaña Generador: stats basicas + histograma por secuencia."""
        for w in self._gen_inner.winfo_children():
            w.destroy()

        hdr = tk.Frame(self._gen_inner, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(16, 4))
        tk.Label(hdr, text=self._nombre_gen, bg=BG, fg=WHITE,
                 font=FONT_TITLE).pack(anchor="w")
        n_seqs = len(self._secuencias_gen)
        info = (f"{n_seqs} secuencia(s)  -  N = {len(self._secuencia):,} por secuencia"
                if n_seqs > 1 else
                f"N = {len(self._secuencia):,} numeros generados")
        tk.Label(hdr, text=info, bg=BG, fg=SUBTEXT, font=FONT_BODY).pack(anchor="w")
        tk.Frame(self._gen_inner, bg=BORDER, height=1).pack(
            fill="x", padx=20, pady=(12, 0))

        if not MATPLOTLIB_OK:
            tk.Label(self._gen_inner, text="matplotlib no disponible.",
                     bg=BG, fg=RED, font=FONT_BODY).pack(pady=20)
            self._gen_scroll.refresh()
            return

        plt.style.use("dark_background")

        for seq_idx, (lbl, seq) in enumerate(self._secuencias_gen):
            # Encabezado de secuencia
            sec_hdr = tk.Frame(self._gen_inner, bg=CARD2, padx=16, pady=8)
            sec_hdr.pack(fill="x", padx=16, pady=(12, 4))
            tk.Label(sec_hdr,
                     text=f"Secuencia {seq_idx+1}  -  {lbl}",
                     bg=CARD2, fg=ACCENT,
                     font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(sec_hdr,
                     text=f"N = {len(seq):,}",
                     bg=CARD2, fg=SUBTEXT,
                     font=("Segoe UI", 10)).pack(side="right")

            # Tarjetas de stats basicas
            stats_frame = tk.Frame(self._gen_inner, bg=BG)
            stats_frame.pack(fill="x", padx=16, pady=(4, 8))

            media  = sum(seq) / len(seq)
            var    = sum((x - media)**2 for x in seq) / (len(seq) - 1)
            mn, mx = min(seq), max(seq)
            rango  = mx - mn

            stats = [
                ("Media muestral", f"{media:.6f}",  ACCENT),
                ("Varianza",       f"{var:.6f}",    YELLOW),
                ("Minimo",         f"{mn:.6f}",     GREEN),
                ("Maximo",         f"{mx:.6f}",     GREEN),
                ("Rango",          f"{rango:.6f}",  SUBTEXT),
                ("Media teorica",  "0.500000",      SUBTEXT),
            ]
            for col_i, (label, valor, color) in enumerate(stats):
                stats_frame.columnconfigure(col_i, weight=1)
                card = tk.Frame(stats_frame, bg=CARD, padx=14, pady=10,
                                highlightthickness=1, highlightbackground=BORDER)
                card.grid(row=0, column=col_i, padx=5, sticky="nsew")
                tk.Label(card, text=label, bg=CARD, fg=SUBTEXT,
                         font=("Segoe UI", 9)).pack(anchor="w")
                tk.Label(card, text=valor, bg=CARD, fg=color,
                         font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(4, 0))

            # Histograma + dispersion side by side
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 3.8),
                                            facecolor="#0D1117")
            fig.subplots_adjust(wspace=0.35)

            for ax in (ax1, ax2):
                ax.set_facecolor("#161B22")
                for sp in ax.spines.values():
                    sp.set_color(BORDER)
                ax.tick_params(colors=SUBTEXT, labelsize=8)

            # Histograma
            ax1.hist(seq, bins=20, color=ACCENT, alpha=0.85,
                     edgecolor="#0D1117", linewidth=0.5)
            ax1.axvline(media, color=YELLOW, linestyle="--",
                        linewidth=1.5, label=f"Media = {media:.4f}")
            ax1.axvline(0.5,   color=GREEN,  linestyle=":",
                        linewidth=1.2, label="Media teorica (0.5)")
            ax1.set_xlabel("Valor Ri", fontsize=9, color=SUBTEXT)
            ax1.set_ylabel("Frecuencia", fontsize=9, color=SUBTEXT)
            ax1.set_title(f"Histograma  -  {lbl}", fontsize=9, color=TEXT, pad=8)
            ax1.legend(fontsize=7, loc="upper right")

            # Dispersion Ri vs Ri+1 (prueba visual de independencia)
            ax2.scatter(seq[:-1], seq[1:], s=2, color=ACCENT, alpha=0.4)
            ax2.set_xlabel("Ri", fontsize=9, color=SUBTEXT)
            ax2.set_ylabel("Ri+1", fontsize=9, color=SUBTEXT)
            ax2.set_title("Dispersion Ri vs Ri+1", fontsize=9, color=TEXT, pad=8)

            canvas = FigureCanvasTkAgg(fig, master=self._gen_inner)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="x", padx=16, pady=(0, 8))
            plt.close(fig)

            if seq_idx < n_seqs - 1:
                tk.Frame(self._gen_inner, bg=BORDER, height=1).pack(
                    fill="x", padx=20, pady=(4, 0))

        self._gen_scroll.refresh()

    def _detalle(self, nombre, res):
        if nombre == "Medias":
            return [f"Media muestral : {res['media_muestral']}",
                    f"LI             : {res['limite_inferior']}",
                    f"LS             : {res['limite_superior']}"]
        elif nombre == "Varianza":
            return [f"Var. muestral  : {res['varianza_muestral']}",
                    f"Var. teórica   : {res['varianza_teorica']}",
                    f"LI / LS        : {res['limite_inferior']} / {res['limite_superior']}"]
        elif nombre == "Chi-Cuadrado":
            return [f"χ² calculado   : {res['chi2_calculado']}",
                    f"χ² crítico     : {res['chi2_critico']}",
                    f"GL             : {res['grados_libertad']}"]
        elif nombre == "Kolmogorov-Smirnov":
            return [f"DMAX           : {res['dmax']}",
                    f"DMAXP          : {res['dmaxp']}"]
        elif nombre == "Póker":
            return [f"χ² calculado   : {res['chi2_calculado']}",
                    f"χ² crítico     : {res['chi2_critico']}"]
        elif nombre == "Rachas":
            return [f"Z calculado    : {res['z_calculado']}",
                    f"Z crítico      : ±{res['z_critico']}",
                    f"Rachas obs/esp : {res['rachas_observadas']} / {res['rachas_esperadas']}"]
        return []

    # ──────────────────────────────────────────────────────
    def _generar_graficos(self):
        for w in self._graf_inner.winfo_children():
            w.destroy()

        plt.style.use("dark_background")
        n    = len(self._resultados)
        cols = 3
        rows = math.ceil(n/cols)

        fig, axes = plt.subplots(rows, cols, figsize=(14, 4.8*rows),
                                 facecolor="#0D1117")
        fig.subplots_adjust(hspace=0.55, wspace=0.38)

        if rows == 1 and n == 1:
            axes = [[axes]]
        elif rows == 1:
            axes = [list(axes)]
        flat = [ax for row in axes for ax in row]

        for idx, (nombre, res) in enumerate(self._resultados.items()):
            ax = flat[idx]
            ax.set_facecolor("#161B22")
            self._plot(ax, nombre, res)

        for idx in range(n, len(flat)):
            flat[idx].set_visible(False)

        canvas = FigureCanvasTkAgg(fig, master=self._graf_inner)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        self._graf_inner.update_idletasks()
        self._graf_canvas.configure(scrollregion=self._graf_canvas.bbox("all"))

    def _plot(self, ax, nombre, res):
        c    = GREEN if res["aprueba"] else RED
        bar1 = ACCENT
        bar2 = YELLOW
        titulo = f"{nombre}  ·  {'APRUEBA ✓' if res['aprueba'] else 'FALLA ✗'}"

        if nombre == "Medias":
            ax.axhline(0.5, color=ACCENT, linestyle="--", lw=1.5, label="Media teórica")
            ax.axhspan(res["limite_inferior"], res["limite_superior"],
                       alpha=0.2, color=GREEN, label="IC 95%")
            ax.plot(0.5, res["media_muestral"], "o", color=c, ms=12,
                    label=f"Media: {res['media_muestral']}")
            ax.set_xlim(0,1); ax.set_xticks([]); ax.set_ylim(0,1)

        elif nombre == "Varianza":
            ax.axhline(res["varianza_teorica"], color=ACCENT,
                       linestyle="--", lw=1.5, label="Var. teórica")
            ax.axhspan(res["limite_inferior"], res["limite_superior"],
                       alpha=0.2, color=GREEN, label="IC 95%")
            ax.plot(0.5, res["varianza_muestral"], "o", color=c, ms=12,
                    label=f"Var: {res['varianza_muestral']}")
            ax.set_xlim(0,1); ax.set_xticks([])
            ax.set_ylim(0, res["limite_superior"]+0.02)

        elif nombre == "Chi-Cuadrado":
            k = res["k"]; x = range(k)
            etiq = [f"{i/k:.1f}" for i in range(k)]
            ax.bar([i-.2 for i in x], res["frecuencias_observadas"],
                   .4, label="Observada", color=bar1, alpha=0.85)
            ax.bar([i+.2 for i in x], [res["frecuencia_esperada"]]*k,
                   .4, label="Esperada", color=bar2, alpha=0.7)
            ax.set_xticks(list(x)); ax.set_xticklabels(etiq, fontsize=6)

        elif nombre == "Kolmogorov-Smirnov":
            tabla = res["tabla"]
            p_obs = [f["p_obs_acumulada"] for f in tabla]
            p_esp = [f["p_esp_acumulada"] for f in tabla]
            labs  = [f["intervalo"] for f in tabla]
            ax.plot(labs, p_obs, "o-", color=bar1, lw=2, label="FEC Observada")
            ax.plot(labs, p_esp, "s--", color=bar2, lw=2, label="FEC Esperada")
            difs = [f["diferencia"] for f in tabla]
            idx_max = difs.index(max(difs))
            ax.annotate(f"DMAX={res['dmax']}",
                        xy=(idx_max, p_obs[idx_max]),
                        xytext=(idx_max+1, p_obs[idx_max]-.15),
                        arrowprops=dict(arrowstyle="->", color=RED),
                        color=RED, fontsize=7)
            ax.set_xticks(range(len(labs)))
            ax.set_xticklabels(labs, rotation=45, fontsize=6)

        elif nombre == "Póker":
            cats = [f["categoria"].split(" - ")[0] for f in res["tabla"]]
            obs  = [f["frecuencia_observada"] for f in res["tabla"]]
            esp  = [f["frecuencia_esperada"] for f in res["tabla"]]
            x = range(len(cats))
            ax.bar([i-.2 for i in x], obs, .4, label="Observada", color=bar1, alpha=0.85)
            ax.bar([i+.2 for i in x], esp, .4, label="Esperada",  color=bar2, alpha=0.7)
            ax.set_xticks(list(x)); ax.set_xticklabels(cats, fontsize=8)

        elif nombre == "Rachas":
            vals = [res["rachas_observadas"], res["rachas_esperadas"]]
            bars = ax.bar(["Observadas", "Esperadas"], vals,
                          color=[bar1, bar2], width=0.4,
                          edgecolor="white", linewidth=0.5)
            margen = res["z_critico"] * math.sqrt(res["varianza_esperada"])
            ax.errorbar(1, res["rachas_esperadas"], yerr=margen,
                        fmt="none", color=RED, capsize=6, lw=2)
            for b, v in zip(bars, vals):
                ax.text(b.get_x()+b.get_width()/2,
                        b.get_height()+0.3,
                        str(round(v,1)), ha="center",
                        fontsize=9, color=WHITE)

        ax.set_title(titulo, fontsize=9, color=c, pad=8)
        ax.legend(fontsize=7, loc="upper right")
        for sp in ax.spines.values():
            sp.set_color(BORDER)
        ax.tick_params(colors=SUBTEXT, labelsize=7)

    # ──────────────────────────────────────────────────────
    def _exportar_csv(self):
        if not self._secuencia:
            messagebox.showwarning("Sin datos",
                "Ejecuta una simulación primero.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile=f"secuencia_{self._nombre_gen.replace(' ','_')}.csv")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["#", "Ri", "Generador"])
            for i, v in enumerate(self._secuencia, 1):
                w.writerow([i, round(v, 8), self._nombre_gen])
        messagebox.showinfo("Exportado", f"Archivo guardado en:\n{path}")
        self._status(f"✅ CSV exportado: {os.path.basename(path)}", GREEN)


if __name__ == "__main__":
    app = App()
    app.mainloop()