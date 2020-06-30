import os
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Queue

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = os.environ.get('DEBUG')
app.config['ENV'] = os.environ.get('ENV')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)

queue = Queue()


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/new', methods=['POST'])
def new_item():
    new_user = request.get_json()
    queue.enqueue(new_user)
    return jsonify({"msg":f"Se ha agregado el usuario '{new_user['nombre']}' a la cola"}),200

@app.route('/next', methods=['GET'])
def next_item():
    processed_user = queue.dequeue()
    if processed_user:
        return jsonify({"msg":f"El usuario {processed_user['nombre']} fue procesado y eliminado de la fila"}), 200
    else:
        return jsonify({"msg": "No hay usuarios en la cola para procesar"}),200

@app.route('/all', methods=['GET'])
def all_items():
    users_list = queue.get_queue()
    if users_list:
        return jsonify(users_list), 200
    else:
        return jsonify({"msg":"No hay usuarios en la cola"}), 200


if __name__ == '__main__':
    manager.run()