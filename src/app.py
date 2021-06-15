from logging import debug
from flask import Flask, request, jsonify
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Config por defecto para evitar el "warning"

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Creamos la tabla
class Task(db.Model):
    id = db.Column (db.Integer, primary_key = True)
    title = db.Column (db.String(70), unique = True)
    description = db.Column (db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

#Lee todas las clases, y crea las tablas especificadas
db.create_all()

#Esquema que interactua
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description') #lo que quiero obtener


task_schema = TaskSchema()
tasks_schema = TaskSchema(many = True) #Multiples respuestas

@app.route('/')
def index():
    return jsonify({'message':'Welcome to my API'})

@app.route('/tasks', methods = ['POST']) #Puedo probar la ruta, enviando un POST al task
def create_task(): #Guardo datos
    title = request.json['title'] #Guardo lo enviado por json
    description = request.json['description']
    
    new_Task = Task(title, description) #Guardo la tarea en una variable
    db.session.add(new_Task) #asigna la tarea en bd
    db.session.commit() #termina la operacion
    
    return task_schema.jsonify(new_Task) #Vemos por consola lo que acabamos de guardar en bs


    #print(request.json) #imprime en consola el valor ingresado por task(route)
    #return 'received' #Informa al postman, que se recibio el valor.

@app.route('/tasks', methods = ['GET'])
def get_tasks():  # Obtener todos los datos guardados
    all_tasks = Task.query.all() #Muestrame todas las tareas guardadas
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<id>', methods = ['GET'])
def get_task(id):
    task = Task.query.get(id) #obten de BD
    return task_schema.jsonify(task) #view task console postman

@app.route('/tasks/<id>', methods = ['PUT'])
def update_task(id):
    task = Task.query.get(id) #guardo

    title = request.json['title'] # Obtengo y guardo los datos en variables
    description = request.json['description']

    task.title = title # add 
    task.description = description # add

    db.session.commit()
    return task_schema.jsonify(task) # view task actuality

@app.route('/tasks/<id>', methods = ['DELETE'])
def delete_task(id):
    task = Task.query.get(id) #get task
    db.session.delete(task) #delete task
    db.session.commit() #close operation

    return task_schema.jsonify(task) #view deleted task

if __name__ == "__main__":
    app.run(debug = True)

