# 1. Importamos la clase Flask desde el paquete que acabamos de instalar.
#    Con render_template le decimos a Flask que busque en la carpeta de plantillas
#    y muestre eso al usuario en una función específica.
#    Implementamos el método "request" para recibir peticiones desde el HTML
from flask import Flask, render_template, request

# 2. Creamos una instancia de la aplicación.
#    __name__ es una variable especial de Python que le dice a Flask dónde buscar
#    recursos como plantillas. Es como darle a la app un punto de partida.
app = Flask(__name__)

# 3. Definimos una "ruta". Esto es como una dirección URL específica.
#    El decorador @app.route('/') le dice a Flask: "Cuando alguien visite
#    la página principal del sitio (la raíz '/'), ejecuta la función que está justo debajo".
#    Le decimos a la ruta que ahora acepta tanto peticiones GET como POST.
@app.route('/', methods=['GET','POST'])
def pagina_principal():
    # 4. La función devuelve el contenido que se mostrará en el navegador.
    #    Por ahora, es solo un simple texto. return "¡La página web funciona!"
    #    El nuevo texto se encuenta en la plantilla llamada "index.html" return render_template('index.html')
    #    Verificamos si el método de la petición es POST (es decir, si se envió el formulario).
    # Creamos una variable 'resultado' y la inicializamos en None.
    # Esto es para que exista incluso antes de que se envíe el formulario.
    resultado = None
    if request.method == 'POST':
        # 4.1 Accedemos a los datos del formulario usando su atributo 'name'.
        #     request.form es como un diccionario que contiene los datos.
        #     Lo convertimos a float para poder hacer cálculos matemáticos.
        masa = float(request.form['masa'])
        aceleracion = float(request.form['aceleracion'])

        # 4.2 Calculamos la fuerza
        fuerza = masa * aceleracion

        # 4.3 Por ahora, solo imprimiremos el resultado en la terminal
        #     para verificar que todo funciona.
        resultado = f'La fuerza resultante es: {fuerza:.2f} N'
        # El :.2f formatea el número para que solo tenga 2 decimales.
    
    # 2. Pasamos la variable 'resultado' a la plantilla.
    #    Esto funciona tanto para GET (donde resultado es None)
    #    como para POST (donde tiene el valor calculado).
    return render_template('index.html', resultado=resultado)

# 5. Esta es una condición estándar en Python.
#    Significa: "Solo si ejecuto este archivo directamente (python app.py),
#    entonces inicia el servidor de desarrollo".
if __name__ == '__main__':
    # app.run() inicia el servidor. debug=True es muy útil:
    # reinicia el servidor automáticamente cuando hacemos cambios y
    # nos muestra errores detallados en el navegador.
    app.run(debug=True)