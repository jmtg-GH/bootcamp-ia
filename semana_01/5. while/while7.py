#Des. un prog. que me sume números hasta que el usuario ingrese el cero
suma = 0
valor = float(input("Si ingresa el cero, el programa parará y" \
            "le mostrará la suma respectiva a los valores ingresados.\nIngrese un valor: "))
suma += valor
print(f"El acumulado es: {suma}")
while(valor!=0):
    valor = float(input("Ingrese otro valor: "))
    suma += valor
    print(f"El acumulado es: {suma}")
print(f"La suma total es: {suma}")