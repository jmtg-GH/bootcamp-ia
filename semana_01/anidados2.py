#Desarrollar un programa que, con respecto a un promedio,
# me evalúe: 
#>4.5 Excelente
#>3.5 Bueno
#>3 Aceptable
#>2 En recuperación
#<2 Reprobado
while(True):
    try:
        nota1=float(input("Ingrese nota 1: "))
        nota2=float(input("Ingrese nota 2: "))
        nota3=float(input("Ingrese nota 3: "))
        promedio=(nota1+nota2+nota3)/3
        print("El promedio es: " + str(round(promedio,2)))
        if(promedio <= 5 or promedio >= 0):
            if(promedio >= 4.5):
                print("Excelente")
                break
            elif(promedio >= 3.5):
                print("Bueno")
                break
            elif(promedio >= 3):
                print("Aceptable")
                break
            elif(promedio >= 2):
                print("En recuperación")
                break
            else:
                print("Reprobado")
                break
        else:
            print("Valor inválido")
        pass
    except ValueError:
        print("Valor inválido")
        pass