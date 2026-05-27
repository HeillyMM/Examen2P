from app.__init__ import db

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(200),nullable=False)
    precio = db.Column(db.Float,nullable=False)
    stock = db.Column(db.Integer,nullable=False)

    pedidos = db.relationship('Pedido',back_populates='producto',cascade='all,delete-orphan')

    def __repr__(self):
        return f"{{'id':'{self.nombre}','nombre':'{self.nombre}','precio':'{self.precio}','stock':'{self.stock}'}}"