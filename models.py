from pydantic import BaseModel

class centro_formador(BaseModel):
    nombre:str
    Telefono:str
    Correo:str
    Tipo:str

class formacion(BaseModel):
    idFormacion:int
    id_desarrollador:int
    nombre:str
    evidencia:str
    fecha_inicio:str
    fecha_terminacion:str
    estado:str
    tipo:str
    centro_formador:list[centro_formador]

class tecnologias(BaseModel):
    nombre:str

class responsabilidades(BaseModel):
    nombre:str

class proyectos(BaseModel):
    nombre:str
    tecnologias:list[tecnologias]
    objetivo:str
    responsabilidades:list[responsabilidades]

class experiencia(BaseModel):
    _id:int
    id_desarrollador:int
    puesto:str
    empresa:str
    periodo:str
    proyectos:list[proyectos]

class regisExperiencia(BaseModel):
    id_desarrollador:int
    puesto:str
    empresa:str
    periodo:str
    proyectos:list[proyectos]

class Respuesta(BaseModel):
    estatus:str
    mensaje:str

class regisFormacion(BaseModel):
    id_desarrollador:int
    nombre:str
    evidencia:str
    fecha_inicio:str
    fecha_terminacion:str
    estado:str
    tipo:str
    centro_formador:list[centro_formador]

