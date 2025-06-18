import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

class CodegenApp:
    def __init__(self, root):
        self.root = root
        root.title("Generador de Ensamblador")

        # Lenguaje
        tk.Label(root, text="Lenguaje:").grid(row=0, column=0, sticky="w")
        self.lang_var = tk.StringVar(value="C")
        tk.OptionMenu(root, self.lang_var, "C").grid(row=0, column=1, sticky="ew")

        # Arquitectura
        tk.Label(root, text="Arquitectura:").grid(row=1, column=0, sticky="w")
        self.arch_var = tk.StringVar(value="ARMv7")
        tk.OptionMenu(root, self.arch_var, "ARMv7").grid(row=1, column=1, sticky="ew")

        # Optimización
        tk.Label(root, text="Nivel de optimización:").grid(row=2, column=0, sticky="w")
        self.opt_var = tk.StringVar(value="0")
        tk.OptionMenu(root, self.opt_var, "0", "1", "2", "3", "s", "g").grid(row=2, column=1, sticky="ew")

        # Comentarios
        self.comments_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Comentarios detallados", variable=self.comments_var).grid(row=3, columnspan=2, sticky="w")

        # Folding
        self.folding_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Evitar folding", variable=self.folding_var).grid(row=4, columnspan=2, sticky="w")

        # Archivo entrada
        tk.Label(root, text="Archivo de entrada:").grid(row=5, column=0, sticky="w")
        self.input_entry = tk.Entry(root)
        self.input_entry.grid(row=5, column=1, sticky="ew")
        tk.Button(root, text="Seleccionar", command=self.browse_file).grid(row=5, column=2)

        # Archivo salida
        tk.Label(root, text="Archivo de salida:").grid(row=6, column=0, sticky="w")
        self.output_entry = tk.Entry(root)
        self.output_entry.insert(0, "salida.s")
        self.output_entry.grid(row=6, column=1, columnspan=2, sticky="ew")

        # Botón ejecutar
        tk.Button(root, text="Ejecutar compilación", command=self.compile).grid(row=7, columnspan=3, pady=10)

        # Ajuste de columnas
        root.grid_columnconfigure(1, weight=1)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C files", "*.c")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)

    def compile(self):
        src = self.input_entry.get()
        out = self.output_entry.get()
        opt = self.opt_var.get()
        cmts = "on" if self.comments_var.get() else "off"
        folding = "off" if self.folding_var.get() else "on"

        if not src:
            messagebox.showerror("Error", "Debes seleccionar un archivo de entrada.")
            return

        cmd = ["./genasm.sh", src, opt, out, cmts, folding]
        try:
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Éxito", f"Archivo ensamblador generado: {out}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Ocurrió un error durante la compilación.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodegenApp(root)
    root.mainloop()
