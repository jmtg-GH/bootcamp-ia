#Desarrollar un programa que me permita calcular,
# con respecto a una edad si:
#Es niño: <14
#Adolescente: <18
#Adulto >= 18
while(True):
    try:
        edad = int(input("Ingrese su edad: "))
        if(edad < 0 or edad > 120):
            print("Error: Por favor, ingrese una edad válida (entre 0 y 120).")
            continue
        elif edad <= 14:
            categoria = "Es niño"
        elif edad < 18:
            categoria = "Es adolescente"
        elif edad < 60:
            categoria = "Es adulto"
        else:
            categoria = "Es adulto mayor"

        print(categoria)
        break
    except ValueError:
        print("Error: Por favor, ingrese solo números enteros.")