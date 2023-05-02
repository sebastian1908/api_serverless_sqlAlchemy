import json
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from config.conexion import Conexion
from model.usuario import Usuario

conn = Usuario()

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
        # Conectarse a la base de datos

        conexion = Conexion()
        engine = conexion.get_connection()
        Session = sessionmaker(bind=engine)
        session = Session()

        # Insertar el nuevo usuario en la tabla
        nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, usuario=usuario, password=password)
        session.add(nuevo_usuario)
        session.commit()

        # Cerrar la sesión
        session.close()

        # Devolver una respuesta HTTP indicando que el usuario ha sido registrado
        response = {
            "statusCode": 200,
            "body": json.dumps({"mensaje": "Usuario registrado correctamente"})
        }
        return response

def login(event, context):
    # Obtener los datos de inicio de sesión desde la petición HTTP
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
        engine = conexion.get_connection()
        Session = sessionmaker(bind=engine)
        session = Session()

        # Verificar el inicio de sesión
        user = session.query(Usuario).filter_by(usuario=usuario, password=password).first()

        # Cerrar la sesión
        session.close()

        # Devolver una respuesta HTTP indicando si el inicio de sesión fue exitoso o no
        if user is not None:
            response = {
                "statusCode": 200,
                "body": json.dumps({"mensaje": "Inicio de sesión exitoso", "nombre": user.nombre, "apellido": user.apellido})
            }
        else:
            response = {
                "statusCode": 401,
                "body": json.dumps({"mensaje": "Credenciales incorrectas"})
            }

        return response

def updateUser(event, context):
    # Obtener los datos del usuario desde la petición HTTP
    data = json.loads(event['body'])
    id = data['id']
    nombre = data['nombre']
    apellido = data['apellido']
    usuario = data['usuario'] 
    password = data['password']
    campoVacio = ''

    if not id:
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
        engine = conexion.get_connection()
        Session = sessionmaker(bind=engine)
        session = Session()

        # Obtener el usuario a actualizar
        usuario_actualizar = session.query(Usuario).get(id)

        # Actualizar los datos del usuario
        usuario_actualizar.nombre = nombre
        usuario_actualizar.apellido = apellido
        usuario_actualizar.usuario = usuario
        usuario_actualizar.password = password

        # Guardar los cambios en la base de datos
        session.commit()

        # Cerrar la sesión
        session.close()

        # Devolver una respuesta HTTP indicando que el usuario ha sido actualizado
        response = {
            "statusCode": 200,
            "body": json.dumps({"mensaje": "Usuario actualizado correctamente"})
        }
        return response

def deleteUser(event, context):
    # Obtener el ID del usuario desde la petición HTTP
    data = json.loads(event['body'])
    user_id = data['id']
    campoVacio = ''

    if not user_id:
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
        engine = conexion.get_connection()
        Session = sessionmaker(bind=engine)
        session = Session()

        # Buscar el usuario por ID
        usuario = session.query(Usuario).filter_by(id=user_id).first()

        # Si no se encuentra el usuario, devolver una respuesta HTTP de error
        if not usuario:
            response = {
                "statusCode": 404,
                "body": json.dumps({"mensaje": "No se encontró el usuario"})
            }
            return response

        # Eliminar el usuario de la base de datos
        session.delete(usuario)
        session.commit()

        # Cerrar la sesión
        session.close()

        # Devolver una respuesta HTTP indicando que el usuario ha sido eliminado
        response = {
            "statusCode": 200,
            "body": json.dumps({"mensaje": "Usuario eliminado correctamente"})
        }
        return response