from fastapi import FastAPI, HTTPException
from dao import Conexion
from models import Herramienta, UsuarioInsert, UsuarioInactivo, Usuario, UsuarioUpdate, RegionInsert,FavoritosInsert, HerramientasInsert
from fastapi.responses import JSONResponse, Response, Any
from datetime import datetime
from bson import ObjectId,DatetimeConversion
from time import strftime
from pymongo import MongoClient,ReturnDocument
import uvicorn


app = FastAPI()

#0
@app.get('/')
def inicio ():
    return {"mensaje":"Bienvenido a devOpsREST "}

@app.on_event('startup')
def startup():
    app.cn=Conexion()
    print("Conectando con la BD")

@app.on_event('shutdown')
def shutdown():
    app.cn.cerrar()
    print("Cerrando la Conexión")

#1
@app.post('/usuarios', tags=["USUARIO"])
def agregarUsuario (usuario:UsuarioInsert):
    salida=app.cn.agregarUsuario(usuario)
    return salida

#2
@app.delete('/usuarios/{idUsuario}/cancelar', tags=["USUARIO"])
def cancelarUsuario (idUsuario:str,usuario:UsuarioInactivo):
    salida=app.cn.cancelarUsuario(idUsuario,usuario)
    return salida
#3.1
@app.put('/usuarios/{idUsuario}/modificar', tags=["USUARIO"])
def modificarUsuario(idUsuario:str, modificar: UsuarioUpdate):
    salida = app.cn.modificarUsuario(idUsuario, modificar)
    return salida

#3
@app.put('/usuarios/{idUsuario}/agregarHerramienta', tags=["MODIFICAR USUARIO POR ELEMENTO"])
def agregarHerramientaUsuario (idUsuario:str, herramienta:Herramienta):
    salida=app.cn.agregarHerramientaUsuario(idUsuario,herramienta.idHerramienta,herramienta)
    return salida

#4
@app.get('/herramientas/{idUsuario}', tags=["CONSULTAS DE USUARIO POR ELEMENTO"])
def consultaGeneralHerramientas(idUsuario:str):
    herramientas = app.cn.consultaGeneralHerramientas(idUsuario)
    if herramientas:
        return herramientas
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    ################################### MOISES VERDUZCO

    #-------------------REGION---------------------------#
@app.post('/AgregarRegion', tags=["RegionREST"])
def agregarRegion(region:RegionInsert):
    #return {"mensaje":"Agregando un pedido"}
    salida=app.cn.agregarRegion(region)
    return salida

@app.get('/consultarRegion/{idRegion}', tags=["RegionREST"])
def consultarRegion(idRegion: str):
    salida = app.cn.consultarRegion(idRegion)
    return salida

@app.put("/modificarRegion/{idRegion}", tags=["RegionREST"])
def modificarRegion(idRegion: str, region: RegionInsert):
    resultado = app.cn.modificarRegion(idRegion, region)
    return resultado

@app.delete("/eliminarRegion/{idRegion}", tags=["RegionREST"])
def eliminarRegion(idRegion: str):
    resultado = app.cn.eliminarRegion(idRegion)
    return resultado

#-------------------Favoritos---------------------------#
@app.post('/Agregarfavoritos',tags=["FavoritosREST"])
def agregarFavoritos(favoritos:FavoritosInsert):
    #return {"mensaje":"Agregando un pedido"}
    salida=app.cn.agregarFavoritos(favoritos)
    return salida

@app.get('/consultarFavoritos/{idFavoritos}',tags=["FavoritosREST"])
def consultarFavoritos(idFavoritos: str):
    salida = app.cn.consultarFavoritos(idFavoritos)
    return salida

@app.put("/modificarFavoritos/{idFavoritos}", tags=["FavoritosREST"])
def modificarFavoritos(idFavoritos: str, favoritos: FavoritosInsert):
    resultado = app.cn.modificarFavoritos(idFavoritos, favoritos)
    return resultado

@app.delete("/eliminarFavoritos/{idFavoritos}", tags=["FavoritosREST"])
def eliminarFavoritos(idFavoritos: str):
    resultado = app.cn.eliminarFavoritos(idFavoritos)
    return resultado

if __name__ == '__main--':
    uvicorn.run("main:app",port=8500, reload=True)