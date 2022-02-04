from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

from config import config
from validation import *


app = Flask(__name__)

# CORS(app)
CORS(app, resources={r"/cursos/*": {"origins": "http://localhost"}})

conexion = MySQL(app)


# @cross_origin
@app.route('/tasks', methods=['GET'])
def getallTasks():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM TASKS"
        cursor.execute(sql)
        data = cursor.fetchall()
        tasks = []
        for da in data:
            task = {'id':da[0],'name': da[1], 'description': da[2],'completed':da[3]}
            tasks.append(task)
        return jsonify({'tasks': tasks}),200
    except Exception as ex:
        return "Error",500


def getTaskById(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tasks WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        tasks = cursor.fetchone()
        if tasks != None:
            task = {'id': tasks[0], 'name': tasks[1], 'description': tasks[2]}
            return task
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/task/<id>', methods=['GET'])
def getTask(id):
    try:
        task = getTaskById(id)
        if task != None:
            return task
        else:
            return jsonify({'message': "no task with id "+id})
    except Exception as ex:
        return "Error", 500


@app.route('/task', methods=['POST'])
def addTask():
   
    if (validate_name(request.json['name']) and validate_description(request.json['description'])
     and validate_is_completed(request.json['completed'])):
        try:
                cursor = conexion.connection.cursor()
                sql = """INSERT INTO tasks (name, description, completed) 
                VALUES ('{0}', '{1}', {2})""".format(request.json['name'],
                                                     request.json['description'], request.json['completed'])
                cursor.execute(sql)
                conexion.connection.commit()  
                return "created",201
        except Exception as ex:
            return jsonify({'message': "Error"})
    else:
        return "bad request",400


@app.route('/task/<id>', methods=['PUT'])
def updateTask(id):
    if (validate_name(request.json['name']) and 
    validate_description(request.json['description'])and validate_is_completed(request.json['completed'])):
        try:
            task = getTaskById(id)
            if task != None:
                cursor = conexion.connection.cursor()
                sql = """UPDATE tasks SET name = '{0}', description = '{1}', completed= {2} 
                WHERE id = {3}""".format(request.json['name'], request.json['description'],request.json['completed'],id)
                cursor.execute(sql)
                conexion.connection.commit() 
                return jsonify({'id':id, 'name': request.json['name'],'description':
                request.json['description'],'completed':request.json['completed']}),200
            else:
                return 'Not found',404
        except Exception as ex:
            return 'Internal error',500
    else:
        return 'Bad request',400


@app.route('/task/<id>', methods=['DELETE'])
def deleteTask(id):
    try:
        task = getTaskById(id)
        if task != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM tasks WHERE id = '{0}'".format(id)
            cursor.execute(sql)
            conexion.connection.commit()  
            return task, 200
        else:
            return "not found",404
    except Exception as ex:
        return "Server error",500


def notFound(error):
    return "not found", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,notFound)
    app.run()
