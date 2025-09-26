#CALCULADORA
#Des. un programa que me muestre un menú de op. básicas. Que pida dos números.
#Dependiendo la operación, muestre su resultado

print("CALCULADORA")
print("Seleccione un número de la lista para realizar una operación:")
print("1. Suma")
print("2. Resta")
print("3. Multiplicación")
print("4. División")

opcion = input("Operación: ")
num1 = float(input("Ingrese el primer número: "))
num2 = float(input("Ingrese el segundo número: "))

match opcion:
  case '1':
    print(f"{num1} + {num2} = {num1 + num2}")
  case '2':
    print(f"{num1} - {num2} = {num1 - num2}")
  case '3':
    print(f"{num1} x {num2} = {num1 * num2}")
  case '4':
    if num2 == 0: print("Error. No se puede dividir entre cero")
    else: print(f"{num1} / {num2} = {num1 / num2}")
  case _:
    print("Ingrese una operación válida")