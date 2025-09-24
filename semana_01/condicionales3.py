#Desarrollar un programa que evalúe una nota. 
#Si la nota está por encima de 3.0, imprima "Aprobó",
#por debajo "Reprobó"
nota = float(input("Ingrese la nota: "))

if nota < 3.0:
    print(f"Reprobó con una nota de {nota}")
else:
    print(f"Aprobó con una nota de {nota}")