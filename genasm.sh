#!/bin/bash

usage() {
  echo "Uso: $0 <archivo.c> <opt_level: 0|1|2|3|s|g> <salida.s> <comments:on|off> <folding:on|off>"
  exit 1
}

# Comprobar número de argumentos
[ $# -ne 5 ] && usage

# Parámetros
src="$1"
opt="$2"
out="$3"
cmts="$4"
folding="$5"

# Validar existencia del archivo fuente
[ ! -f "$src" ] && { echo "Error: El archivo '$src' no existe."; exit 1; }

# Validar nivel de optimización
case "$opt" in
  0|1|2|3|s|g) ;;
  *) echo "Error: Nivel de optimización inválido: $opt"; exit 1 ;;
esac

# Activar o desactivar comentarios
case "$cmts" in
  on) vasm="-fverbose-asm" ;;
  off) vasm="" ;;
  *) echo "Error: El cuarto parámetro debe ser 'on' o 'off'."; exit 1 ;;
esac

# Nombre temporal si folding está desactivado
if [ "$folding" == "off" ]; then
  edit_src="${src%.c}_nofold.c"

  # Copiar archivo original y modificar #define A ... a int A = ... dentro del main
  awk '
  BEGIN {
    inserted = 0;
  }
  # Capturar defines
  /^#define[ \t]+([A-Za-z_][A-Za-z0-9_]*)[ \t]+([0-9]+)/ {
    macro_name = $2;
    macro_val = $3;
    macros[macro_name] = macro_val;
    next;
  }
  # Insertar dentro de main
  /^int[ \t]+main[ \t]*\(.*\)[ \t]*\{/ {
    print;
    for (name in macros) {
      print "    int " name " = " macros[name] ";";
    }
    inserted = 1;
    next;
  }
  { print; }
  ' "$src" > "$edit_src"

  src="$edit_src"
fi

# Ejecutar compilación
arm-none-eabi-gcc -S -O"$opt" -mcpu=arm7tdmi -mthumb-interwork $vasm "$src" -o "$out"

# Comprobar resultado
if [ $? -eq 0 ]; then
  echo "✅ Ensamblador generado en '$out' con -O$opt, comentarios: $cmts, folding: $folding"
else
  echo "❌ Error en la compilación"
  exit 1
fi
