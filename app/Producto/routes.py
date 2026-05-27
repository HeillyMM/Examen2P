from flask import render_template,redirect, url_for,request,Blueprint
from app.__init__ import db
from app.Producto.models import Producto


bp_productos = Blueprint('bp_productos',__name__,template_folder='templates')

@bp_productos.route('/')
def index():
    productos = Producto.query.all()
    return render_template('/productos/index.html',productos=productos)

@bp_productos.route("/create",methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('/productos/create.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        stock = request.form.get('stock')

        producto = Producto(nombre=nombre,precio=precio,stock=stock)
        db.session.add(producto)
        db.session.commit()
        
        return redirect(url_for('bp_productos.index'))
    
@bp_productos.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    producto = Producto.query.get(id)
    if request.method == 'GET':
        return render_template('/productos/update.html',producto=producto)
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        stock = request.form.get('stock')

        producto.nombre = nombre
        producto.precio = precio        
        producto.stock = stock        
        db.session.commit()

        return redirect(url_for('bp_productos.index'))

@bp_productos.route("/delete/<int:id>")
def delete(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('bp_productos.index'))