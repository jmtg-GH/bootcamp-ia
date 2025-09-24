#Desarrollar un programa que, de acuerdo a una fecha,
# me muestre si es mi cuempleaños o no
print("Digite mi fecha de nacimiento")
while(True):
    try:
        dd=int(input("Día: "))
        mm=int(input("Mes: "))
        aa=int(input("Año: "))
        #Fecha de mi cumpleaños: 28/02/96
        if(dd < 0 or dd > 29
            or mm < 0 or mm > 12
            or aa < 0 or aa > 2025):
            print("Fecha inválida, por favor ingrese una fecha válida")
            continue
        elif(dd == 28 and mm == 2 and (aa == 96 or aa == 1996)):
            print("¡Ese es mi cumpleaños! El 28/Feb/1996")
            break
        else:
            print("Ese no es mi cumpleaños, intenta de nuevo")
    except ValueError:
        print("Ingrese solo un valor numérico")