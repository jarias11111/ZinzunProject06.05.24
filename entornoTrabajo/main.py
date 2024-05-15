from fastapi import FastAPI
from dao import Conexion
from models import UsuarioInsert, UsuarioInactivo, AgregarHerramienta, Usuario, UsuarioUpdate
from fastapi.responses import JSONResponse, Response, Any
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
def agregarHerramientaUsuario (idUsuario:str, herramienta:AgregarHerramienta):
    salida=app.cn.agregarHerramientaUsuario(idUsuario,herramienta.herramienta.idHerramienta, herramienta)
    return salida

#@app.put('/usuarios/{idUsuario}/agregarHerramienta', tags=["MODIFICAR USUARIO POR ELEMENTO"])
#def agregarHerramientaUsuario (idUsuario: Union[str, int], herramienta:AgregarHerramienta):
#    salida=app.cn.agregarHerramientaUsuario(idUsuario,herramienta.herramienta.idHerramienta, herramienta)
#    return salida

#4
@app.get('/herramientas', response_model=list[Usuario], tags=["CONSULTAS DE USUARIO POR ELEMENTO"])
def consultaGeneralHerramientas():
    salida = app.cn.consultaGeneralHerramientas()
    return salida

if __name__ == '__main--':
    uvicorn.run("main:app",port=8000, reload=True)