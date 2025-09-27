#Desarrollar un prog. que imprima la suma de diez números ingresados

suma=0
x=1

valor=int(input("Ingrese un número: "))
suma+=valor

while x<10:
    valor=int(input("Ingrese otro número: "))
    suma+=valor
    x+=1
print(f"Suma acumulada: {suma}")