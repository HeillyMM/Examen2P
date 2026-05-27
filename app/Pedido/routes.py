from flask import render_template, redirect, url_for, request, Blueprint, flash
from app.__init__ import db
from app.Pedido.models import Pedido
from app.Cliente.models import Cliente
from app.Producto.models import Producto
from datetime import datetime

bp_pedidos = Blueprint('bp_pedidos', __name__, template_folder='templates')

@bp_pedidos.route("/")
def index():
    pedidos = Pedido.query.all()
    return render_template('/pedidos/index.html', pedidos=pedidos)

@bp_pedidos.route("/create", methods=['GET', 'POST'])
def create():

    if request.method == 'GET':
        clientes = Cliente.query.all()
        productos = Producto.query.filter(Producto.stock > 0).all()

        return render_template('/pedidos/create.html', clientes=clientes, productos=productos)

    elif request.method == 'POST':

        fecha_texto = request.form['fecha']
        fecha_convertida = datetime.strptime(fecha_texto, '%Y-%m-%d').date()

        monto = int(request.form.get('monto'))
        producto_id = request.form.get('producto_id')
        cliente_id = request.form.get('cliente_id')

        producto = Producto.query.get_or_404(producto_id)

        if producto.stock < monto:
            flash(f"No hay suficiente stock de {producto.nombre}. Stock actual: {producto.stock}", "danger")

            clientes = Cliente.query.all()
            productos = Producto.query.filter(Producto.stock > 0).all()

            return render_template('/pedidos/create.html', clientes=clientes, productos=productos)

        producto.stock -= monto

        pedido = Pedido(fecha=fecha_convertida,monto=monto,producto_id=producto_id,cliente_id=cliente_id)

        db.session.add(producto)
        db.session.add(pedido)
        db.session.commit()

        return redirect(url_for('bp_pedidos.index'))

@bp_pedidos.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):

    pedido = Pedido.query.get_or_404(id)

    if request.method == 'GET':
        clientes = Cliente.query.all()
        productos = Producto.query.all()
        return render_template('/pedidos/update.html', clientes=clientes, productos=productos, pedido=pedido)

    elif request.method == 'POST':

        fecha_texto = request.form['fecha']
        fecha_convertida = datetime.strptime(fecha_texto, '%Y-%m-%d').date()

        nuevo_producto_id = request.form.get('producto_id')
        nueva_monto = int(request.form.get('monto'))

        producto_viejo = Producto.query.get_or_404(pedido.producto_id)
        producto_viejo.stock += pedido.monto

        producto_nuevo = Producto.query.get_or_404(nuevo_producto_id)

        if producto_nuevo.stock < nueva_monto:

            producto_viejo.stock -= pedido.monto

            flash(f"No hay suficiente stock de {producto_nuevo.nombre}. Stock actual: {producto_nuevo.stock}", "danger")

            clientes = Cliente.query.all()
            productos = Producto.query.all()

            return render_template('/pedidos/update.html', clientes=clientes, productos=productos, pedido=pedido)

        producto_nuevo.stock -= nueva_monto

        pedido.fecha = fecha_convertida
        pedido.monto = request.form.get('monto')
        pedido.producto_id = nuevo_producto_id
        pedido.cliente_id = request.form.get('cliente_id')
        pedido.monto = nueva_monto

        db.session.commit()

        return redirect(url_for('bp_pedidos.index'))

@bp_pedidos.route("/delete/<int:id>")
def delete(id):

    pedido = Pedido.query.get_or_404(id)
    producto = Producto.query.get_or_404(pedido.producto_id)

    producto.stock += pedido.monto

    db.session.delete(pedido)
    db.session.commit()

    return redirect(url_for('bp_pedidos.index'))