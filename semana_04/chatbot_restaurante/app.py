from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import re
import os

app = Flask(__name__)

# Archivo donde se guardan los pedidos
PEDIDOS_FILE = "pedidos.json"

# --------------------------
# 🧾 Menú con imágenes
# --------------------------
MENU = {
    "hamburguesa": {
        "precio": 12000,
        "imagen": "https://cdn.pixabay.com/photo/2016/03/05/19/02/hamburger-1238246_1280.jpg"
    },
    "perro": {
        "precio": 10000,
        "imagen": "https://cdn.pixabay.com/photo/2014/10/19/20/59/hot-dog-494706_1280.jpg"
    },
    "salchipapa": {
        "precio": 15000,
        "imagen": "https://laparisienne.com.co/cdn/shop/articles/SALCHIPAPA_LA_PARISIENNE_CUADRADA_480x480@2x.jpg?v=1682626308"
    },
    "gaseosa": {
        "precio": 4000,
        "imagen": "https://multidulces.com.co/wp-content/uploads/2024/01/postobon-250.jpg"
    },
    "malteada": {
        "precio": 7000,
        "imagen": "https://i.blogs.es/c6f09d/como-hacer-malteada-chocolate-cremosa-receta-facil-mundo/840_560.jpg"
    }
}

# --------------------------
# 🧠 IA simple: interpretar pedidos (mejorada)
# --------------------------
def parse_pedido(texto):
    texto = texto.lower()
    pedido = []
    for producto, datos in MENU.items():
        # reconocer plurales agregando s opcional y usar word boundaries
        prod_escaped = re.escape(producto)
        # si el nombre aparece (incluso en plural)
        if re.search(rf'\b{prod_escaped}s?\b', texto):
            # buscar cantidad antes del producto: "2 hamburguesas"
            m = re.search(rf'(\d+)\s*(?:{prod_escaped}s?\b)', texto)
            # o buscar cantidad después: "hamburguesa 2"
            if not m:
                m = re.search(rf'\b(?:{prod_escaped}s?)\b\s*(\d+)', texto)
            cantidad = int(m.group(1)) if m else 1
            pedido.append({
                "producto": producto,
                "cantidad": cantidad,
                "subtotal": datos["precio"] * cantidad
            })
    return pedido

# --------------------------
# Helper: comprobar si un texto parece una dirección
# --------------------------
def es_direccion(texto):
    texto = texto.lower()
    # palabras comunes y abreviaturas usadas en direcciones en español/colombia
    palabras_calle = r'\b(calle|cll|cl|cra|carrera|av|avenida|transversal|tv|via)\b'
    # si contiene una de las palabras de calle o contiene '#' o 'no' seguido de número
    if re.search(palabras_calle, texto):
        return True
    if '#' in texto:
        return True
    # "no 12", "número 12", o simplemente una combinación de número y palabra calle
    if re.search(r'\b(no\.?|numero|nº)\b.*\d+', texto):
        return True
    # fallback: si el texto tiene un número y al menos una palabra corta (ej: "5 10-20")
    if re.search(r'\d{1,4}', texto) and len(texto.split()) <= 6 and any(c.isalpha() for c in texto):
        # esto ayuda cuando el usuario escribe "Cll 5 # 10-20" o "123 Avenida Siempre Viva"
        return True
    return False

# --------------------------
# 🏠 Página principal
# --------------------------
@app.route("/")
def index():
    return render_template("index.html", menu=MENU)

# --------------------------
# 🤖 Endpoint del chatbot
# --------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    mensaje = (data.get("mensaje") or "").strip().lower()
    pedido_actual = data.get("pedido", []) or []
    direccion_actual = data.get("direccion", "") or ""

    # 1️⃣ Detectar productos (si el texto contiene nombres del menú)
    # Usamos parse_pedido para obtener items
    posibles_pedido = parse_pedido(mensaje)
    if posibles_pedido:
        pedido_actual = posibles_pedido
        total = sum(item["subtotal"] for item in pedido_actual)
        respuesta = (
            f"Entendido 😋 Tu pedido es: "
            + ", ".join(f"{p['cantidad']} {p['producto']}" for p in pedido_actual)
            + f". Total: ${total}. ¿Cuál es tu dirección?"
        )
        return jsonify({"respuesta": respuesta, "fase": "direccion", "pedido": pedido_actual})

    # 2️⃣ Detectar dirección
    if es_direccion(mensaje):
        direccion_actual = mensaje
        respuesta = "Perfecto 🏠. ¿Cómo deseas pagar? (efectivo, tarjeta o transferencia)"
        return jsonify({
            "respuesta": respuesta,
            "fase": "pago",
            "pedido": pedido_actual,
            "direccion": direccion_actual
        })

    # 3️⃣ Detectar forma de pago y guardar pedido
    if any(palabra in mensaje for palabra in ["efectivo", "tarjeta", "transferencia"]):
        # determinar forma de pago exacta
        if "efectivo" in mensaje:
            forma_pago = "efectivo"
        elif "tarjeta" in mensaje:
            forma_pago = "tarjeta"
        else:
            forma_pago = "transferencia"

        nuevo_pedido = {
            "pedido": pedido_actual,
            "direccion": direccion_actual if direccion_actual else "Por definir",
            "pago": forma_pago,
            "estado": "pendiente"
        }

        # Crear archivo si no existe
        if not os.path.exists(PEDIDOS_FILE):
            with open(PEDIDOS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        # Leer y actualizar pedidos (manejo robusto de JSON)
        with open(PEDIDOS_FILE, "r+", encoding="utf-8") as f:
            try:
                pedidos = json.load(f)
                if not isinstance(pedidos, list):
                    pedidos = []
            except json.JSONDecodeError:
                pedidos = []
            pedidos.append(nuevo_pedido)
            f.seek(0)
            json.dump(pedidos, f, ensure_ascii=False, indent=4)
            f.truncate()

        respuesta = (
            "Gracias 🧾 Tu pedido fue registrado con éxito.\n"
            "🕒 Tu pedido está en proceso y pronto llegará a tu dirección.\n"
            "💖 ¡Gracias por preferir Restaurante IA! ¡Buen provecho!"
        )
        return jsonify({"respuesta": respuesta, "fase": "final"})

    # 4️⃣ Mensaje por defecto
    respuesta = (
        "Hola 👋 Soy tu asistente virtual. Dime qué deseas pedir "
        "(por ejemplo: '2 hamburguesas y una gaseosa')."
    )
    return jsonify({"respuesta": respuesta, "fase": "inicio"})

# --------------------------
# 📋 Ver pedidos
# --------------------------
@app.route("/pedidos")
def ver_pedidos():
    pedidos = []
    if os.path.exists(PEDIDOS_FILE):
        with open(PEDIDOS_FILE, "r", encoding="utf-8") as f:
            try:
                pedidos = json.load(f)
                if not isinstance(pedidos, list):
                    pedidos = []
            except json.JSONDecodeError:
                pedidos = []
    return render_template("pedidos.html", pedidos=pedidos)

# --------------------------
# 🔄 Actualizar estado
# --------------------------
@app.route("/actualizar_estado", methods=["POST"])
def actualizar_estado():
    try:
        index = int(request.form.get("index"))
    except (TypeError, ValueError):
        return redirect(url_for("ver_pedidos"))

    nuevo_estado = request.form.get("estado", "pendiente")
    pedidos = []
    if os.path.exists(PEDIDOS_FILE):
        with open(PEDIDOS_FILE, "r+", encoding="utf-8") as f:
            try:
                pedidos = json.load(f)
                if not isinstance(pedidos, list):
                    pedidos = []
            except json.JSONDecodeError:
                pedidos = []
            if 0 <= index < len(pedidos):
                pedidos[index]["estado"] = nuevo_estado
                f.seek(0)
                json.dump(pedidos, f, ensure_ascii=False, indent=4)
                f.truncate()
    return redirect(url_for("ver_pedidos"))

# --------------------------
if __name__ == "__main__":
    # host y port opcionales — ajusta según necesites
    app.run(debug=True, host="0.0.0.0", port=5000)