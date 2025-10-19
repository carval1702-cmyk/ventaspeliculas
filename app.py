from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)

# Crear tabla al iniciar
db.create_table()

@app.route("/")
def index():
    peliculas = db.obtener_peliculas()
    return render_template("index.html", peliculas=peliculas)

@app.route("/agregar", methods=["POST"])
def agregar():
    titulo = request.form["titulo"]
    genero = request.form["genero"]
    precio = request.form["precio"]
    db.agregar_pelicula(titulo, genero, precio)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)


