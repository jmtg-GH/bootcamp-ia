#Desarrolle un prog. que muestre la tabla de multiplicar de un número deseado por el usuario
valor = int(input("\nIngrese un número: "))
print(f"\nLA TABLA DEL {valor} (de 1 a 100) es: \n\n","-"*30,"\n")
for i in range(1, 101):
    print(f"-> {valor} x {i} = {valor*i}")
print("")