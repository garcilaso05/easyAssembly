# easyAssembly

**easyAssembly** es una herramienta visual y multiplataforma para traducir código fuente en **C** o **Java** a ensamblador para diferentes arquitecturas (ARM7, x86-64, MIPS, ...).

---

## ¿Para qué sirve?

- **Aprendizaje:** Analiza cómo se traduce tu código a bajo nivel, compara optimizaciones y comprende el funcionamiento interno de los compiladores.
- **Optimización:** Extrae funciones críticas, edítalas en ensamblador y vuelve a integrarlas en tus proyectos para obtener el máximo rendimiento.

---

## Características principales

- Interfaz gráfica intuitiva (Tkinter).
- Traducción de C y Java a ensamblador para ARM7, x86-64, MIPS.
- Selección de nivel de optimización, comentarios, folding y simplificación del código ensamblador.
- Visualización y comparación del código generado.
- Explicaciones y ayudas integradas para cada arquitectura y opción.
- Uso tanto gráfico como por línea de comandos.

---

## Instalación y requisitos

- **Python 3.x**
- **Tkinter** (incluido en la mayoría de instalaciones de Python)
- Compiladores:
  - **ARM:** `arm-none-eabi-gcc`
  - **x86-64:** `gcc`
  - **MIPS:** `mips-linux-gnu-gcc`
- (Opcional) **Java JDK** para integración JNI

Instala los compiladores según tu sistema operativo (ver ayuda en la propia interfaz).

---

## Ejecución

### Interfaz gráfica

```bash
python3 interfaz.py
```

### Línea de comandos

```bash
python3 asmarm7.py archivo.c 0 salida.s on off on
python3 asmintel.py archivo.c 2 salida_x86.s off on off
python3 asmmips.py archivo.c 1 salida_mips.s on off on
```
Parámetros:  
`<archivo.c> <nivel_opt: 0|1|2|3|s|g> <salida.s> <comments:on|off> <folding:on|off> <simplify:on|off>`

---

## ¿Cómo usar el ensamblador generado?

### ✅ En C: llamar a funciones escritas en ensamblador

1. Escribe tu función en ensamblador (ejemplo ARM):

    ```asm
    .global mi_suma
    .type mi_suma, %function
    mi_suma:
        @ int mi_suma(int a, int b)
        add r0, r0, r1
        bx lr
    ```

2. Declara la función en tu archivo `.c`:

    ```c
    extern int mi_suma(int a, int b);

    int main() {
        int r = mi_suma(5, 7);
        return 0;
    }
    ```

3. Compila todo junto:

    ```bash
    arm-none-eabi-gcc main.c funcion.S -o programa.elf
    ```

---

### ✅ En Java: usar ensamblador mediante JNI (Java Native Interface)

1. Crea una clase Java:

    ```java
    public class NativeOps {
        static {
            System.loadLibrary("asmcode");
        }
        public native int sumaASM(int a, int b);
    }
    ```

2. Genera el header:

    ```bash
    javac NativeOps.java
    javah NativeOps
    ```

3. Implementa la función en C y llama al ASM:

    ```c
    #include "NativeOps.h"
    extern int mi_suma(int a, int b); // definida en ensamblador
    JNIEXPORT jint JNICALL Java_NativeOps_sumaASM(JNIEnv *env, jobject obj, jint a, jint b) {
        return mi_suma(a, b);
    }
    ```

4. Compila el `.c` y `.S` como biblioteca compartida:

    ```bash
    gcc -c -fPIC NativeOps.c funcion.S
    gcc -shared -o libasmcode.so NativeOps.o funcion.o
    ```

5. Ejecuta en Java:

    ```bash
    java -Djava.library.path=. NativeOps
    ```

---

## Funciones adicionales

- Analiza el impacto de la optimización en el ensamblador.
- Compara código generado por diferentes arquitecturas.
- Útil para docencia, prácticas y análisis de bajo nivel.
- Facilita la integración de rutinas optimizadas en proyectos reales.

---

## ¡Disfruta aprendiendo y optimizando con easyAssembly!
