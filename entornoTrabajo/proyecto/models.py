from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

class RegionInsert(BaseModel):
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
