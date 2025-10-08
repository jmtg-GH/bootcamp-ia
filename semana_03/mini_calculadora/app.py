from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def suma():
    resultado = None
    if request.method == "POST":
        try:
            n1 = float(request.form["num1"])
            n2 = float(request.form["num2"])
            operacion = request.form["operacion"]

            match operacion:
                case "suma": resultado = n1 + n2
                case "resta": resultado = n1 - n2
                case "multiplicacion": resultado = n1 * n2
                case "division": resultado = n1/n2 if n2 != 0 else "Error: división entre cero"
        except:
            resultado = "Error: ingresa números válidos"
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)