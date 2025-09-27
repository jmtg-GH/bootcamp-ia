#La tabla de multiplicar
i=1
valor = int(input("\nIngrese un número: "))
print(f"\nLA TABLA DEL {valor} (del 1 al 100)\n")
while(i<=100):
    print(f"{valor} x {i} = {valor*i}")
    i+=1