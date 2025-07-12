import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Constantes y datos
elementos = ["H\u2082", "O\u2082", "Cl\u2082", "Br\u2082", "N\u2082", "C", "H\u2082O", "CO", "NH\u2083"]
R = 8.314

valores_abc = {
    "H₂": {"a": 29.066, "b": -8.36e-4, "c": 2.0117e-6},
    "O₂": {"a": 25.503, "b": 0.13612, "c": -4.2555e-6},
    "Cl₂": {"a": 31.696, "b": 0.010144, "c": -4.0376e-6},
    "Br₂": {"a": 35.24, "b": 4.075e-3, "c": -1.4874e-6},
    "N₂": {"a": 26.984, "b": 5.91e-3, "c": -3.376e-7},
    "C": {"a": -5.293, "b": 0.058609, "c": -4.3225e-5},
    "H₂O": {"a": 30.206, "b": 9.933e-3, "c": 1.1171e-6},
    "CO": {"a": 26.537, "b": 7.683e-3, "c": -1.1719e-6},
    "NH₃": {"a": 25.894, "b": 0.032999, "c": -3.0459e-6}
}

procesos = {
    "Proceso Isotérmico": [
        "Número de moles (mol)", "Temperatura (K)", "Volumen 1 (L)", "Volumen 2 (L)", "Presión 1 (atm)", "Presión 2 (atm)"
    ],
    "Proceso Isocórico": [
        "Número de moles (mol)", "Volumen (L)", "Temperatura 1 (K)", "Temperatura 2 (K)", "Presión 1 (atm)", "Presión 2 (atm)"
    ],
    "Proceso Isobárico": [
        "Número de moles (mol)", "Presión (atm)", "Temperatura 1 (K)", "Temperatura 2 (K)", "Volumen 1 (L)", "Volumen 2 (L)"
    ]
}
root = tk.Tk()
root.title("Proceso Termodinámico")

var_proceso = tk.StringVar()
var_elemento = tk.StringVar()
entries = []

label_info_extra = tk.Label(root, text="", justify="left", font=("Arial", 10, "italic"))
label_info_extra.pack()

frame_campos = tk.Frame(root)
frame_campos.pack(pady=10)

frame_resultado = tk.Frame(root)
frame_resultado.pack(pady=10)

frame_grafica = tk.Frame(root)
frame_grafica.pack(pady=10)
def mostrar_campos(event):
    for widget in frame_campos.winfo_children():
        widget.destroy()
    for widget in frame_resultado.winfo_children():
        widget.destroy()
    for widget in frame_grafica.winfo_children():
        widget.destroy()
    entries.clear()
    campos = procesos.get(var_proceso.get(), [])
    for campo in campos:
        tk.Label(frame_campos, text=campo).pack()
        ent = tk.Entry(frame_campos)
        ent.pack()
        entries.append((campo, ent))
    actualizar_info_extra()

def actualizar_info_extra(*args):
    elemento = var_elemento.get()
    info = f"Constante R = {R} J/mol·K\n"
    if elemento in valores_abc:
        abc = valores_abc[elemento]
        info += f"a = {abc['a']}\n"
        info += f"b = {abc['b']:.6e}\n"
        info += f"c = {abc['c']:.6e}"
    else:
        info += "a, b, c: No disponibles"
    label_info_extra.config(text=info)
def mostrar_tabla(wvr, wvi, wp, qr, qi, du, dh, n):
    for widget in frame_resultado.winfo_children():
        widget.destroy()

    contenedor = tk.Frame(frame_resultado)
    contenedor.pack()

    ancho = 220
    alto = 200

    div1 = tk.Frame(contenedor, bd=1, relief="solid", width=ancho, height=alto)
    div1.grid(row=0, column=0, padx=5)
    div1.pack_propagate(False)
    tk.Label(div1, text=f"Trabajo Reversible (wᵣ) = {wvr:.4f} J").pack()
    tk.Label(div1, text=f"Trabajo Irreversible (wᵢ) = {wvi:.4f} J").pack()
    tk.Label(div1, text=f"Trabajo Presión (wₚ) = {wp:.4f} J").pack()

    div2 = tk.Frame(contenedor, bd=1, relief="solid", width=ancho, height=alto)
    div2.grid(row=0, column=1, padx=5)
    div2.pack_propagate(False)
    tk.Label(div2, text=f"Calor Reversible (qᵣ) = {qr:.4f} J").pack()
    tk.Label(div2, text=f"Calor Irreversible (qᵢ) = {qi:.4f} J").pack()

    div3 = tk.Frame(contenedor, bd=1, relief="solid", width=ancho, height=alto)
    div3.grid(row=0, column=2, padx=5)
    div3.pack_propagate(False)
    tk.Label(div3, text=f"ΔU = {du:.4f} J").pack()
    tk.Label(div3, text=f"ΔH = {dh:.4f} J").pack()
    tk.Label(div3, text=f"n = {n} mol").pack()
def graficar_comparacion_isotermico(T, V1, V2, P2, n):
    V_reversible = np.linspace(0.1, 10, 100)
    P_reversible = (n * R * T) / V_reversible

    V_irreversible = np.linspace(min(V1, V2), max(V1, V2), 100)
    P_irreversible = np.full_like(V_irreversible, P2)

    for widget in frame_grafica.winfo_children():
        widget.destroy()

    contenedor = tk.Frame(frame_grafica)
    contenedor.pack()

    fig1, ax1 = plt.subplots(figsize=(4, 3), dpi=100)
    ax1.plot(V_reversible, P_reversible, color="blue")
    ax1.set_title("Isotérmico Reversible")
    ax1.set_xlabel("Volumen (L)")
    ax1.set_ylabel("Presión (atm)")
    ax1.grid(True)

    canvas1 = FigureCanvasTkAgg(fig1, master=contenedor)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT, padx=10)

    fig2, ax2 = plt.subplots(figsize=(4, 3), dpi=100)
    ax2.plot(V_irreversible, P_irreversible, color="red", linestyle="--")
    ax2.set_title("Isotérmico Irreversible")
    ax2.set_xlabel("Volumen (L)")
    ax2.set_ylabel("Presión (atm)")
    ax2.grid(True)

    canvas2 = FigureCanvasTkAgg(fig2, master=contenedor)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.RIGHT, padx=10)

def graficar_pv_isocorico(V, T1, T2):
    T_vals = np.linspace(T1, T2, 100)
    P_vals = (R * T_vals) / V

    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.plot([V]*len(P_vals), P_vals, color="green")
    ax.set_xlabel("Volumen (L)")
    ax.set_ylabel("Presión (atm)")
    ax.grid(True)

    for widget in frame_grafica.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack()

def graficar_comparacion_isobarico(qp, wv):
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    labels = ['Trabajo (w)', 'Calor (q)']
    valores = [wv, qp]
    colores = ['orange', 'green']

    ax.bar(labels, valores, color=colores)
    ax.set_title("Trabajo y Calor (Isobárico)")
    ax.grid(axis='y')

    for widget in frame_grafica.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack()
def enviar_datos():
    datos = {campo: ent.get() for campo, ent in entries}
    elemento = var_elemento.get()

    try:
        n = float(datos["Número de moles (mol)"])

        if var_proceso.get() == "Proceso Isotérmico":
            T = float(datos["Temperatura (K)"])
            V1 = float(datos["Volumen 1 (L)"])
            V2 = float(datos["Volumen 2 (L)"])
            P1 = float(datos["Presión 1 (atm)"])
            P2 = float(datos["Presión 2 (atm)"])
    
            wvr = -n * R * T * math.log(V2 / V1)
            qr = -wvr
            wvi = -P2 * (V2 - V1)
            qi = -wvi
            wp = n * R * T * math.log(P2 / P1)
            du = dh = 0

            mostrar_tabla(wvr, wvi, wp, qr, qi, du, dh, n)
            graficar_comparacion_isotermico(T, V1, V2, P2, n)

        elif var_proceso.get() == "Proceso Isocórico":
            V = float(datos["Volumen (L)"])
            T1 = float(datos["Temperatura 1 (K)"])
            T2 = float(datos["Temperatura 2 (K)"])
            P1 = float(datos["Presión 1 (atm)"])
            P2 = float(datos["Presión 2 (atm)"])

            wv = 0
            wp = n * R * (T2 - T1)

            if elemento in valores_abc:
                abc = valores_abc[elemento]
                pol = np.polynomial.Polynomial([abc["a"] - R, abc["b"], abc["c"]])
                qv = pol.integ()(T2) - pol.integ()(T1)
                du = qv
                dh = du + n * R * (T2 - T1)

                mostrar_tabla(wv, 0, wp, qv, 0, du, dh, n)
                graficar_pv_isocorico(V, T1, T2)
            else:
                messagebox.showerror("Error", "Faltan datos térmicos del gas")

        elif var_proceso.get() == "Proceso Isobárico":
            P = float(datos["Presión (atm)"])
            T1 = float(datos["Temperatura 1 (K)"])
            T2 = float(datos["Temperatura 2 (K)"])
            V1 = float(datos["Volumen 1 (L)"])
            V2 = float(datos["Volumen 2 (L)"])

            wv = P * (V2 - V1)

            if elemento in valores_abc:
                abc = valores_abc[elemento]
                pol = np.polynomial.Polynomial([abc["a"] - R, abc["b"], abc["c"]])
                qp = pol.integ()(T2) - pol.integ()(T1)
                du = qp - wv
                dh = qp + n * R * (T2 - T1)

                mostrar_tabla(wv, 0, wv, qp, 0, du, dh, n)
                graficar_comparacion_isobarico(qp, wv)
            else:
                messagebox.showerror("Error", "Faltan datos térmicos del gas")

    except Exception as e:
        messagebox.showerror("Error", f"Datos inválidos: {e}")
var_proceso.set("Proceso Isotérmico")
var_elemento.set("H₂")

tk.Label(root, text="Selecciona proceso:").pack()
combo_proceso = ttk.Combobox(root, textvariable=var_proceso, values=list(procesos.keys()))
combo_proceso.pack()
combo_proceso.bind("<<ComboboxSelected>>", mostrar_campos)

tk.Label(root, text="Selecciona elemento:").pack()
combo_elemento = ttk.Combobox(root, textvariable=var_elemento, values=elementos)
combo_elemento.pack()
combo_elemento.bind("<<ComboboxSelected>>", actualizar_info_extra)

mostrar_campos(None)

tk.Button(root, text="Calcular", command=enviar_datos).pack(pady=10)

root.mainloop()
