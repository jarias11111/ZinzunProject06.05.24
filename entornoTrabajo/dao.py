from pymongo import MongoClient
from models import Herramienta, UsuarioInsert, UsuarioInactivo, Herramienta1, Usuario, UsuarioUpdate, RegionInsert, HerramientasInsert, FavoritosInsert
from datetime import datetime
from bson import ObjectId

class Conexion():
    
#0
    def __init__(self):
        self.cliente=MongoClient()
        self.bd=self.cliente.opsdevs

    def cerrar(self):
        self.cliente.close()

#1  AGREGAR USUARIO
    def agregarUsuario(self,usuario:UsuarioInsert):
        respuesta={"estatus":"","mensaje":""}
        if usuario:
                    res=self.bd.desarrollador.insert_one(usuario.dict())
                    respuesta["estatus"]="OK"
                    respuesta["mensaje"]="Usuario agregado con id"+str(res)
                    respuesta["Usuario"]=usuario
        else:
                    respuesta["estatus"]="Error"
                    respuesta["mensaje"]="El Usuario no se agregó"
        return respuesta

#2  ELIMINAR USUARIO
    def comprobarUsuario(self,idUsuario):
        filtro = {"_id": ObjectId(idUsuario), "estatus": 'A'}
        usuario = self.bd.desarrollador.find_one(filtro)
        return usuario
    
    def cancelarUsuario(self,idUsuario,cancelacion:UsuarioInactivo): 
        usuario=self.comprobarUsuario(idUsuario)
        resp={"estatus":"","mensaje":""}
        if usuario:
            self.bd.desarrollador.update_one(
                    {"_id": ObjectId(idUsuario)},
                    {"$set": {"estatus": "INACTIVO"}}
                )
            resp["estatus"]="Ok"
            resp["mensaje"]=f"Usuario desactivado con id:{idUsuario}"  
        else:
            resp["estatus"]="Error"
            resp["mensaje"]="El usuario no se ha cancelado."
        return  resp
    
    #AL CONSULTAR POR HERRAMIENTA NO SE MUESTRAN TODAS LAS HERRAMIENTAS CREADAS
    #COMO SE MANDA LLAMAR DE UNA CONSULTAGENERAL
    #
    
    # def comprobarUsuario(self,idUsuario):
    #     if isinstance(idUsuario, int):
    #         filtro = {"_id": idUsuario, "estatus": 'A'}
    #     elif isinstance(idUsuario, str):
    #         if idUsuario.isdigit():  
    #             filtro = {"_id": int(idUsuario), "estatus": 'A'}
    #         else:
    #             raise ValueError("El idUsuario no es válido. Debe ser un entero o una cadena de dígitos.")
    #     else:
    #         raise ValueError("El idUsuario debe ser de tipo entero o cadena de dígitos")
    #     usuario = self.bd.desarrollador.find_one(filtro)
    #     return usuario
    
    # def cancelarUsuario(self, idUsuario, cancelacion: UsuarioInactivo): 
    #     if isinstance(idUsuario, ObjectId):
    #         usuario = self.comprobarUsuario(idUsuario)
    #     elif isinstance(idUsuario, int):
    #         usuario = self.comprobarUsuario(ObjectId(str(idUsuario)))
    #     else:
    #         raise ValueError("El idUsuario debe ser un ObjectId o un entero")
    #     resp = {"estatus": "", "mensaje": ""}
    #     if usuario:
    #         self.bd.desarrollador.update_one(
    #             {"_id": idUsuario},
    #             {"$set": {"estatus": "INACTIVO"}}
    #         )
    #         resp["estatus"] = "Ok"
    #         resp["mensaje"] = f"Usuario desactivado con id: {idUsuario}"  
    #     else:
    #         resp["estatus"] = "Error"
    #         resp["mensaje"] = "El usuario no se ha cancelado."
    #     return resp

#3.1 MODIFICAR USUARIO 
    def comprobarUsuario2(self,idUsuario):
        usuario=self.bd.desarrollador.find_one({"_id":ObjectId(idUsuario),
                                         "$or": [{"estatus": "INACTIVO"}, {"estatus": "A"}]})
        return usuario
    
    def modificarUsuario(self,idUsuario,modificar:UsuarioUpdate):
        user=self.comprobarUsuario2(idUsuario)
        resp={"estatus":"","mensaje":""}
        if user: 
            self.bd.desarrollador.update_one(
                    {"_id": ObjectId(idUsuario)},
                    {"$set": {"estatus": "A",
                              "telefono":modificar.telefono,
                              "email":modificar.email,
                              "calle":modificar.calle,
                              "num_int":modificar.num_int,
                              "num_ext":modificar.num_ext}}
            )
            resp["estatus"]="Ok"
            resp["mensaje"]=f"Usuario modificado en datos generales con id:{idUsuario}"  
        else:
            resp["estatus"]="Error"
            resp["mensaje"]="El usuario no se ha modificado ."
        return  resp

#3  MODIFICAR USAURIO POR HERRAMIENTA
    def comprobarUsuario1(self,idUsuario,idHerramienta):
        usuario=self.bd.desarrollador.find_one({"_id": ObjectId(idUsuario),
                                         "$or": [{"estatus": "INACTIVO"}, {"estatus": "A"}]})
        if usuario:
                cont1 = self.bd.desarrollador.herramienta.count_documents(
                                {"idUsuario": ObjectId(idUsuario),
                                 "herramientas": {
                                 "$elemMatch": {"_id": int(idHerramienta)}
                                                 }
                                }                                                           
                                                                         )
                return cont1
        else:
                return None
    
    def comprobarHerramienta(self,idHerramienta):
        cont=self.bd.herramientas.count_documents({"_id":idHerramienta})
        return cont
    
    def agregarHerramientaUsuario(self,idUsuario,idHerramienta,herramienta:Herramienta):
        cont1=self.comprobarUsuario1(idUsuario,idHerramienta)
        resp={"estatus":"","mensaje":""}
        if cont1<0:
                cont=self.comprobarHerramienta(idHerramienta)
                if cont>0:
                    self.bd.desarrollador.update_one({"_id": ObjectId(idUsuario)},
                                                         {"$push": {"herramienta": herramienta.dict()}}
                                                        )
                    resp["estatus"]="OK"
                    resp["mensaje"]=f'Se agregó una herramienta id:{idHerramienta} al usuario id:{idUsuario} con éxito.'
                else:
                        resp["estatus"]="Error"
                        resp["mensaje"]=f'No se agregó una herramienta al usuario id:{idUsuario} con éxito. Por que no existe la Herramienta'
        else:
                resp["estatus"]="Error"
                resp["mensaje"]='El usuario ya cuenta con la Herramienta agregada'
        return resp
    
#4  CONSULTA DE USUARIOS POR HERRAMIENTA
    def convert_objectid(self, cursor):
        result = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            result.append(doc)
        return result

    def consultaGeneralHerramientas(self,idUsuario:str):
        herramientas=self.bd.consultaHerramienta.find({"_id":ObjectId(idUsuario)})
        usuario = None
        for herramienta in herramientas:
            if usuario is None:
                usuario = {
                    "_id": str(herramienta["_id"]),
                    "nombre": herramienta["nombre"],
                    "apellido_pat": herramienta["apellido_pat"],
                    "apellido_mat": herramienta["apellido_mat"],
                    "herramientas": []
                }
            herramienta_info = herramienta.pop("herramienta1")
            usuario["herramientas"].append(herramienta_info)

        return usuario 
    
############### MOISES VERDUZCO

#-------------------REGION---------------------------#
    def agregarRegion(self,region:RegionInsert):
        respuesta={"estatus":"","mensaje":""}
        if region:
                    res=self.bd.region.insert_one(region.dict())
                    respuesta["estatus"]="OK"
                    respuesta["mensaje"]="Usuario agregado con id"
                    respuesta["Usuario"]=region
        else:
                    respuesta["estatus"]="Error"
                    respuesta["mensaje"]="El Usuario no se agregó"
        return respuesta

    def consultarRegion(self, id_region: str):
        id_object = ObjectId(id_region)
        region = self.bd.region.find_one({"_id": id_object})
        if region is None:
            return {"mensaje": "La región no existe"}
        region["_id"] = str(region["_id"])
        return region

    def modificarRegion(self, id_region: str, region: RegionInsert):
        id_object = ObjectId(id_region)
        region_dict = region.dict()
        respuesta={"estatus":"","mensaje":""}
        if region:
            res= self.bd.region.update_one({"_id": id_object},{"$set": region_dict})
            respuesta["estatus"]="OK"
            respuesta["mensaje"]=f"Región con id:{id_object} actualizada correctamente"
            respuesta["Usuario"]=region
        else:
            respuesta["estatus"]="Error"
            respuesta["mensaje"]="No se realizaron cambios"
        return respuesta      

    def eliminarRegion(self, id_Region: str):
        id_object = ObjectId(id_Region)
        resultado = self.bd.region.delete_one({"_id": id_object})

        if resultado.deleted_count == 0:
            return {"mensaje": "No se encontró un favorito con ese id"}

        return {
            "mensaje": f"Favorito con id:{id_object} eliminado correctamente",
            "estatus": "OK"
        }

#-------------------Favoritos---------------------------#
    def agregarFavoritos(self,favoritos:FavoritosInsert):
        respuesta={"estatus":"","mensaje":""}
        if favoritos:
                    res=self.bd.favoritos.insert_one(favoritos.dict())
                    respuesta["estatus"]="OK"
                    respuesta["mensaje"]="Usuario agregado con id"
                    respuesta["Usuario"]=favoritos
        else:
                    respuesta["estatus"]="Error"
                    respuesta["mensaje"]="El Usuario no se agregó"
        return respuesta

    def consultarFavoritos(self, id_Favoritos: str):
        id_object = ObjectId(id_Favoritos)
        favoritos = self.bd.favoritos.find_one({"_id": id_object})
        if favoritos is None:
            return {"mensaje": "La región no existe"}
        favoritos["_id"] = str(favoritos["_id"])
        return favoritos

    def modificarFavoritos(self, id_favoritos: str, favoritos: FavoritosInsert):
        id_object = ObjectId(id_favoritos)
        favoritos_dict = favoritos.dict()
        respuesta={"estatus":"","mensaje":""}
        if favoritos:
            res= self.bd.favoritos.update_one({"_id": id_object},{"$set": favoritos_dict})
            respuesta["estatus"]="OK"
            respuesta["mensaje"]=f"favoritos con id:{id_object} actualizada correctamente"
            respuesta["Usuario"]=favoritos
        else:
            respuesta["estatus"]="Error"
            respuesta["mensaje"]="No se realizaron cambios"
        return respuesta    

    def eliminarFavoritos(self, id_Favoritos: str):
        id_object = ObjectId(id_Favoritos)
        respuesta={"estatus":"","mensaje":""}
        resultado = self.bd.favoritos.delete_one({"_id": id_object})

        if resultado.deleted_count == 0:
            respuesta["estatus"]="Error"
            respuesta["mensaje"]="No se encontró un favorito con ese id"

        else :
            respuesta["estatus"]="OK"
            respuesta["mensaje"]=f"Favorito con id:{id_object} eliminado correctamente"

        return respuesta

#-------------------Herramientas---------------------------#
    # def consultarHerramientas(self, id_Herramientas: str):
    #      id_object = ObjectId(id_Herramientas)
    #      herramientas = self.bd.herramientas.find_one({"_id": id_object})
    #      if herramientas is None:
    #           return {"mensaje": "La herramienta no existe"}
    #      herramientas["_id"] = str(herramientas["_id"])
    #      return herramientas

    # def agregarHerramientas(self, herramientas: HerramientasInsert):
    #      respuesta={"estatus":"","mensaje":""}
    #      if herramientas:
    #           res= self.bd.herramientas.insert_one(herramientas.dict())
    #           respuesta["estatus"]="OK"
    #           respuesta["mensaje"]=f"Herramienta con id:{res.inserted_id} agregada correctamente"
    #           respuesta["Usuario"]=herramientas
    #      else:
    #           respuesta["estatus"]="Error"
    #           respuesta["mensaje"]="No se realizaron cambios"
    #      return respuesta

    # def modificarHerramientas(self, id_herramientas: str, herramientas: HerramientasInsert):
    #      id_object = ObjectId(id_herramientas)
    #      herramientas_dict = herramientas.dict()
    #      herramientas_dict["_id"] = id_object
    #      respuesta={"estatus":"","mensaje":""}
    #      res= self.bd.herramientas.update_one({"_id": id_object},{"$set": herramientas_dict})
    #      if res.modified_count == 0:
    #           respuesta["estatus"]="Error"
    #           respuesta["mensaje"]="No se realizaron cambios"
    #      else:
    #           respuesta["estatus"]="OK"
    #           respuesta["mensaje"]=f"Herramienta con id:{id_object} modificada correctamente"
    #           respuesta["Usuario"]=herramientas
    #      return respuesta

    # def eliminarHerramientas(self, id_herramientas: str):
    #      id_object = ObjectId(id_herramientas)
    #      respuesta={"estatus":"","mensaje":""}
    #      res= self.bd.herramientas.delete_one({"_id": id_object})
    #      if res.deleted_count == 0:
    #           respuesta["estatus"]="Error"
    #           respuesta["mensaje"]="No se encontró una herramienta con ese id"
    #      else:
    #         respuesta["estatus"]="OK"
    #         respuesta["mensaje"]=f"Herramienta con id:{id_object} eliminado correctamente"
    #      return respuesta
    