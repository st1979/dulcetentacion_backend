"""La línea de comando:
pip install Flask SQLAlchemy mysql-connector-python 

se utiliza para instalar
tres paquetes en tu entorno de Python. 
Aquí está una breve descripción de cada uno de ellos:

Flask: Flask es un framework ligero de desarrollo
web para Python. Facilita la creación de aplicaciones
web de manera rápida y sencilla. Con Flask, puedes
definir rutas, gestionar solicitudes HTTP, y construir
aplicaciones web de manera eficiente.

SQLAlchemy: SQLAlchemy es una biblioteca de
SQL en Python que proporciona un conjunto
de herramientas de alto nivel para interactuar
con bases de datos relacionales. Facilita la
creación, el acceso y la manipulación de bases
de datos utilizando objetos Python en lugar de escribir directamente SQL.

mysql-connector-python: Este paquete es un conector oficial
de MySQL para Python. Permite a tu aplicación Python conectarse y 
comunicarse con una base de datos MySQL. En el contexto de Flask
y SQLAlchemy, se utiliza para establecer la conexión entre tu 
aplicación y la base de datos MySQL ."""

# 3. Importar las herramientas
# Acceder a las herramientas para crear la app web

import json

from flask import Flask, request, jsonify

# Para manipular la DB
from flask_sqlalchemy import SQLAlchemy 

from sqlalchemy import desc

# Módulo cors es para que me permita acceder desde el frontend al backend
from flask_cors import CORS

# 4. Crear la app
app = Flask(__name__)

# Habilitar a la app para recibir peticiones
# CORS(app, resources={r"/registro": {"origins": "http://127.0.0.1:5500"}})

CORS(app)
CORS(app, resources={r"/registro": {"origins": "http://127.0.0.1:5500"}})  # Permitir acceso desde cualquier origen para la ruta /registro


# 5. Configurar a la app la DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://usuario:contraseña@localhost:3306/nombre_de_la_base_de_datos'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost:3306/db_23528'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/bd_dulcetentacion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 6. Crear un objeto db, para informar a la app que se trabajará con sqlalchemy
db = SQLAlchemy(app)

# 7. Definir la tabla 
# class Producto(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(50))
#     precio=db.Column(db.Integer)
#     stock=db.Column(db.Integer)
#     imagen=db.Column(db.String(400))

#     def __init__(self,nombre,precio,stock,imagen):   #crea el  constructor de la clase
#         self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
#         self.precio=precio
#         self.stock=stock
#         self.imagen=imagen
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    apellido=db.Column(db.String(90))
    telefono=db.Column(db.Integer)
    fechaEvento=db.Column(db.Date)
    sabor=db.Column(db.String(50))
    tamano=db.Column(db.Integer)
    cobertura=db.Column(db.String(60))
    # decoracion=db.Column(db.JSON)

    decoracion = db.Column(db.Text) 
    mensaje=db.Column(db.Text)

    def __init__(self,nombre,apellido,telefono,fechaEvento,sabor,tamano,cobertura,decoracion,mensaje):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.apellido=apellido
        self.telefono=telefono
        self.fechaEvento=fechaEvento
        self.sabor=sabor
        self.tamano=tamano
        self.cobertura=cobertura
        self.decoracion=decoracion
        self.mensaje=mensaje

# 8. Crear la tabla al ejecutarse la app
with app.app_context():
    db.create_all()

# Crear ruta de acceso
# / es la ruta de inicio
@app.route("/")
def index():
    return f'App Web para registrar pedidos de tortas'

# Recibir los datos que vienen del formulario 
# para insertarlos en la DB
@app.route("/registro", methods=['POST'])
def registro():
       
    nombre_recibido = request.json["nombre"]
    apellido=request.json['apellido']
    telefono=request.json['telefono']
    fechaEvento=request.json['fechaEvento']
    sabor=request.json['sabor']
    tamano=request.json['tamano']
    cobertura=request.json['cobertura']
    # decoracion=jsonify(request.json['decoracion'])
    decoracion=request.json['decoracion']

    # decoracion = set(request.json['decoracion'])
    decoracion_str = ','.join(decoracion)  # Convertir el conjunto a una cadena separada por comas para almacenarla en la base de datos

    mensaje=request.json['mensaje']

    # ¿Cómo insertar el registro en la tabla?
    nuevo_registro=Pedido(nombre_recibido,apellido,telefono,fechaEvento,sabor,tamano,cobertura,decoracion_str,mensaje)
    
    db.session.add(nuevo_registro)
    db.session.commit()
    # return nuevo_registro
    return "Solicitud via post recibida"


# Retornar todos los registros de la tabla producto, en un Json
@app.route("/pedidos",  methods=['GET'])
def pedidos():
    # Consultar la tabla pedidos y traer todos los registros
    # all_registros -> lista de objetos
    # all_registros = Pedido.query.all()
    all_registros = Pedido.query.order_by(desc(Pedido.id)).all()
    data_serializada = [] # Lista de diccionarios
    for registro in all_registros:
        data_serializada.append({
            "id":registro.id,
            "nombre":registro.nombre, 
            "apellido":registro.apellido,
            "telefono":registro.telefono,
            "fechaEvento":registro.fechaEvento, 
            "sabor":registro.sabor, 
            "tamano":registro.tamano,
            "cobertura":registro.cobertura,
            # "decoracion": list(registro.decoracion), 
            "decoracion": registro.decoracion, 
            "mensaje":registro.mensaje})

    # transformar a json
    return jsonify(data_serializada)


# Modificar un registro
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    # Buscar el registro por el id
    update_pedido = Pedido.query.get(id)

    # Recibir los nuevos datos a guardar
    # nombre = request.json["nombre"]
    # apellido=request.json['apellido']
    # stock=request.json['stock']
    # imagen=request.json['imagen']
    
    nombre = request.json["nombre"]
    apellido=request.json['apellido']
    telefono=request.json['telefono']
    fechaEvento=request.json['fechaEvento']
    sabor=request.json['sabor']
    tamano=request.json['tamano']
    cobertura=request.json['cobertura']
    decoracion=request.json['decoracion']

    # decoracion_str = ','.join(decoracion)
    # decoracion_str = json.dumps(decoracion)
    # print(decoracion_str)
    # decoracion_str = ','.join(decoracion) 
    decoracion_list = list(decoracion)

    mensaje=request.json['mensaje']

    # Sobreescribir la info
    update_pedido.nombre=nombre
    update_pedido.apellido=apellido
    update_pedido.telefono=telefono
    update_pedido.fechaEvento=fechaEvento
    update_pedido.sabor=sabor
    update_pedido.tamano=tamano
    update_pedido.cobertura=cobertura
    update_pedido.decoracion=','.join(decoracion_list)  # Convertir a cadena de texto
    update_pedido.mensaje=mensaje
    db.session.commit()

    data_serializada = [{"id":update_pedido.id, "nombre":update_pedido.nombre, "apellido":update_pedido.apellido, "telefono":update_pedido.telefono,
                          "fechaEvento":update_pedido.fechaEvento, "sabor":update_pedido.sabor, "tamano":update_pedido.tamano,
                          "cobertura":update_pedido.cobertura, "decoracion":decoracion_list, "mensaje":update_pedido.mensaje}]
    return jsonify(data_serializada)

    
# Eliminar un pediudo de la tabla pedidos por id
@app.route('/borrar/<id>', methods=['DELETE'])
def borrar(id):
    # Buscar el registro por el id
    delete_pedido = Pedido.query.get(id)

    # db.session.delete(delete_pedido)
    # db.session.commit()

    # data_serializada = [{"id":delete_pedido.id, "nombre":delete_pedido.nombre, "apellido":delete_pedido.apellido, "telefono":delete_pedido.telefono, 
    #                      "fechaEvento":delete_pedido.fechaEvento, "sabor":delete_pedido.sabor, "tamano":delete_pedido.tamano,
    #                      "cobertura":delete_pedido.cobertura, "decoracion":delete_pedido.decoracion, "mensaje":delete_pedido.mensaje}]

    # return jsonify(data_serializada)

    if delete_pedido:
        db.session.delete(delete_pedido)
        db.session.commit()
        return jsonify({"message": "Pedido eliminado correctamente"})
    else:
        return jsonify({"error": "El pedido no existe"}), 404

if __name__ == "__main__":
    app.run(debug=True)

