from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --------------------------
# ✨ Filtro de template personalizado para formatear números
# --------------------------
@app.template_filter('number_format')
def number_format_filter(value):
    """Formatea un número como 12.000"""
    return f"{value:,.0f}".replace(",", ".")

# Archivo donde se guardan los pedidos
PEDIDOS_FILE = "pedidos.json"

# ... (el resto del código es idéntico al anterior, pero incluyo la sección relevante corregida) ...

MENU = {
    "hamburguesa": {"precio": 12000, "imagen": "https://www.unileverfoodsolutions.com.co/dam/global-ufs/mcos/NOLA/calcmenu/recipes/col-recipies/fruco-tomate-cocineros/HAMBURGUESA%201200x709.png"},
    "perro": {"precio": 10000, "imagen": "https://caracol.com.co/resizer/v2/G3S35CK2XJEY3DEDOIIJIDDY2A.jpg?auth=06f3d9bc825787abfca93a32793786cbee55096b96abdf595b7a1e70df8a2e97&width=768&height=576&quality=70&smart=true"},
    "salchipapa": {"precio": 15000, "imagen": "https://laparisienne.com.co/cdn/shop/articles/SALCHIPAPA_LA_PARISIENNE_CUADRADA.jpg?v=1682626308"},
    "gaseosa": {"precio": 4000, "imagen": "https://multidulces.com.co/wp-content/uploads/2024/01/postobon-250.jpg"},
    "malteada": {"precio": 7000, "imagen": "https://www.saborusa.com/wp-content/uploads/2020/12/Captura-de-pantalla-101.png"}
}

# ... (funciones leer_pedidos, guardar_pedidos, parse_pedido, es_direccion) ...
def leer_pedidos():
    if not os.path.exists(PEDIDOS_FILE): return []
    with open(PEDIDOS_FILE, "r", encoding="utf-8") as f:
        try:
            pedidos = json.load(f)
            return pedidos if isinstance(pedidos, list) else []
        except json.JSONDecodeError: return []

def guardar_pedidos(pedidos):
    with open(PEDIDOS_FILE, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=4)

def parse_pedido(texto):
    texto = texto.lower()
    pedido = []
    for producto, datos in MENU.items():
        prod_escaped = re.escape(producto)
        if re.search(rf'\b{prod_escaped}s?\b', texto):
            m = re.search(rf'(\d+)\s*(?:{prod_escaped}s?\b)', texto)
            if not m: m = re.search(rf'\b(?:{prod_escaped}s?)\b\s*(\d+)', texto)
            cantidad = int(m.group(1)) if m else 1
            pedido.append({"producto": producto, "cantidad": cantidad, "subtotal": datos["precio"] * cantidad})
    return pedido

def es_direccion(texto):
    texto = texto.lower()
    palabras_calle = r'\b(calle|cll|cl|cra|carrera|av|avenida|transversal|tv|via)\b'
    if re.search(palabras_calle, texto) or '#' in texto: return True
    if re.search(r'\b(no\.?|numero|nº)\b.*\d+', texto): return True
    if re.search(r'\d{1,4}', texto) and len(texto.split()) <= 6 and any(c.isalpha() for c in texto): return True
    return False

@app.route("/")
def index():
    return render_template("index.html", menu=MENU)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    mensaje = (data.get("mensaje") or "").strip().lower()

    if 'fase' not in session:
        session['fase'] = 'inicio'
        session['pedido'] = []
        session['direccion'] = ''

    if session['fase'] == 'inicio':
        posibles_pedido = parse_pedido(mensaje)
        if posibles_pedido:
            session['pedido'] = posibles_pedido
            session['fase'] = 'direccion'
            total = sum(item["subtotal"] for item in session['pedido'])
            # CORRECCIÓN APLICADA AQUÍ TAMBIÉN
            total_formateado = number_format_filter(total)
            respuesta = (
                f"Entendido 😋 Tu pedido es: "
                + ", ".join(f"{p['cantidad']} {p['producto']}" for p in session['pedido'])
                + f". Total: ${total_formateado}. ¿Cuál es tu dirección?"
            )
            return jsonify({"respuesta": respuesta, "fase": session['fase']})

    if session['fase'] == 'direccion':
        if es_direccion(mensaje):
            session['direccion'] = mensaje.title()
            session['fase'] = 'pago'
            respuesta = "Perfecto 🏠. ¿Cómo deseas pagar? (efectivo, tarjeta o transferencia)"
            return jsonify({"respuesta": respuesta, "fase": session['fase']})

    if session['fase'] == 'pago':
        if any(palabra in mensaje for palabra in ["efectivo", "tarjeta", "transferencia"]):
            forma_pago = "transferencia"
            if "efectivo" in mensaje: forma_pago = "efectivo"
            elif "tarjeta" in mensaje: forma_pago = "tarjeta"
            nuevo_pedido = {"pedido": session['pedido'], "direccion": session['direccion'], "pago": forma_pago, "estado": "pendiente"}
            pedidos = leer_pedidos()
            pedidos.append(nuevo_pedido)
            guardar_pedidos(pedidos)
            session.clear()
            respuesta = (
                "Gracias 🧾 Tu pedido fue registrado con éxito.\n"
                "🕒 Tu pedido está en proceso y pronto llegará a tu dirección.\n"
                "💖 ¡Gracias por preferir Restaurante IA! ¡Buen provecho!"
            )
            return jsonify({"respuesta": respuesta, "fase": "final"})

    if session['fase'] == 'inicio':
        respuesta = "Hola 👋 Soy tu asistente virtual. Dime qué deseas pedir (ej: '2 hamburguesas y una gaseosa')."
    elif session['fase'] == 'direccion':
        respuesta = "No entendí eso como una dirección. Por favor, intenta de nuevo usando palabras como 'calle', 'carrera', o el símbolo '#'."
    elif session['fase'] == 'pago':
        respuesta = "No reconozco ese método de pago. Por favor, elige entre 'efectivo', 'tarjeta' o 'transferencia'."
    else:
        respuesta = "Puedes iniciar un nuevo pedido diciendo qué productos quieres."
    return jsonify({"respuesta": respuesta, "fase": session.get('fase', 'inicio')})

@app.route("/pedidos")
def ver_pedidos():
    pedidos = leer_pedidos()
    return render_template("pedidos.html", pedidos=pedidos)

@app.route("/actualizar_estado", methods=["POST"])
def actualizar_estado():
    try:
        index = int(request.form.get("index"))
        nuevo_estado = request.form.get("estado", "pendiente")
    except (TypeError, ValueError):
        return redirect(url_for("ver_pedidos"))
    pedidos = leer_pedidos()
    if 0 <= index < len(pedidos):
        pedidos[index]["estado"] = nuevo_estado
        guardar_pedidos(pedidos)
    return redirect(url_for("ver_pedidos"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)