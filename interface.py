#!/usr/bin/env python3
"""
Interface simples para o AI Audio Fingerprint Remover.

O que faz:
  Remove fingerprints/marcas d'água de áudios gerados por IA (Suno, ElevenLabs,
  OpenAI, etc.). Limpa metadados, padrões espectrais, padrões estatísticos e
  adiciona imperfeições humanas para tornar o áudio indistinguível de gravações normais.

  Baseado em: https://github.com/geeknik/ai-audio-fingerprint-remover
"""

import os
import sys
import platform
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if platform.system() == "Windows":
    VENV_PYTHON = os.path.join(SCRIPT_DIR, "venv", "Scripts", "python.exe")
else:
    VENV_PYTHON = os.path.join(SCRIPT_DIR, "venv", "bin", "python")
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, "ai_audio_fingerprint_remover.py")
MONO_FONT = ("Consolas", 9) if platform.system() == "Windows" else ("Monospace", 9)

LEVELS = ["gentle", "moderate", "aggressive", "extreme"]
LEVEL_DESC = {
    "gentle":     "Mínimo — preserva qualidade, pode deixar alguns fingerprints",
    "moderate":   "Balanceado — bom equilíbrio qualidade/remoção (padrão)",
    "aggressive": "Agressivo — remove a maioria dos fingerprints, qualidade ok",
    "extreme":    "Máximo — remove tudo, pode adicionar artefatos sutis",
}

SUPPORTED = (".mp3", ".wav", ".flac", ".aiff", ".aif")


def pick_input(entry_var):
    path = filedialog.askopenfilename(
        title="Arquivo de entrada",
        filetypes=[("Áudio", "*.mp3 *.wav *.flac *.aiff *.aif"), ("Todos", "*.*")],
    )
    if path:
        entry_var.set(path)
        # auto-preenche saída se vazio
        if not out_var.get():
            base, ext = os.path.splitext(path)
            out_var.set(base + "_clean" + ext)


def pick_output(entry_var):
    path = filedialog.asksaveasfilename(
        title="Arquivo de saída",
        filetypes=[("Áudio", "*.mp3 *.wav *.flac *.aiff *.aif"), ("Todos", "*.*")],
    )
    if path:
        entry_var.set(path)


def pick_dir_in(entry_var):
    path = filedialog.askdirectory(title="Pasta de entrada")
    if path:
        entry_var.set(path)


def pick_dir_out(entry_var):
    path = filedialog.askdirectory(title="Pasta de saída")
    if path:
        entry_var.set(path)


def run_cmd(cmd, log_widget, done_callback):
    log_widget.config(state="normal")
    log_widget.delete("1.0", tk.END)

    def worker():
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            for line in proc.stdout:
                log_widget.after(0, lambda l=line: (
                    log_widget.insert(tk.END, l),
                    log_widget.see(tk.END),
                ))
            proc.wait()
            rc = proc.returncode
        except Exception as e:
            rc = -1
            log_widget.after(0, lambda: log_widget.insert(tk.END, f"\nErro: {e}\n"))

        log_widget.after(0, lambda: done_callback(rc))

    threading.Thread(target=worker, daemon=True).start()


def process_file(btn, log, level_var, in_var, out_var):
    inp = in_var.get().strip()
    out = out_var.get().strip()
    level = level_var.get()

    if not inp:
        messagebox.showerror("Erro", "Selecione o arquivo de entrada.")
        return
    if not os.path.isfile(inp):
        messagebox.showerror("Erro", f"Arquivo não encontrado:\n{inp}")
        return

    cmd = [VENV_PYTHON, MAIN_SCRIPT, inp]
    if out:
        cmd.append(out)
    cmd += ["--level", level]

    btn.config(state="disabled", text="Processando…")

    def done(rc):
        btn.config(state="normal", text="Processar arquivo")
        if rc == 0:
            messagebox.showinfo("Pronto", "Arquivo processado com sucesso!")
        else:
            messagebox.showerror("Erro", f"Processo terminou com código {rc}.\nVeja o log abaixo.")

    run_cmd(cmd, log, done)


def process_dir(btn, log, level_var, din_var, dout_var):
    din = din_var.get().strip()
    dout = dout_var.get().strip()
    level = level_var.get()

    if not din:
        messagebox.showerror("Erro", "Selecione a pasta de entrada.")
        return
    if not os.path.isdir(din):
        messagebox.showerror("Erro", f"Pasta não encontrada:\n{din}")
        return

    cmd = [VENV_PYTHON, MAIN_SCRIPT, "--directory", din]
    if dout:
        cmd.append(dout)
    cmd += ["--level", level]

    btn.config(state="disabled", text="Processando…")

    def done(rc):
        btn.config(state="normal", text="Processar pasta")
        if rc == 0:
            messagebox.showinfo("Pronto", "Pasta processada com sucesso!")
        else:
            messagebox.showerror("Erro", f"Processo terminou com código {rc}.\nVeja o log abaixo.")

    run_cmd(cmd, log, done)


# ── GUI ──────────────────────────────────────────────────────────────────────

root = tk.Tk()
root.title("AI Audio Fingerprint Remover")
root.resizable(True, True)

# variáveis globais (usadas nos callbacks acima)
in_var  = tk.StringVar()
out_var = tk.StringVar()
din_var  = tk.StringVar()
dout_var = tk.StringVar()

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=8, pady=8)

# ── Aba 1: arquivo único ──────────────────────────────────────────────────

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="  Arquivo único  ")

ttk.Label(tab1, text="Entrada:").grid(row=0, column=0, sticky="w", padx=6, pady=(10,2))
ttk.Entry(tab1, textvariable=in_var, width=55).grid(row=0, column=1, padx=4, pady=(10,2))
ttk.Button(tab1, text="…", width=3, command=lambda: pick_input(in_var)).grid(row=0, column=2, pady=(10,2))

ttk.Label(tab1, text="Saída:").grid(row=1, column=0, sticky="w", padx=6, pady=2)
ttk.Entry(tab1, textvariable=out_var, width=55).grid(row=1, column=1, padx=4, pady=2)
ttk.Button(tab1, text="…", width=3, command=lambda: pick_output(out_var)).grid(row=1, column=2, pady=2)

ttk.Label(tab1, text="Nível:").grid(row=2, column=0, sticky="w", padx=6, pady=2)
level_var1 = tk.StringVar(value="aggressive")
lvl_combo1 = ttk.Combobox(tab1, textvariable=level_var1, values=LEVELS, state="readonly", width=14)
lvl_combo1.grid(row=2, column=1, sticky="w", padx=4, pady=2)

level_desc1 = ttk.Label(tab1, text=LEVEL_DESC["aggressive"], foreground="#555", wraplength=420)
level_desc1.grid(row=3, column=0, columnspan=3, sticky="w", padx=6, pady=(0,6))

def on_level1(e=None):
    level_desc1.config(text=LEVEL_DESC.get(level_var1.get(), ""))
lvl_combo1.bind("<<ComboboxSelected>>", on_level1)

log1 = tk.Text(tab1, height=14, font=MONO_FONT, wrap="word", state="disabled", bg="#1e1e1e", fg="#d4d4d4")
log1.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=6, pady=(4,6))
tab1.grid_rowconfigure(5, weight=1)
tab1.grid_columnconfigure(1, weight=1)

btn1 = ttk.Button(tab1, text="Processar arquivo",
                  command=lambda: process_file(btn1, log1, level_var1, in_var, out_var))
btn1.grid(row=4, column=0, columnspan=3, pady=6)

# ── Aba 2: pasta inteira ──────────────────────────────────────────────────

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="  Pasta inteira  ")

ttk.Label(tab2, text="Pasta entrada:").grid(row=0, column=0, sticky="w", padx=6, pady=(10,2))
ttk.Entry(tab2, textvariable=din_var, width=55).grid(row=0, column=1, padx=4, pady=(10,2))
ttk.Button(tab2, text="…", width=3, command=lambda: pick_dir_in(din_var)).grid(row=0, column=2, pady=(10,2))

ttk.Label(tab2, text="Pasta saída:").grid(row=1, column=0, sticky="w", padx=6, pady=2)
ttk.Entry(tab2, textvariable=dout_var, width=55).grid(row=1, column=1, padx=4, pady=2)
ttk.Button(tab2, text="…", width=3, command=lambda: pick_dir_out(dout_var)).grid(row=1, column=2, pady=2)

ttk.Label(tab2, text="Nível:").grid(row=2, column=0, sticky="w", padx=6, pady=2)
level_var2 = tk.StringVar(value="aggressive")
lvl_combo2 = ttk.Combobox(tab2, textvariable=level_var2, values=LEVELS, state="readonly", width=14)
lvl_combo2.grid(row=2, column=1, sticky="w", padx=4, pady=2)

level_desc2 = ttk.Label(tab2, text=LEVEL_DESC["aggressive"], foreground="#555", wraplength=420)
level_desc2.grid(row=3, column=0, columnspan=3, sticky="w", padx=6, pady=(0,6))

def on_level2(e=None):
    level_desc2.config(text=LEVEL_DESC.get(level_var2.get(), ""))
lvl_combo2.bind("<<ComboboxSelected>>", on_level2)

log2 = tk.Text(tab2, height=14, font=MONO_FONT, wrap="word", state="disabled", bg="#1e1e1e", fg="#d4d4d4")
log2.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=6, pady=(4,6))
tab2.grid_rowconfigure(5, weight=1)
tab2.grid_columnconfigure(1, weight=1)

btn2 = ttk.Button(tab2, text="Processar pasta",
                  command=lambda: process_dir(btn2, log2, level_var2, din_var, dout_var))
btn2.grid(row=4, column=0, columnspan=3, pady=6)

# ── Aba 3: sobre ──────────────────────────────────────────────────────────

tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="  Sobre  ")

sobre = tk.Text(tab3, wrap="word", font=("Sans", 10), padx=12, pady=12,
                relief="flat", bg=root.cget("bg"))
sobre.insert("1.0", __doc__.strip())
sobre.config(state="disabled")
sobre.pack(fill="both", expand=True)

root.mainloop()
