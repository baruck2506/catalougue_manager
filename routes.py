from flask import render_template, request, redirect, url_for, flash
from models import db, Produto, Pedido, ItemPedido, Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

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
    @login_required
    def listar_pedidos():
        pedidos = Pedido.query.all()
        return render_template("pedidos.html", pedidos=pedidos)

    # Atualizar status de um pedido
    @app.route("/atualizar_status/<int:id>", methods=["POST"])
    @login_required
    def atualizar_status(id):
        pedido = Pedido.query.get_or_404(id)
        novo_status = request.form["status"]
        pedido.status = novo_status
        db.session.commit()
        return redirect(url_for("listar_pedidos"))
    
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            nome = request.form["nome"]
            email = request.form["email"]
            senha = generate_password_hash(request.form["senha"])

            if Usuario.query.filter_by(email=email).first():
                flash("Email já cadastrado")
                return redirect(url_for("register"))
            
            novo_usuario = Usuario(nome=nome, email=email, senha=senha)
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Cadastro realizado com sucesso!")
            return redirect(url_for("login"))
        return render_template("register.html")
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            senha = request.form["senha"]
            usuario = Usuario.query.filter_by(email=email).first()

            if usuario and check_password_hash(usuario.senha, senha):
                login_user(usuario)
                flash("Login realizado com sucesso!")
                return redirect(url_for("listar_pedidos"))  # corrigido
            else:
                flash("Email ou senha incorretos")
        
        return render_template("login.html")
        
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logout realizado!")
        return redirect(url_for("login"))
