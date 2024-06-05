from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

class RegionInsert(BaseModel):
    _id: ObjectId
    _id: int
    pais: str
    estado: str
    ciudad: str

class FavoritosInsert(BaseModel):
    id_usuarioDesarrollador: int
    id_usuarioEmpleador: int
    calificacion: int
    comentarios: str
    

class HerramientasInsert(BaseModel):
    nombre : str
    fabricante: str
    version: str
    descripcion: str
    tipo: str

class certificaciones(BaseModel):
    
    nombre:str
    vigencia:int
    empresa:str
    nivel:str
    
class desarrollador(BaseModel):
    id_usuario : int
    nombre_completo: str
    empresa_reclutador: str
    empresa_giro : str
    cargo: str
    telefono : int
    estatus : str
    email: str
    calle: str
    num_int: int
    num_ext: int
    cp : str
    region:RegionInsert
    herramientas:HerramientasInsert
    certificaciones:certificaciones




