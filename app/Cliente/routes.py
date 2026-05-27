from flask import render_template,redirect, url_for,request,Blueprint
from app.__init__ import db
from app.Cliente.models import Cliente


bp_clientes = Blueprint('bp_clientes',__name__,template_folder='templates')

@bp_clientes.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('/clientes/index.html',clientes=clientes)

@bp_clientes.route("/create",methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('/clientes/create.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')

        cliente = Cliente(nombre=nombre,telefono=telefono)
        db.session.add(cliente)
        db.session.commit()
        
        return redirect(url_for('bp_clientes.index'))
    
@bp_clientes.route("/update/<int:id>",methods={'GET','POST'})
def update(id):
    cliente = Cliente.query.get(id)
    if request.method == 'GET':
        return render_template('/clientes/update.html',cliente=cliente)
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')

        cliente.nombre = nombre
        cliente.telefono = telefono        
        db.session.commit()

        return redirect(url_for('bp_clientes.index'))

@bp_clientes.route("/delete/<int:id>")
def delete(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('bp_clientes.index'))