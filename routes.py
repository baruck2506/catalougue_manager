from flask import Flask, render_template, request, redirect, url_for
from models import db, Produto

def criar_rotas(app):
    @app.route("/")
    def index():
        produtos = Produto.query.all()
        return render_template("index.html", produtos=produtos)
    
    @app.route("/adicionar", methods=["GET", "POST"])
    def adicionar():
        if request.method == "POST":
            nome = request.form["nome"]
            preco = float(request.form["preco"])
            p = Produto(nome=nome, preco=preco)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("adicionar.html")
