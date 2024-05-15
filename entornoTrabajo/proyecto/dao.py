from pymongo import MongoClient,ReturnDocument
from models import RegionInsert,FavoritosInsert, HerramientasInsert
from datetime import datetime
from bson import ObjectId,DatetimeConversion
from time import strftime
class Conexion():
    def __init__(self):
        self.cliente=MongoClient()
        self.bd=self.cliente.proyecto

    def cerrar(self):
        self.cliente.close()
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
    def consultarHerramientas(self, id_Herramientas: str):
         id_object = ObjectId(id_Herramientas)
         herramientas = self.bd.herramientas.find_one({"_id": id_object})
         if herramientas is None:
              return {"mensaje": "La herramienta no existe"}
         herramientas["_id"] = str(herramientas["_id"])
         return herramientas
    
    def agregarHerramientas(self, herramientas: HerramientasInsert):
         respuesta={"estatus":"","mensaje":""}
         if herramientas:
              res= self.bd.herramientas.insert_one(herramientas.dict())
              respuesta["estatus"]="OK"
              respuesta["mensaje"]=f"Herramienta con id:{res.inserted_id} agregada correctamente"
              respuesta["Usuario"]=herramientas
         else:
              respuesta["estatus"]="Error"
              respuesta["mensaje"]="No se realizaron cambios"
         return respuesta
    
    def modificarHerramientas(self, id_herramientas: str, herramientas: HerramientasInsert):
         id_object = ObjectId(id_herramientas)
         herramientas_dict = herramientas.dict()
         herramientas_dict["_id"] = id_object
         respuesta={"estatus":"","mensaje":""}
         res= self.bd.herramientas.update_one({"_id": id_object},{"$set": herramientas_dict})
         if res.modified_count == 0:
              respuesta["estatus"]="Error"
              respuesta["mensaje"]="No se realizaron cambios"
         else:
              respuesta["estatus"]="OK"
              respuesta["mensaje"]=f"Herramienta con id:{id_object} modificada correctamente"
              respuesta["Usuario"]=herramientas
         return respuesta
    
    def eliminarHerramientas(self, id_herramientas: str):
         id_object = ObjectId(id_herramientas)
         respuesta={"estatus":"","mensaje":""}
         res= self.bd.herramientas.delete_one({"_id": id_object})
         if res.deleted_count == 0:
              respuesta["estatus"]="Error"
              respuesta["mensaje"]="No se encontró una herramienta con ese id"
         else:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]=f"Herramienta con id:{id_object} eliminado correctamente"
         return respuesta


    