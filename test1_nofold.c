int sumar (int a, int b) {

    int r = a + b;
    return r;

}

int main() {
    int A = 2;
    int suma = sumar(5, A);
    int resta = 6 - A;
    int multiplicacion = 7 * A;
    int division = 4 / A;
    int modulo = 4 % A;

    int resultado = (suma + resta) * (multiplicacion - division);

    return 0;
}
