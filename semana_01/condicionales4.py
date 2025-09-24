#Desarrollar un programa en el que se ingresen tres notas,
#se calcule el promedio y se evalúe la nota final

nota_1 = float(input("Ingrese la nota 1: "))
nota_2 = float(input("Ingrese la nota 2: "))
nota_3 = float(input("Ingrese la nota 3: "))

nota = (nota_1+nota_2+nota_3)/3

if nota < 3.0:
    print(f"Reprobó con una nota de {nota}")
else:
    print(f"Aprobó con una nota de {nota}")