from flask import Flask, render_template, request, redirect, url_for
import db
import time

app = Flask(__name__)


db.create_table()


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        values['q'] = int(time.time())
    return url_for(endpoint, **values)


carrito = []



@app.route("/")
def index():
    peliculas = db.obtener_peliculas()
    return render_template("index.html", peliculas=peliculas)


@app.route("/agregar", methods=["POST"])
def agregar():
    titulo = request.form["titulo"]
    genero = request.form["genero"]
    precio = request.form["precio"]
    poster = request.form["poster"]

    db.agregar_pelicula(titulo, genero, precio, poster)
    return redirect("/")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    pelicula = db.obtener_pelicula(id)
    if request.method == "POST":
        titulo = request.form["titulo"]
        genero = request.form["genero"]
        precio = request.form["precio"]
        poster = request.form["poster"]
        db.actualizar_pelicula(id, titulo, genero, precio, poster)
        return redirect("/")
    return render_template("editar.html", pelicula=pelicula)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    db.eliminar_pelicula(id)
    return redirect("/")


@app.route("/carrito")
def carrito_view():
    total = sum(float(p["precio"]) for p in carrito)
    return render_template("carrito.html", carrito=carrito, total=total)


@app.route("/agregar_carrito/<int:id>")
def agregar_carrito(id):
    pelicula = db.obtener_pelicula(id)

    if pelicula:
        carrito.append({
            "id": pelicula["id"],
            "titulo": pelicula["titulo"],
            "genero": pelicula["genero"],
            "precio": pelicula["precio"],
            "poster": pelicula["poster"]
        })

    return redirect("/carrito")


@app.route("/vaciar_carrito")
def vaciar_carrito():
    carrito.clear()
    return redirect("/carrito")


@app.route("/boleta")
def boleta():
    if not carrito:
        return redirect("/carrito")

    total = sum(float(p["precio"]) for p in carrito)
    return render_template("boleta.html", carrito=carrito, total=total)



if __name__ == "__main__":
    app.run(debug=True)
