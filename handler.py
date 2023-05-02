import mysql.connector
import json
import os
from dotenv import load_dotenv
from jsonaa import schemaSeba
import jsonschema
from config.conexion import Conexion


def registerUser(event, context):
    # Obtener los datos del usuario desde la petición HTTP
    data = json.loads(event['body'])
    nombre = data['nombre']
    apellido = data['apellido']
    usuario = data['usuario'] 
    password = data['password']
    campoVacio = ''

    if not nombre:
        campoVacio = "nombre"
    elif not apellido:
        campoVacio = "apellido"
    elif not usuario:
        campoVacio = "usuario"
    elif not password:
        campoVacio = "password"

    if campoVacio:
        response = {
            "statusCode": 400,
            "body": json.dumps({"mensaje": f"El campo '{campoVacio}' es obligatorio"})
        }
        return response
    else:     

        jsonschema.validate(data, schemaSeba)

        # Conectarse a la base de datos usando la conexión definida en el archivo conexion.py
        conexion = Conexion()
        cnx = conexion.get_connection()

        cursor = cnx.cursor()

        # Insertar el nuevo usuario en la tabla
        insert_query = "INSERT INTO usuarios (nombre, apellido, usuario, password) VALUES (%s, %s, %s, %s)"
        values = (nombre, apellido, usuario, password)
        cursor.execute(insert_query, values)
        cnx.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        cnx.close()

        # Devolver una respuesta HTTP indicando que el usuario ha sido registrado
        response = {
            "statusCode": 200,
            "body": json.dumps({"mensaje": "Usuario registrado correctamente"})
        }
        return response

def login(event, context):
    # Obtener los datos del usuario desde la petición HTTP
    data = json.loads(event['body'])
    usuario = data['usuario']
    password = data['password']
    campoVacio = ''

    if not usuario:
        campoVacio = "usuario"
    elif not password:
        campoVacio = "password"
    
    if campoVacio:
        response = {
            "statusCode": 400,
            "body": json.dumps({"mensaje": f"El campo '{campoVacio}' es obligatorio"})
        }
        return response
    else:
        # Conectarse a la base de datos
        conexion = Conexion()
        cnx = conexion.get_connection()

        cursor = cnx.cursor()

        # Verificar si el usuario y la contraseña son correctos
        select_query = "SELECT * FROM usuarios WHERE usuario=%s AND password=%s"
        values = (usuario, password)
        cursor.execute(select_query, values)

        # Obtener el resultado de la consulta
        result = cursor.fetchone()

        # Cerrar la conexión a la base de datos
        cursor.close()
        cnx.close()

        # Si el resultado de la consulta es None, entonces el usuario no existe o la contraseña es incorrecta
        if result is None:
            response = {
                "statusCode": 401,
                "body": json.dumps({"mensaje": "Usuario o contraseña incorrectos"})
            }
        else:
            nombre = result[1]
            apellido = result[2]
            response = {
                "statusCode": 200,
                "body": json.dumps({"mensaje": "Login exitoso", "nombre": nombre, "apellido": apellido})
            }

        return response

def updateUser(event, context):
    # Obtener los datos del usuario desde la petición HTTP
    data = json.loads(event['body'])
    id_usuario = data['id']
    nombre = data['nombre']
    apellido = data['apellido']
    usuario = data['usuario']
    password = data['password']
    campoVacio = ''
      
    if not id_usuario:
        campoVacio = "id"
    elif not nombre:
        campoVacio = "nombre"
    elif not apellido:
        campoVacio = "apellido"
    elif not usuario:
        campoVacio = "usuario"
    elif not password:
        campoVacio = "password"

    if campoVacio:
        response = {
            "statusCode": 400,
            "body": json.dumps({"mensaje": f"El campo '{campoVacio}' es obligatorio"})
        }
        return response
    else:
        # Conectarse a la base de datos
        conexion = Conexion()
        cnx = conexion.get_connection()

        cursor = cnx.cursor()

        # Actualizar los datos del usuario en la tabla
        update_query = "UPDATE usuarios SET nombre = %s, apellido = %s, usuario = %s, password = %s WHERE id = %s"
        values = (nombre, apellido, usuario, password, id_usuario)
        cursor.execute(update_query, values)
        cnx.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        cnx.close()

        # Devolver una respuesta HTTP indicando que el usuario ha sido actualizado
        response = {
            "statusCode": 200,
            "body": json.dumps({"mensaje": "Usuario actualizado correctamente"})
        }
        return response

def deleteUser(event, context):
    # Obtener el ID del usuario a eliminar desde los parámetros de la petición HTTP
    data = json.loads(event['body'])
    id_usuario = data['id']
    campoVacio = ''
      
    if not id_usuario:
        campoVacio = "id"
    
    
    if campoVacio:
        response = {
            "statusCode": 400,
            "body": json.dumps({"mensaje": f"El campo '{campoVacio}' es obligatorio"})
        }
        return response
    else:


        # Conectarse a la base de datos
        conexion = Conexion()
        cnx = conexion.get_connection()

        cursor = cnx.cursor()

        # Eliminar el usuario de la tabla
        delete_query = "DELETE FROM usuarios WHERE id = %s"
        values = (id_usuario,)
        cursor.execute(delete_query, values)
        cnx.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        cnx.close()

        # Devolver una respuesta HTTP indicando que el usuario ha sido eliminado
        response = {
            "statusCode": 200,
            "body": json.dumps({"mensaje": "Usuario eliminado correctamente"})
        }
        return response