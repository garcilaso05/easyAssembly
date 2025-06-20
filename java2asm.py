import sys
import platform

def usage():
    print("Uso: python java2asm_helper.py <SO: linux|windows> <arquitectura: x86_64|armv7|riscv|mips>")
    sys.exit(1)

if len(sys.argv) != 3:
    usage()

so = sys.argv[1].lower()
arch = sys.argv[2].lower()

if so not in ["linux", "windows"]:
    print("❌ SO no soportado. Usa 'linux' o 'windows'.")
    sys.exit(1)

if arch not in ["x86_64", "armv7", "riscv", "mips"]:
    print("❌ Arquitectura no válida. Usa: x86_64, armv7, riscv, mips")
    sys.exit(1)

print("\n📦 PASO 1: Instalar GraalVM con Native Image")
if so == "linux":
    print("1. Instala SDKMAN si no lo tienes:")
    print("   curl -s https://get.sdkman.io | bash")
    print("   source $HOME/.sdkman/bin/sdkman-init.sh")
    print("2. Instala GraalVM (ejemplo Java 17):")
    print("   sdk install java 22.3.1.r17-nik")
    print("   sdk use java 22.3.1.r17-nik")
    print("3. Instala Native Image:")
    print("   gu install native-image")
else:
    print("1. Descarga GraalVM desde: https://www.graalvm.org/downloads/")
    print("2. Extrae el zip y configura JAVA_HOME")
    print("3. Abre cmd o PowerShell con entorno GraalVM")
    print("4. Ejecuta:")
    print("   gu.cmd install native-image")

print("\n🛠 PASO 2: Compilar tu código Java a binario nativo")
print("   native-image -o mi_programa MiClase")

print("\n🧩 PASO 3: Obtener ensamblador para arquitectura", arch.upper())

if arch == "x86_64":
    print("   objdump -d mi_programa > salida_x86_64.s")
elif arch == "armv7":
    print("   arm-none-eabi-objdump -d mi_programa > salida_armv7.s")
elif arch == "riscv":
    print("   riscv64-unknown-elf-objdump -d mi_programa > salida_rv64.s")
elif arch == "mips":
    print("   mipsel-linux-gnu-objdump -d mi_programa > salida_mips.s")

print("\n📘 Notas:")
print("- Asegúrate de tener instalado el toolchain adecuado para el objdump (pacman, apt, msys2, etc.)")
print("- Puedes usar Docker o toolchains externos si no compilas directamente en esa arquitectura.")
print("- El binario generado por Native Image es para tu arquitectura actual; para otra, necesitas cross-compiling (avanzado).")
print("\n✅ Proceso completado. Puedes copiar y ejecutar los comandos paso a paso. ✨")
