from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__,template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd_equipo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app,db)
    
    # Blueprints
    from app.Cliente.routes import bp_clientes
    from app.Pedido.routes import bp_pedidos
    from app.Producto.routes import bp_productos
    
    app.register_blueprint(bp_clientes,url_prefix="/clientes")
    app.register_blueprint(bp_pedidos,url_prefix="/pedidos")
    app.register_blueprint(bp_productos,url_prefix="/")

    return app
    