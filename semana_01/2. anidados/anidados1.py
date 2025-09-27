#Desarrollar un programa que me permita calcular,
# con respecto a una edad si:
#Es niño: <14
#Adolescente: <18
#Adulto >= 18
edad = input()
try:
    if int(edad) <= 14:
        print("Es niño")
    elif int(edad) < 18:
        print("Es adolescente")
    else:
        print("Es adulto")
    pass
except ValueError:
    print("Valor inválido")
    pass