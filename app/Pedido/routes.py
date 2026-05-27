from flask import render_template,redirect, url_for,request,Blueprint
from app.__init__ import db
from app.Pedido.models import Pedido
from app.Cliente.models import Cliente
from app.Producto.models import Producto


bp_pedidos = Blueprint('bp_pedidos',__name__,template_folder='templates')

@bp_pedidos.route("/")
def index():
    pedidos = Pedido.query.all()
    return render_template('/pedidos/index.html',pedidos=pedidos)

@bp_pedidos.route("/create",methods=['GET','POST'])
def create():
    if request.method == 'GET':
        clientes = Cliente.query.all()
        productos = Producto.query.all()
        return render_template('/pedidos/create.html',clientes=clientes,productos=productos)
    elif request.method == 'POST':
        fecha = request.form.get('fecha')
        monto = request.form.get('monto')
        producto_id = request.form.get('producto_id')
        cliente_id = request.form.get('cliente_id')

        pedido = Pedido(fecha=fecha,monto=monto,producto_id=producto_id,cliente_id=cliente_id)
        db.session.add(pedido)
        db.session.commit()
        
        return redirect(url_for('bp_pedidos.index'))
    
@bp_pedidos.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    pedido = Pedido.query.get(id)
    if request.method == 'GET':
        clientes = Cliente.query.all()
        productos = Producto.query.all()
        return render_template('/pedidos/create.html',clientes=clientes,productos=productos,pedido=pedido)
    elif request.method == 'POST':
        fecha = request.form.get('fecha')
        monto = request.form.get('monto')
        producto_id = request.form.get('producto_id')
        cliente_id = request.form.get('cliente_id')

        pedido.fecha = fecha
        pedido.monto = monto
        pedido.producto_id = producto_id
        pedido.cliente_id = cliente_id

        db.session.add(pedido)
        db.session.commit()
        
        return redirect(url_for('bp_pedidos.index'))

@bp_pedidos.route("/delete/<int:id>")
def delete(id):
    pedido = Pedido.query.get(id)
    db.session.delete(pedido)
    db.session.commit()
    return redirect(url_for('bp_pedidos.index'))