from flask import render_template, request, redirect, url_for
from models import db, Produto

def criar_rotas(app):
    # READ - lista todos os produtos
    @app.route("/")
    def index():
        produtos = Produto.query.all()
        return render_template("index.html", produtos=produtos)

    # CREATE - adicionar novo produto
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

    # UPDATE - editar produto
    @app.route("/editar/<int:id>", methods=["GET", "POST"])
    def editar(id):
        produto = Produto.query.get_or_404(id)
        if request.method == "POST":
            produto.nome = request.form["nome"]
            produto.preco = float(request.form["preco"])
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("editar.html", produto=produto)

    # DELETE - remover produto
    @app.route("/deletar/<int:id>")
    def deletar(id):
        produto = Produto.query.get_or_404(id)
        db.session.delete(produto)
        db.session.commit()
        return redirect(url_for("index"))
