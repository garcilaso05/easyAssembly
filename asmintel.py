import sys
import os
import subprocess
import re

def usage():
    print("Uso: python asmintel.py <archivo.c> <opt_level: 0|1|2|3|s|g> <salida.s> <comments:on|off> <folding:on|off> <simplify:on|off>")
    sys.exit(1)

if len(sys.argv) != 7:
    usage()

src, opt, out, cmts, folding, simplify = sys.argv[1:]

if not os.path.isfile(src):
    print(f"Error: El archivo '{src}' no existe.")
    sys.exit(1)

if opt not in ["0", "1", "2", "3", "s", "g"]:
    print(f"Error: Nivel de optimización inválido: {opt}")
    sys.exit(1)

vasm = "-fverbose-asm" if cmts == "on" else ""
if cmts not in ["on", "off"]:
    print("Error: El cuarto parámetro debe ser 'on' o 'off'.")
    sys.exit(1)

# Si se desactiva folding, convertir defines a variables dentro de main
if folding == "off":
    edit_src = src.replace(".c", "_nofold.c")
    with open(src, 'r') as f:
        lines = f.readlines()

    defines = {}
    output_lines = []
    insert_done = False

    define_re = re.compile(r"^#define\s+(\w+)\s+(\d+)")
    main_re = re.compile(r"^int\s+main\s*\(.*\)\s*\{")

    for line in lines:
        match = define_re.match(line)
        if match:
            name, val = match.groups()
            defines[name] = val
            continue  # No incluir #define en el archivo modificado

        if main_re.match(line) and not insert_done:
            output_lines.append(line)
            for k, v in defines.items():
                output_lines.append(f"    int {k} = {v};\n")
            insert_done = True
            continue

        output_lines.append(line)

    with open(edit_src, 'w') as f:
        f.writelines(output_lines)

    src = edit_src

# Ejecutar compilación para x86 con sintaxis Intel
cmd = ["gcc", "-S", f"-O{opt}", "-masm=intel"]
if vasm:
    cmd.append(vasm)
cmd.extend([src, "-o", out])

try:
    subprocess.run(cmd, check=True)
    print(f"✅ Ensamblador x86 generado en '{out}' con -O{opt}, comentarios: {cmts}, folding: {folding}")
except subprocess.CalledProcessError:
    print("❌ Error en la compilación")
    sys.exit(1)

# Simplificar ensamblador
if simplify == "on":
    try:
        with open(out, 'r') as f:
            asm_lines = f.readlines()

        simplified = []
        skip_prefixes = (".file", ".intel_syntax", ".section", ".ident", ".cfi_", ".type", ".size", "#", "//", "/*", "*/")

        for line in asm_lines:
            stripped = line.lstrip()
            if any(stripped.startswith(p) for p in skip_prefixes):
                continue
            # Opcional: puedes modificar los comentarios si quieres
            line = line.replace("#", "#;")
            simplified.append(line)

        with open(out, 'w') as f:
            f.writelines(simplified)

        print(f"🧹 Ensamblador simplificado en '{out}'")

    except Exception as e:
        print(f"⚠️ Error al simplificar ensamblador: {e}")
