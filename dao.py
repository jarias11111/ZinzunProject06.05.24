from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from models import regisExperiencia, regisFormacion

class Conexion():
    def __init__(self):
        self.cliente = MongoClient()
        self.bd = self.cliente.PROYECTO

    def cerrar(self):
        self.cliente.close()

    def consultFormacion(self):
        return [self.convert_objectid(f) for f in self.bd.formacion.find()]

    def convert_objectid(self, doc):
        doc['_id'] = str(doc['_id'])
        return doc

    def consultExperiencia(self):
        return [self.convert_objectid(f) for f in self.bd.experiencia.find()]

    def registrarExperiencia(self, exp: regisExperiencia):
        resultado = self.bd.experiencia.insert_one(exp.dict())
        # Crear el diccionario de salida con el estado y mensaje
        salida = {
            "estatus": "success",
            "mensaje": f"Experiencia registrada con ID {resultado.inserted_id}"
        }
        return salida

    def registrarFormacion(self, form: regisFormacion):
        resultado = self.bd.formacion.insert_one(form.dict())
        # Crear el diccionario de salida con el estado y mensaje
        salida = {
            "estatus": "success",
            "mensaje": f"Formación registrada con ID {resultado.inserted_id}"
        }
        return salida

    def modificar_experiencia(self, id_experiencia: str, exp: regisExperiencia):
        # Consultar la experiencia existente por su ID
        experiencia_existente = self.bd.experiencia.find_one({"_id": ObjectId(id_experiencia)})

        if experiencia_existente:
            # Actualizar los campos de la experiencia con los nuevos valores
            datos_actualizados = exp.dict(exclude_unset=True)
            resultado = self.bd.experiencia.update_one({"_id": ObjectId(id_experiencia)}, {"$set": datos_actualizados})

            if resultado.modified_count > 0:
                return {
                    "estatus": "success",
                    "mensaje": f"Experiencia con ID {id_experiencia} actualizada exitosamente"
                }
        else:
            return {
                "estatus": "error",
                "mensaje": f"No se encontró ninguna experiencia con ID {id_experiencia}"
            }
        
    def modificar_formacion(self, id_formacion: str, form: regisFormacion):
        # Consultar la formación existente por su ID
        formacion_existente = self.bd.formacion.find_one({"_id": ObjectId(id_formacion)})

        if formacion_existente:
            # Actualizar los campos de la formación con los nuevos valores
            datos_actualizados = form.dict(exclude_unset=True)
            resultado = self.bd.formacion.update_one({"_id": ObjectId(id_formacion)}, {"$set": datos_actualizados})

            if resultado.modified_count > 0:
                return {
                    "estatus": "success",
                    "mensaje": f"Formación con ID {id_formacion} actualizada exitosamente"
                }
        else:
            return {
                "estatus": "error",
                "mensaje": f"No se encontró ninguna formación con ID {id_formacion}"
            }

    def eliminar_formacion(self, id_formacion: str):
        if not ObjectId.is_valid(id_formacion):
            return {
                "estatus": "error",
                "mensaje": "ID de formación no es válido"
            }

        resultado = self.bd.formacion.delete_one({"_id": ObjectId(id_formacion)})

        if resultado.deleted_count > 0:
            return {
                "estatus": "success",
                "mensaje": f"Formación con ID {id_formacion} eliminada exitosamente"
            }
        else:
            return {
                "estatus": "error",
                "mensaje": f"No se encontró ninguna formación con ID {id_formacion}"
            }
        
    def eliminar_experiencia(self, id_experiencia: str):
        if not ObjectId.is_valid(id_experiencia):
            return {
                "estatus": "error",
                "mensaje": "ID de Experiencia no es válido"
            }

        resultado = self.bd.experiencia.delete_one({"_id": ObjectId(id_experiencia)})

        if resultado.deleted_count > 0:
            return {
                "estatus": "success",
                "mensaje": f"Experiencia con ID {id_experiencia} eliminada exitosamente"
            }
        else:
            return {
                "estatus": "error",
                "mensaje": f"No se encontró ninguna experiencia con ID {id_experiencia}"
            }
        
    def consultar_experiencia_por_id(self, id_experiencia: int):
        experiencia = self.bd.ConsulUserExp.find_one({"_id": id_experiencia})
        if experiencia:
            return self.convert_objectid(experiencia)
        else:
            return None
        
    def consultar_formacion_por_id(self, id_formacion: int):
        formacion = self.bd.ConsulUserForm.find_one({"_id": id_formacion})
        if formacion:
            return self.convert_objectid(formacion)
        else:
            return None
        
