from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

#1
class UsuarioInsert(BaseModel):
    nombre:str
    apellido_pat:str
    apellido_mat:str
    empresa_reclutador:str| None=None
    empresa_giro:str| None=None
    cargo:str| None=None
    telefono:str
    email:str
    calle:str
    num_int:str
    num_ext:str
    CP:str
    fechaRegistro:datetime=Field(default=datetime.now())
    tipo:str
    estatus:str=Field(default='A')

#2
class UsuarioInactivo(BaseModel):
    estatus:str=Field(default='DESACTIVADO')
    motivoCancelacion:str

#3.1
class UsuarioUpdate(BaseModel):
    telefono:str
    email:str
    calle:str
    num_int:str
    num_ext:str
    CP:str

#3
class Herramienta(BaseModel):
    idHerramienta:int
    nivel:str
    fecha:datetime=Field(default=datetime.now())

#4
class Herramienta1(BaseModel):
    idHerramienta:int
    nombre:str
    fabricante:str
    version:str
    descripcion:str
    tipo:str
   
class HerramientaConsulta(BaseModel):
    herramientas:list[Herramienta1]
    estatus:str
    mensaje:str

class Usuario(BaseModel):
    _id: str
    nombre: str
    apellido_pat: str
    apellido_mat: str
    telefono: str
    estatus: str
    email: str
    calle: str
    num_int: str
    num_ext: str
    CP: int
    herramientas:list[Herramienta1] | None=None


    ################################## MOISES VERDUZCO

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