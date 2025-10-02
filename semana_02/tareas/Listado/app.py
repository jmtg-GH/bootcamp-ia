from flask import Flask, render_template, request, redirect
app = Flask(__name__)
tareas = []
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        tarea = request.form["tarea"]
        tareas.append(tarea)
        return redirect("/")
    return render_template("index.html", tareas=tareas)

if __name__ == "__main__":
    app.run(debug=True)