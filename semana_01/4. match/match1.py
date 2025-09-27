#Desarrollar un programa que, de acuerdo a un número del 1 al 7,
#me imprima el día de la semana al que pertenece el número

#"Match evalúa casos y, dependiento del caso, ejecuta una acción."

print("Día de la semana")
dia = int(input("Ingrese número de 1 a 7 que correspondería a un día de la semana: "))

match dia:
	case 1:
		print("Lunes")
	case 2:
		print("Martes")
	case 3:
		print("Miércoles")
	case 4:
		print("Jueves")
	case 5:
		print("Viernes")
	case 6:
		print("Sábado")
	case 7:
		print("Domingo")
	case _:
		print("Dato Inválido")