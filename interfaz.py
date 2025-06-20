import tkinter as tk
from tkinter import filedialog, messagebox, font
import platform
import subprocess

class WelcomeWindow:
    def __init__(self, root, on_start):
        self.root = root
        self.on_start = on_start
        root.title("easyAssembly - Bienvenida")
        root.geometry("440x380")
        azul_oscuro = "#1a2942"
        fuente_titulo = font.Font(family="Arial", size=22, weight="bold", slant="italic")
        fuente_normal = font.Font(family="Arial", size=11)
        fuente_autor = font.Font(family="Arial", size=10, slant="italic")
        tk.Label(root, text="easyAssembly", font=fuente_titulo, fg=azul_oscuro).pack(pady=10)
        tk.Label(
            root,
            text="Programa que traduce de C a Assembly.\n\n"
                 "Convierte código fuente en lenguaje C o Java\na código ensamblador para distintas arquitecturas.",
            font=fuente_normal, fg=azul_oscuro, justify="center"
        ).pack(pady=10)
        tk.Label(root, text="Creador: garcialaso05", font=fuente_autor, fg="#2a4a7b").pack(pady=(0, 10))
        so = platform.system()
        self.so = so
        tk.Label(root, text=f"Sistema operativo detectado: {so}", fg="#234", font=fuente_normal).pack(pady=10)
        tk.Button(
            root, text="Empezar", font=("Arial", 13, "bold"), bg="#2a4a7b", fg="white",
            activebackground="#19325a", activeforeground="white", command=self.start
        ).pack(pady=30)
    def start(self):
        self.root.destroy()
        self.on_start(self.so)

class SelectWindow:
    def __init__(self, so):
        self.so = so
        self.root = tk.Tk()
        self.root.title("easyAssembly - Selección de Lenguaje y Arquitectura")
        self.root.geometry("420x320")
        azul_oscuro = "#1a2942"
        fuente_titulo = font.Font(family="Arial", size=15, weight="bold")
        fuente_normal = font.Font(family="Arial", size=11)
        tk.Label(self.root, text="Selecciona el lenguaje:", font=fuente_titulo, fg=azul_oscuro).pack(pady=10)
        self.lang_var = tk.StringVar(value="C")
        frame_lang = tk.Frame(self.root)
        frame_lang.pack()
        self.btn_c = tk.Button(frame_lang, text="C", width=10, relief="sunken", font=fuente_normal, fg=azul_oscuro,
                               command=lambda: self.select_lang("C"))
        self.btn_c.pack(side="left", padx=10)
        self.btn_java = tk.Button(frame_lang, text="Java", width=10, font=fuente_normal, fg=azul_oscuro,
                                  command=lambda: self.select_lang("Java"))
        self.btn_java.pack(side="left", padx=10)
        tk.Label(self.root, text="Selecciona la arquitectura:", font=fuente_titulo, fg=azul_oscuro).pack(pady=10)
        self.arch_var = tk.StringVar(value="ARMv7")
        archs = ["ARMv7", "ARMv8", "x86‑64", "RISC-V", "MIPS"]
        tk.OptionMenu(self.root, self.arch_var, *archs).pack()
        tk.Button(
            self.root, text="Comenzar", font=("Arial", 12, "bold"), bg="#2a4a7b", fg="white",
            activebackground="#19325a", activeforeground="white", command=self.start
        ).pack(pady=30)
        self.root.mainloop()
    def select_lang(self, lang):
        self.lang_var.set(lang)
        if lang == "C":
            self.btn_c.config(relief="sunken")
            self.btn_java.config(relief="raised")
        else:
            self.btn_c.config(relief="raised")
            self.btn_java.config(relief="sunken")
    def start(self):
        lang = self.lang_var.get()
        arch = self.arch_var.get()
        if lang == "C" and arch == "ARMv7":
            CArm7Window(self.so)
        elif lang == "C" and arch in ["x86‑64", "x86-64", "x86_64", "x86_64"]:
            CX86Window(self.so)
        elif lang == "C" and arch == "MIPS":
            CMIPSWindow(self.so)
        else:
            messagebox.showinfo("En proceso", "Esta función aún está en proceso.")

class CArm7Window:
    def __init__(self, so):
        self.so = so
        self.win = tk.Toplevel()
        self.win.title("easyAssembly - C a Assembly (ARM7)")
        self.win.geometry("600x500")
        azul_oscuro = "#1a2942"
        fuente_titulo = font.Font(family="Arial", size=16, weight="bold")
        fuente_normal = font.Font(family="Arial", size=11)
        tk.Label(self.win, text="C a Assembly (ARM7)", font=fuente_titulo, fg=azul_oscuro).pack(pady=(10, 5))
        self.show_dependencies_window(so)
        # Recuadro comentario desplegable
        self.comment_frame = tk.Frame(self.win, bg="#e6f0fa", bd=2, relief="groove")
        self.comment_frame.pack(padx=10, pady=(5, 10), fill="x")
        self.comment_expanded = False
        self.comment_label = tk.Label(
            self.comment_frame,
            text="💡 Comentarios útiles (haz clic para desplegar)",
            font=("Arial", 10, "bold"), fg="#234", bg="#e6f0fa", cursor="hand2", anchor="w", justify="left"
        )
        self.comment_label.pack(fill="x", padx=5, pady=3)
        self.comment_label.bind("<Button-1>", self.toggle_comment)
        self.comment_content = tk.Label(
            self.comment_frame,
            text=(
                "1) Si hay más de un archivo fuente, compílalos por separado y luego enlázalos. "
                "Revisa los includes y los .h.\n"
                "2) Puede haber líneas innecesarias o redundantes según el contexto.\n"
                "3) Los comentarios explican cada instrucción según el programa principal.\n"
                "4) Los push/pop pueden optimizarse para preservar solo los registros necesarios.\n"
                "5) Las etiquetas son por defecto LX, si las sustituyes usa 'replace all'.\n"
                "6) En algunos casos, especialmente en bucles y condicionales la optimización 0 puede hacer muchos accesos a memoria\n\n"
                "\t @; while (i < limite) {}     //Opt0\n\tldr     r2, [fp, #-8]   @; i\n\tldr     r3, [fp, #-20]  @; limite\n\tcmp     r2, r3 \n\tblt     .L5\n\n"
                "\t @; while (i < limite) {}     //Opt1\n\tcmp	r3, #10	@; i\n\tbne	.L5\n\n"
                "7) Ten cuidado con utilizar includes a funciones raiz de C como <stdio.h> o <math.h>.\nNo recomiendo su uso en ARM7, si lo necesitas puedes añadir el path a la librería."
            ),
            font=("Arial", 10), fg="#1a2942", bg="#e6f0fa", wraplength=570, justify="left"
        )
        # Inicialmente oculto
        self.comment_content.pack_forget()
        frame = tk.Frame(self.win)
        frame.pack(pady=5, padx=10, fill="x")
        # Nivel de optimización + info
        tk.Label(frame, text="Nivel de optimización:", font=fuente_normal, fg=azul_oscuro).grid(row=0, column=0, sticky="w")
        self.opt_var = tk.IntVar(value=0)
        self.opt_slider = tk.Scale(frame, from_=0, to=3, orient="horizontal", variable=self.opt_var)
        self.opt_slider.grid(row=0, column=1, padx=10)
        tk.Button(frame, text="info", font=("Arial", 8, "bold"), fg="#2a4a7b", command=self.show_opt_info, width=4).grid(row=0, column=2, padx=2)
        # Comentarios
        tk.Label(frame, text="Comentarios detallados:", font=fuente_normal, fg=azul_oscuro).grid(row=1, column=0, sticky="w")
        self.comments_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, variable=self.comments_var).grid(row=1, column=1, sticky="w")
        # Folding + info
        tk.Label(frame, text="Evitar folding:", font=fuente_normal, fg=azul_oscuro).grid(row=2, column=0, sticky="w")
        self.folding_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, variable=self.folding_var).grid(row=2, column=1, sticky="w")
        tk.Button(frame, text="info", font=("Arial", 8, "bold"), fg="#2a4a7b", command=self.show_folding_info, width=4).grid(row=2, column=2, padx=2)
        # Checkbox para simplificar ensamblador
        tk.Label(frame, text="Simplificar ensamblador:", font=fuente_normal, fg=azul_oscuro).grid(row=3, column=0, sticky="w")
        self.simplify_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, variable=self.simplify_var).grid(row=3, column=1, sticky="w")
        # Archivo entrada/salida
        tk.Label(frame, text="Archivo de entrada:", font=fuente_normal, fg=azul_oscuro).grid(row=4, column=0, sticky="w")
        self.input_entry = tk.Entry(frame, width=30)
        self.input_entry.grid(row=4, column=1)
        tk.Button(frame, text="Seleccionar", font=fuente_normal, command=self.browse_file).grid(row=4, column=2, padx=5)
        tk.Label(frame, text="Archivo de salida:", font=fuente_normal, fg=azul_oscuro).grid(row=5, column=0, sticky="w")
        self.output_entry = tk.Entry(frame, width=30)
        self.output_entry.insert(0, "salida.s")
        self.output_entry.grid(row=5, column=1, columnspan=2, sticky="w")
        # Campo para rutas de include
        tk.Label(frame, text="Rutas de include (-I):", font=fuente_normal, fg=azul_oscuro).grid(row=6, column=0, sticky="w")
        self.include_entry = tk.Entry(frame, width=30)
        self.include_entry.grid(row=6, column=1, columnspan=2, sticky="w")
        tk.Button(
            self.win, text="Compilar", font=("Arial", 12, "bold"), bg="#2a4a7b", fg="white",
            activebackground="#19325a", activeforeground="white", command=self.compile
        ).pack(pady=20)
        # Ayuda sobre includes
        tk.Button(self.win, text="¿Problemas con includes?", font=("Arial", 9, "bold"), fg="#2a4a7b", command=self.show_include_help).pack(pady=(0, 10))

    def toggle_comment(self, event=None):
        if self.comment_expanded:
            self.comment_content.pack_forget()
            self.comment_label.config(text="💡 Comentarios útiles (haz clic para desplegar)")
            self.comment_expanded = False
        else:
            self.comment_content.pack(fill="x", padx=5, pady=3)
            self.comment_label.config(text="💡 Comentarios útiles (haz clic para contraer)")
            self.comment_expanded = True

    def show_dependencies_window(self, so):
        dep_win = tk.Toplevel(self.win)
        dep_win.title("Dependencias necesarias")
        dep_win.geometry("500x340")
        dep_win.resizable(False, False)
        azul_oscuro = "#1a2942"
        fuente_titulo = font.Font(family="Arial", size=13, weight="bold")
        fuente_normal = font.Font(family="Arial", size=10)
        dep_msg = self.get_dependencies_message(so)
        tk.Label(dep_win, text="Dependencias necesarias para C-ARM7", font=fuente_titulo, fg=azul_oscuro).pack(pady=(10, 5))
        msg_label = tk.Label(dep_win, text=dep_msg, justify="left", anchor="w", font=fuente_normal, fg=azul_oscuro, wraplength=470)
        msg_label.pack(padx=10, pady=(0, 10))
        if so.startswith("Linux"):
            btns = [
                ("Ubuntu/Debian", "sudo apt update && sudo apt install gcc-arm-none-eabi"),
                ("Arch Linux", "sudo pacman -S arm-none-eabi-gcc"),
                ("Fedora", "sudo dnf install arm-none-eabi-gcc-cs"),
                ("openSUSE", "sudo zypper install cross-arm-none-eabi-gcc"),
            ]
            btn_frame = tk.Frame(dep_win)
            btn_frame.pack(pady=(0, 10))
            for name, cmd in btns:
                def copy_cmd(c=cmd):
                    dep_win.clipboard_clear()
                    dep_win.clipboard_append(c)
                    tk.messagebox.showinfo("Copiado", "Comando copiado al portapapeles.", parent=dep_win)
                tk.Button(btn_frame, text=f"Copiar {name}", font=("Arial", 9, "bold"), fg="#2a4a7b", command=copy_cmd, width=30).pack(pady=2)
        elif so.startswith("Windows"):
            import webbrowser
            def open_url(event=None):
                webbrowser.open("https://developer.arm.com/downloads/-/gnu-rm")
            link = tk.Label(dep_win, text="Enlace oficial de descarga", fg="#1a2942", cursor="hand2", font=("Arial", 10, "underline"))
            link.pack(pady=(0, 10))
            link.bind("<Button-1>", open_url)
        elif so == "macOS":
            def copy_cmd():
                dep_win.clipboard_clear()
                dep_win.clipboard_append("brew tap ArmMbed/homebrew-formulae && brew install arm-none-eabi-gcc")
                tk.messagebox.showinfo("Copiado", "Comando copiado al portapapeles.", parent=dep_win)
            tk.Button(dep_win, text="Copiar comando Homebrew", font=("Arial", 9, "bold"), fg="#2a4a7b", command=copy_cmd, width=30).pack(pady=2)
        tk.Button(dep_win, text="OK", font=("Arial", 11, "bold"), bg="#2a4a7b", fg="white", command=dep_win.destroy).pack(pady=10)

    def get_dependencies_message(self, so):
        if so.startswith("Windows"):
            return (
                "Debes instalar el compilador ARM GCC (arm-none-eabi-gcc).\n"
                "1. Descarga el instalador desde el enlace inferior.\n"
                "2. Instala y añade a la variable PATH."
            )
        elif so.startswith("Linux"):
            return (
                "Debes instalar el compilador ARM GCC (arm-none-eabi-gcc).\n"
                "Comandos para las principales distribuciones (elige el tuyo y cópialo):"
            )
        elif so == "macOS":
            return (
                "Instala Homebrew si no lo tienes y luego ejecuta el siguiente comando en terminal:"
            )
        else:
            return "No se ha podido determinar las dependencias para tu sistema."

    def show_opt_info(self):
        win = tk.Toplevel(self.win)
        win.title("Información de optimización")
        win.geometry("420x260")
        azul_oscuro = "#1a2942"
        msg = (
            "Nivel de optimización:\n"
            "0: Sin optimización (recomendado -> código más cercano al C original).\n"
            "1: Optimización básica.\n"
            "2: Optimización estándar.\n"
            "3: Máxima optimización.\n"
        )
        tk.Label(win, text=msg, justify="left", anchor="w", font=("Arial", 10), fg=azul_oscuro, wraplength=400).pack(padx=10, pady=15)
        tk.Button(win, text="OK", font=("Arial", 11, "bold"), bg="#2a4a7b", fg="white", command=win.destroy).pack(pady=10)

    def show_folding_info(self):
        win = tk.Toplevel(self.win)
        win.title("Información sobre folding")
        win.geometry("440x260")
        azul_oscuro = "#1a2942"
        msg = (
            "Evitar folding:\n"
            "Los compiladores suelen precalcular todas las expresiones posibles con constantes (constant folding), "
            "lo que puede hacer que el código ensamblador resultante sea muy diferente al código C original.\n\n"
            "Si activas esta opción, el programa transformará automáticamente las constantes en variables locales dentro de main, "
            "evitando así el folding y generando un ensamblador más similar al C.\nPara esto se generará un archivo intermedio x_nofold.c\n\n"
            "Existen otras opciones como declarar las constantes como 'volatile' o 'extern', pero eso puede complicar el código."
        )
        tk.Label(win, text=msg, justify="left", anchor="w", font=("Arial", 10), fg=azul_oscuro, wraplength=420).pack(padx=10, pady=15)
        tk.Button(win, text="OK", font=("Arial", 11, "bold"), bg="#2a4a7b", fg="white", command=win.destroy).pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C files", "*.c")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
    def compile(self):
        src = self.input_entry.get()
        out = self.output_entry.get()
        opt = str(self.opt_var.get())
        cmts = "on" if self.comments_var.get() else "off"
        folding = "off" if self.folding_var.get() else "on"
        simplify = "on" if self.simplify_var.get() else "off"
        includes = self.include_entry.get().strip()
        if not src:
            messagebox.showerror("Error", "Debes seleccionar un archivo de entrada.")
            return
        cmd = ["python3", "asmarm7.py", src, opt, out, cmts, folding, simplify]
        if includes:
            cmd.append("--includes=" + includes)
        try:
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Éxito", f"Archivo ensamblador generado: {out}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Ocurrió un error durante la compilación.")

class CX86Window:
    def __init__(self, so):
        self.so = so
        self.win = tk.Toplevel()
        self.win.title("easyAssembly - C a Assembly (x86-64)")
        self.win.geometry("600x500")
        azul_oscuro = "#1a2942"
        fuente_titulo = font.Font(family="Arial", size=16, weight="bold")
        fuente_normal = font.Font(family="Arial", size=11)
        tk.Label(self.win, text="C a Assembly (x86-64)", font=fuente_titulo, fg=azul_oscuro).pack(pady=(10, 5))
        self.show_dependencies_window(so)
        # Recuadro comentario desplegable
        self.comment_frame = tk.Frame(self.win, bg="#e6f0fa", bd=2, relief="groove")
        self.comment_frame.pack(padx=10, pady=(5, 10), fill="x")
        self.comment_expanded = False
        self.comment_label = tk.Label(
            self.comment_frame,
            text="💡 Comentarios útiles (haz clic para desplegar)",
            font=("Arial", 10, "bold"), fg="#234", bg="#e6f0fa", cursor="hand2", anchor="w", justify="left"
        )
        self.comment_label.pack(fill="x", padx=5, pady=3)
        self.comment_label.bind("<Button-1>", self.toggle_comment)
        self.comment_content = tk.Label(
            self.comment_frame,
            text=(
                "1) Si hay más de un archivo fuente, compílalos por separado y luego enlázalos. "
                "Revisa los includes y los .h.\n"
                "2) Puede haber líneas innecesarias o redundantes según el contexto.\n"
                "3) Los comentarios explican cada instrucción según el programa principal.\n"
                "4) Los push/pop pueden optimizarse para preservar solo los registros necesarios.\n"
                "5) Las etiquetas son por defecto LX, si las sustituyes usa 'replace all'.\n"
                "6) En algunos casos, especialmente en bucles y condicionales la optimización 0 puede hacer muchos accesos a memoria."
            ),
            font=("Arial", 10), fg="#1a2942", bg="#e6f0fa", wraplength=570, justify="left"
        )
        self.comment_content.pack_forget()
        frame = tk.Frame(self.win)
        frame.pack(pady=5, padx=10, fill="x")
        # Nivel de optimización + info
        tk.Label(frame, text="Nivel de optimización:", font=fuente_normal, fg=azul_oscuro).grid(row=0, column=0, sticky="w")
        self.opt_var = tk.IntVar(value=0)
        self.opt_slider = tk.Scale(frame, from_=0, to=3, orient="horizontal", variable=self.opt_var)
        self.opt_slider.grid(row=0, column=1, padx=10)
        tk.Button(frame, text="info", font=("Arial", 8, "bold"), fg="#2a4a7b", command=self.show_opt_info, width=4).grid(row=0, column=2, padx=2)
        # Comentarios
        tk.Label(frame, text="Comentarios detallados:", font=fuente_normal, fg=azul_oscuro).grid(row=1, column=0, sticky="w")
        self.comments_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, variable=self.comments_var).grid(row=1, column=1, sticky="w")
        # Folding + info
        tk.Label(frame, text="Evitar folding:", font=fuente_normal, fg=azul_oscuro).grid(row=2, column=0, sticky="w")
        self.folding_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, variable=self.folding_var).grid(row=2, column=1, sticky="w")
        tk.Button(frame, text="info", font=("Arial", 8, "bold"), fg="#2a4a7b", command=self.show_folding_info, width=4).grid(row=2, column=2, padx=2)
        # Checkbox para simplificar ensamblador
        tk.Label(frame, text="Simplificar ensamblador:", font=fuente_normal, fg=azul_oscuro).grid(row=3, column=0, sticky="w")
        self.simplify_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, variable=self.simplify_var).grid(row=3, column=1, sticky="w")
        # Archivo entrada/salida
        tk.Label(frame, text="Archivo de entrada:", font=fuente_normal, fg=azul_oscuro).grid(row=4, column=0, sticky="w")
        self.input_entry = tk.Entry(frame, width=30)
        self.input_entry.grid(row=4, column=1)
        tk.Button(frame, text="Seleccionar", font=fuente_normal, command=self.browse_file).grid(row=4, column=2, padx=5)
        tk.Label(frame, text="Archivo de salida:", font=fuente_normal, fg=azul_oscuro).grid(row=5, column=0, sticky="w")
        self.output_entry = tk.Entry(frame, width=30)
        self.output_entry.insert(0, "salida_x86.s")
        self.output_entry.grid(row=5, column=1, columnspan=2, sticky="w")
        tk.Button(
            self.win, text="Compilar", font=("Arial", 12, "bold"), bg="#2a4a7b", fg="white",
            activebackground="#19325a", activeforeground="white", command=self.compile
        ).pack(pady=20)

    def toggle_comment(self, event=None):
        if self.comment_expanded:
            self.comment_content.pack_forget()
            self.comment_label.config(text="💡 Comentarios útiles (haz clic para desplegar)")
            self.comment_expanded = False
        else:
            self.comment_content.pack(fill="x", padx=5, pady=3)
            self.comment_label.config(text="💡 Comentarios útiles (haz clic para contraer)")
            self.comment_expanded = True

    def show_dependencies_window(self, so):
        dep_win = tk.Toplevel(self.win)
        dep_win.title("Dependencias necesarias")
        dep_win.geometry("500x240")
        dep_win.resizable(False, False)
        azul_oscuro = "#1a2942"
        fuente_titulo = font.Font(family="Arial", size=13, weight="bold")
        fuente_normal = font.Font(family="Arial", size=10)
        dep_msg = self.get_dependencies_message(so)
        tk.Label(dep_win, text="Dependencias necesarias para C-x86-64", font=fuente_titulo, fg=azul_oscuro).pack(pady=(10, 5))
        msg_label = tk.Label(dep_win, text=dep_msg, justify="left", anchor="w", font=fuente_normal, fg=azul_oscuro, wraplength=470)
        msg_label.pack(padx=10, pady=(0, 10))
        if so.startswith("Linux"):
            btns = [
                ("Ubuntu/Debian", "sudo apt update && sudo apt install gcc"),
                ("Arch Linux", "sudo pacman -S gcc"),
                ("Fedora", "sudo dnf install gcc"),
                ("openSUSE", "sudo zypper install gcc"),
            ]
            btn_frame = tk.Frame(dep_win)
            btn_frame.pack(pady=(0, 10))
            for name, cmd in btns:
                def copy_cmd(c=cmd):
                    dep_win.clipboard_clear()
                    dep_win.clipboard_append(c)
                    tk.messagebox.showinfo("Copiado", "Comando copiado al portapapeles.", parent=dep_win)
                tk.Button(btn_frame, text=f"Copiar {name}", font=("Arial", 9, "bold"), fg="#2a4a7b", command=copy_cmd, width=30).pack(pady=2)
        elif so.startswith("Windows"):
            import webbrowser
            def open_url(event=None):
                webbrowser.open("https://jmeubank.github.io/tdm-gcc/")
            link = tk.Label(dep_win, text="Descargar TDM-GCC (Windows)", fg="#1a2942", cursor="hand2", font=("Arial", 10, "underline"))
            link.pack(pady=(0, 10))
            link.bind("<Button-1>", open_url)
        elif so == "macOS":
            def copy_cmd():
                dep_win.clipboard_clear()
                dep_win.clipboard_append("brew install gcc")
                tk.messagebox.showinfo("Copiado", "Comando copiado al portapapeles.", parent=dep_win)
            tk.Button(dep_win, text="Copiar comando Homebrew", font=("Arial", 9, "bold"), fg="#2a4a7b", command=copy_cmd, width=30).pack(pady=2)
        tk.Button(dep_win, text="OK", font=("Arial", 11, "bold"), bg="#2a4a7b", fg="white", command=dep_win.destroy).pack(pady=10)

    def get_dependencies_message(self, so):
        if so.startswith("Windows"):
            return (
                "Debes instalar GCC para x86-64.\n"
                "1. Descarga el instalador desde el enlace inferior (TDM-GCC recomendado).\n"
                "2. Instala y añade a la variable PATH."
            )
        elif so.startswith("Linux"):
            return (
                "Debes instalar GCC para x86-64.\n"
                "Comandos para las principales distribuciones (elige el tuyo y cópialo):"
            )
        elif so == "macOS":
            return (
                "Instala Homebrew si no lo tienes y luego ejecuta el siguiente comando en terminal:"
            )
        else:
            return "No se ha podido determinar las dependencias para tu sistema."

    def show_opt_info(self):
        win = tk.Toplevel(self.win)
        win.title("Información de optimización")
        win.geometry("420x260")
        azul_oscuro = "#1a2942"
        msg = (
            "Nivel de optimización:\n"
            "0: Sin optimización (recomendado -> código más cercano al C original).\n"
            "1: Optimización básica.\n"
            "2: Optimización estándar.\n"
            "3: Máxima optimización.\n"
        )
        tk.Label(win, text=msg, justify="left", anchor="w", font=("Arial", 10), fg=azul_oscuro, wraplength=400).pack(padx=10, pady=15)
        tk.Button(win, text="OK", font=("Arial", 11, "bold"), bg="#2a4a7b", fg="white", command=win.destroy).pack(pady=10)

    def show_folding_info(self):
        win = tk.Toplevel(self.win)
        win.title("Información sobre folding")
        win.geometry("440x260")
        azul_oscuro = "#1a2942"
        msg = (
            "Evitar folding:\n"
            "Los compiladores suelen precalcular todas las expresiones posibles con constantes (constant folding), "
            "lo que puede hacer que el código ensamblador resultante sea muy diferente al código C original.\n\n"
            "Si activas esta opción, el programa transformará automáticamente las constantes en variables locales dentro de main, "
            "evitando así el folding y generando un ensamblador más similar al C.\nPara esto se generará un archivo intermedio x_nofold.c\n\n"
            "Existen otras opciones como declarar las constantes como 'volatile' o 'extern', pero eso puede complicar el código."
        )
        tk.Label(win, text=msg, justify="left", anchor="w", font=("Arial", 10), fg=azul_oscuro, wraplength=420).pack(padx=10, pady=15)
        tk.Button(win, text="OK", font=("Arial", 11, "bold"), bg="#2a4a7b", fg="white", command=win.destroy).pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C files", "*.c")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
    def compile(self):
        src = self.input_entry.get()
        out = self.output_entry.get()
        opt = str(self.opt_var.get())
        cmts = "on" if self.comments_var.get() else "off"
        folding = "off" if self.folding_var.get() else "on"
        simplify = "on" if self.simplify_var.get() else "off"
        if not src:
            messagebox.showerror("Error", "Debes seleccionar un archivo de entrada.")
            return
        cmd = ["python3", "asmintel.py", src, opt, out, cmts, folding, simplify]
        try:
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Éxito", f"Archivo ensamblador generado: {out}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Ocurrió un error durante la compilación.")

class CMIPSWindow:
    def __init__(self, so):
        self.so = so
        self.win = tk.Toplevel()
        self.win.title("easyAssembly - C a Assembly (MIPS)")
        self.win.geometry("600x500")
        azul_oscuro = "#1a2942"
        fuente_titulo = font.Font(family="Arial", size=16, weight="bold")
        fuente_normal = font.Font(family="Arial", size=11)
        tk.Label(self.win, text="C a Assembly (MIPS)", font=fuente_titulo, fg=azul_oscuro).pack(pady=(10, 5))
        self.show_dependencies_window(so)
        # Recuadro comentario desplegable
        self.comment_frame = tk.Frame(self.win, bg="#e6f0fa", bd=2, relief="groove")
        self.comment_frame.pack(padx=10, pady=(5, 10), fill="x")
        self.comment_expanded = False
        self.comment_label = tk.Label(
            self.comment_frame,
            text="💡 Comentarios útiles (haz clic para desplegar)",
            font=("Arial", 10, "bold"), fg="#234", bg="#e6f0fa", cursor="hand2", anchor="w", justify="left"
        )
        self.comment_label.pack(fill="x", padx=5, pady=3)
        self.comment_label.bind("<Button-1>", self.toggle_comment)
        self.comment_content = tk.Label(
            self.comment_frame,
            text=(
                "1) Si hay más de un archivo fuente, compílalos por separado y luego enlázalos. "
                "Revisa los includes y los .h.\n"
                "2) Puede haber líneas innecesarias o redundantes según el contexto.\n"
                "3) Los comentarios explican cada instrucción según el programa principal.\n"
                "4) Los push/pop pueden optimizarse para preservar solo los registros necesarios.\n"
                "5) Las etiquetas son por defecto LX, si las sustituyes usa 'replace all'.\n"
                "6) En algunos casos, especialmente en bucles y condicionales la optimización 0 puede hacer muchos accesos a memoria."
            ),
            font=("Arial", 10), fg="#1a2942", bg="#e6f0fa", wraplength=570, justify="left"
        )
        self.comment_content.pack_forget()
        frame = tk.Frame(self.win)
        frame.pack(pady=5, padx=10, fill="x")
        # Nivel de optimización + info
        tk.Label(frame, text="Nivel de optimización:", font=fuente_normal, fg=azul_oscuro).grid(row=0, column=0, sticky="w")
        self.opt_var = tk.IntVar(value=0)
        self.opt_slider = tk.Scale(frame, from_=0, to=3, orient="horizontal", variable=self.opt_var)
        self.opt_slider.grid(row=0, column=1, padx=10)
        tk.Button(frame, text="info", font=("Arial", 8, "bold"), fg="#2a4a7b", command=self.show_opt_info, width=4).grid(row=0, column=2, padx=2)
        # Comentarios
        tk.Label(frame, text="Comentarios detallados:", font=fuente_normal, fg=azul_oscuro).grid(row=1, column=0, sticky="w")
        self.comments_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, variable=self.comments_var).grid(row=1, column=1, sticky="w")
        # Folding + info
        tk.Label(frame, text="Evitar folding:", font=fuente_normal, fg=azul_oscuro).grid(row=2, column=0, sticky="w")
        self.folding_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, variable=self.folding_var).grid(row=2, column=1, sticky="w")
        tk.Button(frame, text="info", font=("Arial", 8, "bold"), fg="#2a4a7b", command=self.show_folding_info, width=4).grid(row=2, column=2, padx=2)
        # Checkbox para simplificar ensamblador
        tk.Label(frame, text="Simplificar ensamblador:", font=fuente_normal, fg=azul_oscuro).grid(row=3, column=0, sticky="w")
        self.simplify_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, variable=self.simplify_var).grid(row=3, column=1, sticky="w")
        # Archivo entrada/salida
        tk.Label(frame, text="Archivo de entrada:", font=fuente_normal, fg=azul_oscuro).grid(row=4, column=0, sticky="w")
        self.input_entry = tk.Entry(frame, width=30)
        self.input_entry.grid(row=4, column=1)
        tk.Button(frame, text="Seleccionar", font=fuente_normal, command=self.browse_file).grid(row=4, column=2, padx=5)
        tk.Label(frame, text="Archivo de salida:", font=fuente_normal, fg=azul_oscuro).grid(row=5, column=0, sticky="w")
        self.output_entry = tk.Entry(frame, width=30)
        self.output_entry.insert(0, "salida_mips.s")
        self.output_entry.grid(row=5, column=1, columnspan=2, sticky="w")
        tk.Button(
            self.win, text="Compilar", font=("Arial", 12, "bold"), bg="#2a4a7b", fg="white",
            activebackground="#19325a", activeforeground="white", command=self.compile
        ).pack(pady=20)

    def toggle_comment(self, event=None):
        if self.comment_expanded:
            self.comment_content.pack_forget()
            self.comment_label.config(text="💡 Comentarios útiles (haz clic para desplegar)")
            self.comment_expanded = False
        else:
            self.comment_content.pack(fill="x", padx=5, pady=3)
            self.comment_label.config(text="💡 Comentarios útiles (haz clic para contraer)")
            self.comment_expanded = True

    def show_dependencies_window(self, so):
        dep_win = tk.Toplevel(self.win)
        dep_win.title("Dependencias necesarias")
        dep_win.geometry("500x240")
        dep_win.resizable(False, False)
        azul_oscuro = "#1a2942"
        fuente_titulo = font.Font(family="Arial", size=13, weight="bold")
        fuente_normal = font.Font(family="Arial", size=10)
        dep_msg = self.get_dependencies_message(so)
        tk.Label(dep_win, text="Dependencias necesarias para C-MIPS", font=fuente_titulo, fg=azul_oscuro).pack(pady=(10, 5))
        msg_label = tk.Label(dep_win, text=dep_msg, justify="left", anchor="w", font=fuente_normal, fg=azul_oscuro, wraplength=470)
        msg_label.pack(padx=10, pady=(0, 10))
        if so.startswith("Linux"):
            btns = [
                ("Ubuntu/Debian", "sudo apt update && sudo apt install gcc-mips-linux-gnu"),
                ("Arch Linux", "sudo pacman -S mips-linux-gnu-gcc"),
                ("Fedora", "sudo dnf install mips-linux-gnu-gcc"),
                ("openSUSE", "sudo zypper install cross-mips-linux-gnu-gcc"),
            ]
            btn_frame = tk.Frame(dep_win)
            btn_frame.pack(pady=(0, 10))
            for name, cmd in btns:
                def copy_cmd(c=cmd):
                    dep_win.clipboard_clear()
                    dep_win.clipboard_append(c)
                    tk.messagebox.showinfo("Copiado", "Comando copiado al portapapeles.", parent=dep_win)
                tk.Button(btn_frame, text=f"Copiar {name}", font=("Arial", 9, "bold"), fg="#2a4a7b", command=copy_cmd, width=30).pack(pady=2)
        elif so.startswith("Windows"):
            import webbrowser
            def open_url(event=None):
                webbrowser.open("https://github.com/bminor/binutils-gdb/releases")
            link = tk.Label(dep_win, text="Descargar toolchain MIPS (Windows)", fg="#1a2942", cursor="hand2", font=("Arial", 10, "underline"))
            link.pack(pady=(0, 10))
            link.bind("<Button-1>", open_url)
        elif so == "macOS":
            def copy_cmd():
                dep_win.clipboard_clear()
                dep_win.clipboard_append("brew install FiloSottile/musl-cross/mips-linux-musl-cross")
                tk.messagebox.showinfo("Copiado", "Comando copiado al portapapeles.", parent=dep_win)
            tk.Button(dep_win, text="Copiar comando Homebrew", font=("Arial", 9, "bold"), fg="#2a4a7b", command=copy_cmd, width=30).pack(pady=2)
        tk.Button(dep_win, text="OK", font=("Arial", 11, "bold"), bg="#2a4a7b", fg="white", command=dep_win.destroy).pack(pady=10)

    def get_dependencies_message(self, so):
        if so.startswith("Windows"):
            return (
                "Debes instalar el toolchain MIPS (mips-linux-gnu-gcc).\n"
                "1. Descarga el instalador desde el enlace inferior.\n"
                "2. Instala y añade a la variable PATH."
            )
        elif so.startswith("Linux"):
            return (
                "Debes instalar el compilador MIPS (mips-linux-gnu-gcc).\n"
                "Comandos para las principales distribuciones (elige el tuyo y cópialo):"
            )
        elif so == "macOS":
            return (
                "Instala Homebrew si no lo tienes y luego ejecuta el siguiente comando en terminal:"
            )
        else:
            return "No se ha podido determinar las dependencias para tu sistema."

    def show_opt_info(self):
        win = tk.Toplevel(self.win)
        win.title("Información de optimización")
        win.geometry("420x260")
        azul_oscuro = "#1a2942"
        msg = (
            "Nivel de optimización:\n"
            "0: Sin optimización (recomendado -> código más cercano al C original).\n"
            "1: Optimización básica.\n"
            "2: Optimización estándar.\n"
            "3: Máxima optimización.\n"
        )
        tk.Label(win, text=msg, justify="left", anchor="w", font=("Arial", 10), fg=azul_oscuro, wraplength=400).pack(padx=10, pady=15)
        tk.Button(win, text="OK", font=("Arial", 11, "bold"), bg="#2a4a7b", fg="white", command=win.destroy).pack(pady=10)

    def show_folding_info(self):
        win = tk.Toplevel(self.win)
        win.title("Información sobre folding")
        win.geometry("440x260")
        azul_oscuro = "#1a2942"
        msg = (
            "Evitar folding:\n"
            "Los compiladores suelen precalcular todas las expresiones posibles con constantes (constant folding), "
            "lo que puede hacer que el código ensamblador resultante sea muy diferente al código C original.\n\n"
            "Si activas esta opción, el programa transformará automáticamente las constantes en variables locales dentro de main, "
            "evitando así el folding y generando un ensamblador más similar al C.\nPara esto se generará un archivo intermedio x_nofold.c\n\n"
            "Existen otras opciones como declarar las constantes como 'volatile' o 'extern', pero eso puede complicar el código."
        )
        tk.Label(win, text=msg, justify="left", anchor="w", font=("Arial", 10), fg=azul_oscuro, wraplength=420).pack(padx=10, pady=15)
        tk.Button(win, text="OK", font=("Arial", 11, "bold"), bg="#2a4a7b", fg="white", command=win.destroy).pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C files", "*.c")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
    def compile(self):
        src = self.input_entry.get()
        out = self.output_entry.get()
        opt = str(self.opt_var.get())
        cmts = "on" if self.comments_var.get() else "off"
        folding = "off" if self.folding_var.get() else "on"
        simplify = "on" if self.simplify_var.get() else "off"
        if not src:
            messagebox.showerror("Error", "Debes seleccionar un archivo de entrada.")
            return
        cmd = ["python3", "asmmips.py", src, opt, out, cmts, folding, simplify]
        try:
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Éxito", f"Archivo ensamblador generado: {out}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Ocurrió un error durante la compilación.")

def main():
    root = tk.Tk()
    root.title("easyAssembly - Principal")
    root.configure(bg="#e6f0fa")
    def start_main(so):
        SelectWindow(so)
    WelcomeWindow(root, start_main)
    root.mainloop()

if __name__ == "__main__":
    main()
