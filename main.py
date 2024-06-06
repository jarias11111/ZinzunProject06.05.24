import uvicorn
from dao import Conexion
from fastapi.responses import JSONResponse, Response, Any
from models import regisExperiencia, Respuesta, regisFormacion
from fastapi import HTTPException, WebSocketException, FastAPI

app = FastAPI()

@app.on_event('startup')
def startup():
    app.cn = Conexion()
    print('Conectando con la BD')

@app.on_event('shutdown')
def shutdown():
    app.cn.cerrar()
    print('Cerrando la conexion')

@app.get('/')
def inicio():
    return {"mensaje": "Bienvenido a CODYING"}

@app.get('/formacion', tags={"FORMACION"})
def consultFormacion():
    return app.cn.consultFormacion()

@app.get('/experiencia', tags={"EXPERIENCIA"})
def consultExperiencia():
    return app.cn.consultExperiencia()

@app.post('/agregarExperiencia', response_model=Respuesta, tags={"EXPERIENCIA"})
def registrarExperiencia(exp: regisExperiencia) -> Any:
    salida = app.cn.registrarExperiencia(exp)
    return Respuesta(**salida)

@app.post('/agregarFormacion', response_model=Respuesta, tags={"FORMACION"})
def registrarFormacion(form: regisFormacion) -> Any:
    salida = app.cn.registrarFormacion(form)
    return Respuesta(**salida)

@app.delete('/eliminarExperiencia/{id_experiencia}', response_model=Respuesta, tags=["EXPERIENCIA"])
def eliminar_experiencia(id_experiencia: str) -> Any:
    salida = app.cn.eliminar_experiencia(id_experiencia)

    if salida["estatus"] == "error":
        raise HTTPException(status_code=404 if 'No se encontró' in salida["mensaje"] else 400, detail=salida["mensaje"])

    return Respuesta(**salida)

@app.delete('/eliminarFormacion/{id_formacion}', response_model=Respuesta, tags=["FORMACION"])
def eliminar_formacion_endpoint(id_formacion: str) -> Any:
    salida = app.cn.eliminar_formacion(id_formacion)

    if salida["estatus"] == "error":
        raise HTTPException(status_code=404 if 'No se encontró' in salida["mensaje"] else 400, detail=salida["mensaje"])

    return Respuesta(**salida)

@app.put('/modificarExperiencia/{id_experiencia}', response_model=Respuesta, tags={"EXPERIENCIA"})
def modificar_experiencia(id_experiencia: str, exp: regisExperiencia) -> Any:
    salida = app.cn.modificar_experiencia(id_experiencia, exp)
    return Respuesta(**salida)

@app.put('/modificarFormacion/{id_formacion}', response_model=Respuesta, tags={"FORMACION"})
def modificar_formacion(id_formacion: str, form: regisFormacion) -> Any:
    salida = app.cn.modificar_formacion(id_formacion, form)
    return Respuesta(**salida)

@app.get('/experiencia/{id_experiencia}', tags={"EXPERIENCIA"})
def consultar_experiencia_por_id(id_experiencia: int):
    experiencia = app.cn.consultar_experiencia_por_id(id_experiencia)
    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia no encontrada")
    return experiencia

@app.get('/formacion/{id_formacion}', tags={"FORMACION"})
def consultar_formacion_por_id(id_formacion: int):
    formacion = app.cn.consultar_formacion_por_id(id_formacion)
    if not formacion:
        raise HTTPException(status_code=404, detail="Formación no encontrada")
    return formacion

if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, reload=True)