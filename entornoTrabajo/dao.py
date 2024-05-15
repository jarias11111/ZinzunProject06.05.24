from pymongo import MongoClient
from models import UsuarioInsert, UsuarioInactivo, AgregarHerramienta, Herramienta1, Usuario, UsuarioUpdate
from datetime import datetime
from bson import ObjectId

class Conexion():
    
#0
    def __init__(self):
        self.cliente=MongoClient()
        self.bd=self.cliente.opsdevs

    def cerrar(self):
        self.cliente.close()

#1  AGREGAR USUARIO
    def agregarUsuario(self,usuario:UsuarioInsert):
        respuesta={"estatus":"","mensaje":""}
        if usuario:
                    res=self.bd.desarrollador.insert_one(usuario.dict())
                    respuesta["estatus"]="OK"
                    respuesta["mensaje"]="Usuario agregado con id"+str(res)
                    respuesta["Usuario"]=usuario
        else:
                    respuesta["estatus"]="Error"
                    respuesta["mensaje"]="El Usuario no se agregó"
        return respuesta

#2  ELIMINAR USUARIO
    def comprobarUsuario(self,idUsuario):
        filtro = {"_id": ObjectId(idUsuario), "estatus": 'A'}
        usuario = self.bd.desarrollador.find_one(filtro)
        return usuario
    
    def cancelarUsuario(self,idUsuario,cancelacion:UsuarioInactivo): 
        usuario=self.comprobarUsuario(idUsuario)
        resp={"estatus":"","mensaje":""}
        if usuario:
            self.bd.desarrollador.update_one(
                    {"_id": ObjectId(idUsuario)},
                    {"$set": {"estatus": "INACTIVO"}}
                )
            resp["estatus"]="Ok"
            resp["mensaje"]=f"Usuario desactivado con id:{idUsuario}"  
        else:
            resp["estatus"]="Error"
            resp["mensaje"]="El usuario no se ha cancelado."
        return  resp
    
    # def comprobarUsuario(self,idUsuario):
    #     if isinstance(idUsuario, int):
    #         filtro = {"_id": idUsuario, "estatus": 'A'}
    #     elif isinstance(idUsuario, str):
    #         if idUsuario.isdigit():  
    #             filtro = {"_id": int(idUsuario), "estatus": 'A'}
    #         else:
    #             raise ValueError("El idUsuario no es válido. Debe ser un entero o una cadena de dígitos.")
    #     else:
    #         raise ValueError("El idUsuario debe ser de tipo entero o cadena de dígitos")
    #     usuario = self.bd.desarrollador.find_one(filtro)
    #     return usuario
    
    # def cancelarUsuario(self, idUsuario, cancelacion: UsuarioInactivo): 
    #     if isinstance(idUsuario, ObjectId):
    #         usuario = self.comprobarUsuario(idUsuario)
    #     elif isinstance(idUsuario, int):
    #         usuario = self.comprobarUsuario(ObjectId(str(idUsuario)))
    #     else:
    #         raise ValueError("El idUsuario debe ser un ObjectId o un entero")
    #     resp = {"estatus": "", "mensaje": ""}
    #     if usuario:
    #         self.bd.desarrollador.update_one(
    #             {"_id": idUsuario},
    #             {"$set": {"estatus": "INACTIVO"}}
    #         )
    #         resp["estatus"] = "Ok"
    #         resp["mensaje"] = f"Usuario desactivado con id: {idUsuario}"  
    #     else:
    #         resp["estatus"] = "Error"
    #         resp["mensaje"] = "El usuario no se ha cancelado."
    #     return resp

#3.1MODIFICAR USUARIO 
    def comprobarUsuario2(self,idUsuario):
        usuario=self.bd.desarrollador.find_one({"_id":ObjectId(idUsuario),
                                         "$or": [{"estatus": "INACTIVO"}, {"estatus": "A"}]})
        return usuario
    
    def modificarUsuario(self,idUsuario,modificar:UsuarioUpdate):
        user=self.comprobarUsuario2(idUsuario)
        resp={"estatus":"","mensaje":""}
        if user: 
            self.bd.desarrollador.update_one(
                    {"_id": ObjectId(idUsuario)},
                    {"$set": {"estatus": "A",
                              "telefono":modificar.telefono,
                              "email":modificar.email,
                              "calle":modificar.calle,
                              "num_int":modificar.num_int,
                              "num_ext":modificar.num_ext}}
            )
            resp["estatus"]="Ok"
            resp["mensaje"]=f"Usuario modificado en datos generales con id:{idUsuario}"  
        else:
            resp["estatus"]="Error"
            resp["mensaje"]="El usuario no se ha modificado ."
        return  resp

#3  MODIFICAR USAURIO POR HERRMIENTA
    def comprobarUsuario1(self,idUsuario):
        usuario=self.bd.desarrollador.find_one({"_id":int(idUsuario),
                                         "$or": [{"estatus": "INACTIVO"}, {"estatus": "A"}]})
        return usuario
    
    def comprobarHerramienta(self,idHerramienta):
        cont=self.bd.herramientas.count_documents({"_id":idHerramienta})
        return cont
    
    def agregarHerramientaUsuario(self,idUsuario,idHerramienta,herramienta:AgregarHerramienta):
        user=self.comprobarUsuario1(idUsuario)
        resp={"estatus":"","mensaje":""}
        if user:
                cont=self.comprobarHerramienta(idHerramienta)
                if cont>0:
                    res=self.bd.desarrollador.update_one({"_id": int(idUsuario)},
                                                         {"$push": {"herramienta": herramienta.dict()}}
                                                        )
                    resp["estatus"]="OK"
                    resp["mensaje"]=f'Se agregó una herramienta id:{idHerramienta} al usuario id:{idUsuario} con éxito.'
                else:
                        resp["estatus"]="Error"
                        resp["mensaje"]=f'No se agregó una herramienta al usuario id:{idUsuario} con éxito.'
        else:
                resp["estatus"]="Error"
                resp["mensaje"]='No existe la Herramienta.'
        return resp
    
#4  CONSULTA DE USUARIOS POR HERRAMIENTA
    def consultaGeneralHerramientas(self):
        resp={"estatus":"","mensaje":""}
        resp["estatus"]="OK"
        resp["mensaje"]="Listado de Usuarios con su Herramienta"
        usuarios = []
        for usuario_doc in self.bd.desarrollador.find():
            usuario = Usuario(**usuario_doc)
            herramientas_usuario = []
        for herramienta in usuario.herramientas:
            herramienta_doc = self.bd.herramientas.find_one({"_id": herramienta.idHerramienta})
            if herramienta_doc:
                herramientas_usuario.append(Herramienta1(**herramienta_doc))
        usuario.herramientas = herramientas_usuario
        usuarios.append(usuario)
        return usuarios

    def consultarHerramienta(self,idHerramienta):
        herramienta=self.bd.productos.find_one({"_id":idHerramienta})
        return herramienta

    def complementarHerramienta(self,herramienta):
        herr=self.consultarHerramienta(herramienta['_id'])
        herramienta['nombre']=herr['nombre']
        return herramienta