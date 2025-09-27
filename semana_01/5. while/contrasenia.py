#Validar contraseña
passw="password123"
comparar=input("\nIngrese la contraseña: ")
print("")
while(comparar!=passw):
    print("Contraseña incorrecta.\n")
    comparar=input("Ingrese la contraseña: ")
print("Access granted!\n")