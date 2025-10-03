from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def suma():
    resultado = None
    if request.method == "POST":
        try:
            n1 = float(request.form["num1"])
            n2 = float(request.form["num2"])
            resultado = n1 + n2
        except:
            resultado = "Error: ingresa números válidos"
    return render_template("suma.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)