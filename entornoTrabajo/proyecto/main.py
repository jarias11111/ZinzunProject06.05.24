from fastapi import FastAPI
import json
from bson.json_util import dumps
import uvicorn
from models import RegionInsert, FavoritosInsert, HerramientasInsert
from dao import Conexion

app=FastAPI()
@app.on_event('startup')
def startup():
    app.cn=Conexion()
    print('Conectando con la BD')

@app.on_event('shutdown')
def shutdown():
    app.cn.cerrar()
    print('Cerrando la conexion')

@app.get("/")
async def root():
    return {"message":"Bienvenido"}
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
#-------------------Herramientas---------------------------#
@app.post('/AgregarHerramientas', tags=["HerramientasREST"])
def agregarHerramientas(herramientas:HerramientasInsert):
    #return {"mensaje":"Agregando un pedido"}
    salida=app.cn.agregarHerramientas(herramientas)
    return salida
@app.get('/consultarHerramientas/{idHerramientas}', tags=["HerramientasREST"])
def consultarHerramientas(idHerramientas: str):
    salida = app.cn.consultarHerramientas(idHerramientas)
    return salida
@app.put("/modificarHerramientas/{idHerramientas}", tags=["HerramientasREST"])
def modificarHerramientas(idHerramientas: str, herramientas: HerramientasInsert):
    resultado = app.cn.modificarHerramientas(idHerramientas, herramientas)
    return resultado
@app.delete("/eliminarHerramientas/{idHerramientas}", tags=["HerramientasREST"])
def eliminarHerramientas(idHerramientas: str):
    resultado = app.cn.eliminarHerramientas(idHerramientas)
    return resultado



if __name__ == '__main__':
    uvicorn.run("main:app",port=5500,reload=True)