from pymongo import MongoClient,ReturnDocument
from models import RegionInsert,FavoritosInsert, HerramientasInsert, certificaciones
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
    def agregarRegion(self, region: RegionInsert, _id: int):
            region_dict = region.dict()
            region_dict["_id"] = _id
            result = self.bd.region.insert_one(region_dict)
            salida = {
                "estatus": "OK",
                "mensaje": f"region registrada con id {result.inserted_id}"
            }
            return salida
        
    def consultarRegion(self, id_region: str):
        region = self.bd.region.find_one({"_id": id_region})
        if region is None:
            return {"mensaje": "La región no existe"}
        region["_id"] = str(region["_id"])
        return region
    
    
    def ConsulUserRegion(self, id_region: int):
        desarrolladores = list(self.bd.ConsulUserRegion.find({"Region._id": id_region}))
        
        if not desarrolladores:
            return {"mensaje": "No se encontraron desarrolladores en esa región"}
            
        resultado = []
        for desarrollador in desarrolladores:
            desarrollador["_id"] = str(desarrollador["_id"])
            resultado.append(desarrollador)
        
        return resultado

    
    def modificarRegion(self, id_region: int, region: RegionInsert):
        region_dict = region.dict()
        
        respuesta={"estatus":"","mensaje":""}
        if region:
            res= self.bd.region.update_one({"_id": id_region},{"$set": region_dict})
            respuesta["estatus"]="OK"
            respuesta["mensaje"]=f"Región con id:{id_region} actualizada correctamente"
            respuesta["Usuario"]=region
        else:
            respuesta["estatus"]="Error"
            respuesta["mensaje"]="No se realizaron cambios"
        return respuesta      

    def eliminarRegion(self, id_Region: int):
        resultado = self.bd.region.delete_one({"_id": id_Region})
        
        if resultado.deleted_count == 0:
            return {"mensaje": "No se encontró un favorito con ese id"}
        
        return {
            "mensaje": f"Region con id:{id_Region} eliminado correctamente",
            "estatus": "OK"
        }
    
#-------------------Favoritos---------------------------#
    def agregarFavoritos(self,favoritos:FavoritosInsert, _id:int):
        respuesta={"estatus":"","mensaje":""}
        favoritos_dict = favoritos.dict()
        favoritos_dict["_id"] = _id
        if favoritos:
                    res=self.bd.favoritos.insert_one(favoritos_dict)
                    respuesta["estatus"]="OK"
                    respuesta["mensaje"]=f"favorito agregado con id: {res.inserted_id}"
                    respuesta["Usuario"]=favoritos
        else:
                    respuesta["estatus"]="Error"
                    respuesta["mensaje"]="El Usuario no se agregó"
        return respuesta
    
    def consultarFavoritos(self, id_Favoritos: str):
        favoritos = self.bd.favoritos.find_one({"_id": id_Favoritos})
        if favoritos is None:
            return {"mensaje": "La región no existe"}
        favoritos["_id"] = str(favoritos["_id"])
        return favoritos
    
    def modificarFavoritos(self, id_favoritos: int, favoritos: FavoritosInsert):
        #id_object = ObjectId(id_favoritos)
        favoritos_dict = favoritos.dict()
        respuesta={"estatus":"","mensaje":""}
        if favoritos:
            res= self.bd.favoritos.update_one({"_id": id_favoritos},{"$set": favoritos_dict})
            respuesta["estatus"]="OK"
            respuesta["mensaje"]=f"favoritos con id:{id_favoritos} actualizada correctamente"
            respuesta["Usuario"]=favoritos
        else:
            respuesta["estatus"]="Error"
            respuesta["mensaje"]="No se realizaron cambios"
        return respuesta    

    def eliminarFavoritos(self, id_Favoritos: int):
        #id_object = ObjectId(id_Favoritos)
        respuesta={"estatus":"","mensaje":""}
        resultado = self.bd.favoritos.delete_one({"_id": id_Favoritos})
        
        if resultado.deleted_count == 0:
            respuesta["estatus"]="Error"
            respuesta["mensaje"]="No se encontró un favorito con ese id"
        
        else :
            respuesta["estatus"]="OK"
            respuesta["mensaje"]=f"Favorito con id:{id_Favoritos} eliminado correctamente"
       
        return respuesta
    
    def consultaGeneralFav(self ):
         res=self.bd.favoritos.find()
         return res
    
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
    
    def ConsUsuario_x_herramientas(self, nombre:str, certificaciones:certificaciones ):
        str = str(nombre)
        certificaciones=self.db.usuarios.find({"certificaciones.nombre": str})
        if certificaciones is None:
             return {"mensaje": "No se encontraron usuarios con esa herramienta"}
        certificaciones["nombre"] = str(certificaciones["nombre"])
        return certificaciones






    