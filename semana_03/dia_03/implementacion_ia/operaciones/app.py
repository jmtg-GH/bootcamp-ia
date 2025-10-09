import re
from flask import Flask, render_template, request
app = Flask(__name__)
def parse_nl(text):
    #extraer numeros que acepte enteros y decimales negativos
    nums = re.findall(r'-?\d+(?:\.\d+)?', text)
    nums = [float(n) for n in nums]
    t = text.lower()
    if any(k in t for k in ["sum", "suma", "sumar", "más", "mas","+", "adicione", "adición"] ):
        op="suma"
    elif any(k in t for k in ["resta", "restar", "res", "diferencia", "menos", "sustraer", "sustracción", "-"]):
        op="resta"
    elif any(k in t for k in ["mult", "multiplique", "multiplica", "por", "producto", "multiplicación", "*"]):
        op="producto"
    elif any(k in t for k in ["div", "división", "dividir", "entre", "divide","/"]):
        op="division"
    else:
        op = None
    return op, nums
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        text = request.form.get("nl_input", "").strip()
        op, nums = parse_nl(text)
        if op is None or len(nums) < 2:
            resultado ="No se puede entender la operación. Escribe por ejemplo: sumar 2 y 3"
        else:
            a, b = nums[0], nums[1]
            if op =="suma":
                resultado = a + b
            elif op == "resta":
                resultado = a - b
            elif op == "producto":
                resultado = a * b
            elif op == "division":
                resultado = "Error: división por cero" if b == 0 else a / b 
    return render_template("operaciones.html", resultado = resultado)
if __name__ == "__main__":
    app.run(debug=True)