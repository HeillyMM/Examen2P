from app.__init__ import db

class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer,primary_key=True)
    fecha = db.Column(db.Date,nullable=False)
    monto = db.Column(db.Integer,nullable=False)
    producto_id = db.Column(db.Integer,db.ForeignKey('productos.id'),nullable=False)
    cliente_id = db.Column(db.Integer,db.ForeignKey('clientes.id'),nullable=False)

    cliente = db.relationship('Cliente',back_populates='pedidos')
    producto = db.relationship('Producto',back_populates='pedidos')

    def __repr__(self):
        return f"{{'id':'{self.id}','fecha':{self.fecha},'monto':'{self.monto}','producto_id':'{self.producto_id}','cliente_id':'{self.cliente_id}'}}"