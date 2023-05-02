import jsonschema

schemaSeba = {
        "schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "nombre": {
                "type": "string"
            },
            "apellido": {
                "type": "string"
            },
            "usuario": {
                "type": "string"
            },
            "password": {
                "type": "string"
            }
        },
        "required": [
            "nombre",
            "apellido",
            "usuario",
            "password"
        ]
    }


# from jsonschema import validate

# # Definir el esquema para validar los datos
# data_schema = {
#     "type": "object",
#     "properties": {
#         "nombre": {"type": "string"},
#         "apellido": {"type": "string"},
#         "edad": {"type": "integer", "minimum": 18}
#     },
#     "required": ["nombre", "apellido", "edad"]
# }


# def validate_data(data):
#     try:
#         validate(data, data_schema)
#         return True
#     except:
#         return False
