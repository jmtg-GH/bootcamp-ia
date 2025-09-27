#Juego de "Adivina el número"
numero=18.0
adivinanza=1
while(adivinanza!=numero):
    adivinanza = float(input("Adivina el número: "))
    print("El número es mayor" if adivinanza<numero else "El número es menor" if (adivinanza>numero) else f"¡Felicitaciones!, el número era {adivinanza}")