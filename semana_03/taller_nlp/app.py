# 1. Importamos 'request' para poder leer los datos del formulario.
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 2. Añadimos methods=['GET', 'POST'] a la ruta del chatbot.
@app.route('/chatbot-salud', methods=['GET', 'POST'])
def chatbot_salud():
    # 3. Creamos una variable para la respuesta, inicialmente vacía.
    respuesta = None

    # 4. Si el usuario envió el formulario (método POST)...
    if request.method == 'POST':
        # Obtenemos los síntomas del formulario.
        sintomas = request.form['sintomas']
        
        # Convertimos el texto a minúsculas para una detección más fiable.
        sintomas_lower = sintomas.lower()

        # --- Lógica del "Detector de Palabras" ---
        if 'fiebre' in sintomas_lower:
            respuesta = "Parece que tienes fiebre. Te recomiendo descansar, tomar líquidos y monitorizar tu temperatura. Si persiste, consulta a un médico."
        elif 'cabeza' in sintomas_lower:
            respuesta = "Para un dolor de cabeza, puedes probar a descansar en un lugar tranquilo y oscuro. Beber agua también ayuda. Si es muy intenso o recurrente, es mejor ver a un médico."
        elif 'estómago' in sintomas_lower or 'panza' in sintomas_lower:
            respuesta = "Si te duele el estómago, intenta comer alimentos suaves y evitar comidas pesadas o grasosas. Si el dolor es fuerte o no se va, consulta a un profesional."
        else:
            respuesta = "No reconozco esos síntomas. Recuerda que soy un bot simple. Para cualquier problema de salud, lo más seguro es consultar a un médico."

    # 5. Renderizamos la misma plantilla, pero ahora le pasamos la variable 'respuesta'.
    #    Si es una petición GET, 'respuesta' será None.
    #    Si es POST, contendrá el mensaje que calculamos.
    return render_template('chatbot_salud.html', respuesta=respuesta)

@app.route('/asistente-clima', methods=['GET', 'POST'])
def asistente_clima():
    respuesta_clima = None

    if request.method == 'POST':
        # Usamos el 'name' del textarea de clima.html
        pregunta = request.form['pregunta_clima']
        pregunta_lower = pregunta.lower()

        # --- Lógica de Clasificación de Intención ---
        if 'llover' in pregunta_lower or 'lluvia' in pregunta_lower:
            respuesta_clima = "Parece que podría llover. Te recomiendo llevar paraguas por si acaso. ☔"
        elif 'calor' in pregunta_lower or 'sol' in pregunta_lower:
            respuesta_clima = "Sí, parece que será un día caluroso. ¡No olvides mantenerte hidratado y usar protector solar! ☀️"
        elif 'frío' in pregunta_lower:
            respuesta_clima = "Se espera un día frío. ¡Asegúrate de abrigarte bien si vas a salir! 🧣"
        elif 'nublado' in pregunta_lower:
            respuesta_clima = "El cielo estará mayormente nublado. Un día perfecto para una bebida caliente. ☁️"
        else:
            respuesta_clima = "No tengo información sobre eso, pero te deseo que tengas un excelente día."

    # Renderizamos la plantilla del clima, pasándole la respuesta.
    return render_template('clima.html', respuesta_clima=respuesta_clima)

@app.route('/clasificador-animales', methods=['GET', 'POST'])
def clasificador_animales():
    animal_adivinado = None

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        desc_lower = descripcion.lower()

        # --- Lógica del Detective (Sistema de Reglas) ---
        # Para adivinar "perro", necesitamos ambas pistas.
        if ('cuatro patas' in desc_lower or '4 patas' in desc_lower) and 'ladra' in desc_lower:
            animal_adivinado = "Creo que estás hablando de un perro 🐕"
        # Para adivinar "gato", necesitamos ambas pistas.
        elif 'maulla' in desc_lower and 'dormir' in desc_lower:
            animal_adivinado = "Creo que estás hablando de un gato 🐈"
        # Para adivinar "pájaro", necesitamos ambas pistas.
        elif 'vuela' in desc_lower and 'alas' in desc_lower:
            animal_adivinado = "Creo que estás hablando de un pájaro 🐦"
        else:
            animal_adivinado = "¡Uhm, no estoy seguro! No conozco a ese animal. 🤔"

    # Renderizamos la plantilla, pasándole nuestra adivinanza.
    return render_template('animales.html', animal_adivinado=animal_adivinado)

@app.route('/pedidos-comida', methods=['GET', 'POST'])
def pedidos_comida():
    confirmacion_pedido = None

    if request.method == 'POST':
        pedido = request.form['pedido_usuario']
        pedido_lower = pedido.lower()

        # --- Lógica de Extracción de Entidades ---
        # Buscamos la entidad "comida" en el texto.
        if 'pizza' in pedido_lower:
            # Si encontramos la entidad, creamos una respuesta específica.
            confirmacion_pedido = "¡Pedido recibido! Tu pizza 🍕 está en preparación."
        elif 'hamburguesa' in pedido_lower:
            confirmacion_pedido = "¡Pedido recibido! Tu hamburguesa 🍔 está en preparación."
        elif 'pasta' in pedido_lower:
            confirmacion_pedido = "¡Pedido recibido! Tu plato de pasta 🍝 está en preparación."
        elif 'ensalada' in pedido_lower:
            confirmacion_pedido = "¡Pedido recibido! Tu ensalada 🥗 está en preparación."
        else:
            # Si no encontramos ninguna entidad conocida, damos una respuesta genérica.
            confirmacion_pedido = "Lo siento, no tenemos eso en el menú. Por favor, intenta con pizza, hamburguesa, pasta o ensalada."

    # Renderizamos la plantilla, pasándole la confirmación.
    return render_template('pedidos.html', confirmacion_pedido=confirmacion_pedido)

@app.route('/recordatorios', methods=['GET', 'POST'])
def recordatorios():
    confirmacion_recordatorio = None

    if request.method == 'POST':
        frase = request.form['frase_recordatorio']
        frase_lower = frase.lower()

        # --- Lógica de Extracción de Entidades con split() ---
        # Verificamos que las palabras clave existan para evitar errores.
        # Usamos ' a las ' con espacios para ser más precisos.
        if 'recuérdame' in frase_lower and ' a las ' in frase_lower:
            try:
                # Dividimos la frase en dos partes usando ' a las ' como separador.
                partes = frase_lower.split(' a las ')
                
                # La primera parte contiene la acción. Le quitamos "recuérdame" y espacios extra.
                accion = partes[0].replace('recuérdame', '').strip()
                
                # La segunda parte es la hora. Le quitamos espacios extra.
                hora = partes[1].strip()

                # Creamos el mensaje de confirmación.
                confirmacion_recordatorio = f"✅ ¡Entendido! He guardado un recordatorio para '{accion}' a las {hora}."
            except IndexError:
                # Esto es por si algo sale mal con el split.
                confirmacion_recordatorio = "❌ Hubo un problema al entender tu frase. Inténtalo de nuevo."
        else:
            # Si el formato no es el esperado.
            confirmacion_recordatorio = "❌ No entendí el formato. Por favor, usa una frase como 'Recuérdame [acción] a las [hora]'."

    # Renderizamos la plantilla, pasándole la confirmación.
    return render_template('recordatorios.html', confirmacion_recordatorio=confirmacion_recordatorio)

if __name__ == '__main__':
    app.run(debug=True)