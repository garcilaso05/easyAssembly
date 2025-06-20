// ejemplo.c
int main() {
    int i = 0;
    int suma = 0;
    int limite = 10;

    // Bucle while: sumar los primeros 10 números naturales
    while (i < limite) {
        // Condicional: solo sumar si el número es par
        if (i % 2 == 0) {
            suma += i;
        } else {
            suma += 1;  // sumar 1 si es impar (sólo para mostrar uso del else)
        }
        i++;
    }

    // Bucle for: modificar el valor de suma
    for (int j = 0; j < 5; j++) {
        if (suma > 10) {
            suma -= j;
        }
    }

    // En este punto, suma contiene un valor resultante
    // No se hace ninguna salida ni impresión

    return 0;
}
