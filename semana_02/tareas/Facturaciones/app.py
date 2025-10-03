from flask import Flask, render_template, request, redirect
app = Flask(__name__)
@app.route("/", methods = ["GET", "POST"])
def factura():
    datos = None
    if request.method == "POST":
        try:
            nombre = request.form["nombre"]
            correo = request.form["correo"]
            nitId = request.form["nitId"]
            fact = request.form["fact"]
            prod = request.form["prod"]
            precio = float(request.form["precio"])
            unidades = int(request.form["unidades"])
            total = precio * unidades

            datos = {
                "nombre": nombre,
                "correo": correo,
                "nitId": nitId,
                "fact": fact,
                "prod": prod,
                "precio": precio,
                "unidades": unidades,
                "total": total
            }
        except Exception as e:
            datos = {"error": f"Ha ocurrido un error: {e}"}
        
    return render_template("index.html", datos=datos)

if __name__ == "__main__":
    app.run(debug=True)