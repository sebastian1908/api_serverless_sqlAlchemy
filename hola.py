import json
from jsonaa import validate_data

data = {
    "nombre": True,
    "apellido": "Pérez",
    "edad": 30
}

# Validar los datos usando el esquema definido en validar.py
if validate_data(data):
    print("Los datos son válidos")
else:
    print("Los datos no son válidos")
