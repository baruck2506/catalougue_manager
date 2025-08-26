from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Float, nullable=False)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(100), default="Pendente")

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, default=1)

    pedido = db.relationship("Pedido", backref="itens")
    produto = db.relationship("Produto")
