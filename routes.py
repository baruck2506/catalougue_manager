from flask import render_template, request, redirect, url_for
from models import db, Produto, Pedido, ItemPedido

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

    @app.route("/pedido", methods=["GET", "POST"])
    def pedido():
        produtos = Produto.query.all()
        if request.method == "POST":
            nome_cliente = request.form["cliente"]
            pedido = Pedido(cliente_nome=nome_cliente)
            db.session.add(pedido)
            db.session.commit()

            for p in produtos:
                qnt = request.form.get(f"qnt_{p.id}", 0)
                if qnt and int(qnt) > 0:
                    item = ItemPedido(pedido_id=pedido.id, produto_id=p.id, quantidade=int(qnt))
                    db.session.add(item)
            db.session.commit()
            return redirect(url_for("confirmacao", pedido_id=pedido.id))
        return render_template("pedido.html", produtos=produtos)
    
    @app.route("/confirmacao/<int:pedido_id>")
    def confirmacao(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        return render_template("confirmacao.html", pedido=pedido)
    
    @app.route("/pedidos")
    def listar_pedidos():
        pedidos = Pedido.query.all()
        return render_template("pedidos.html", pedidos=pedidos)

    # Atualizar status de um pedido
    @app.route("/atualizar_status/<int:id>", methods=["POST"])
    def atualizar_status(id):
        pedido = Pedido.query.get_or_404(id)
        novo_status = request.form["status"]
        pedido.status = novo_status
        db.session.commit()
        return redirect(url_for("listar_pedidos"))