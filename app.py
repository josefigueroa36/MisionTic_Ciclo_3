from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import random
import envioemail

app = Flask(__name__)
origen=""

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/VerificarUsuario",methods=["GET","POST"])
def VerificarUsuario():
    if request.method=="POST":
        correo=request.form["txtusuario"]
        correo=correo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        passw=request.form["txtpass"]
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        
        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest() #96 caracteres
        
        respuesta=controlador.validar_usuaro(correo,passw2)
        
        global origen
        
        if len(respuesta)==0:
            origen=""
            mensaje="ERROR DE AUtenticacion!!! verifique su usuario y contraseña y/o Verifique si su usario se encuentra activo."
            return render_template("informacion.html",data=mensaje)
        else:
            origen=correo
            respuesta2=controlador.listadoUsuarios(correo)
            return render_template("principal.html",data=respuesta2,infousuario=respuesta)
        
@app.route("/RegistrarUsuario",methods=["GET","POST"])
def RegistrarUsuario():
    if request.method=="POST":
        nombre=request.form["txtnombre"]
        nombre=nombre.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        correo=request.form["txtusuarioregistro"]
        correo=correo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        passw=request.form["txtpassregistro"]
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        
        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest() #96 caracteres
                        
        codigo=datetime.now()
        codigo2=str(codigo)
        codigo2=codigo2.replace("-","")
        codigo2=codigo2.replace(":","")
        codigo2=codigo2.replace(" ","")
        codigo2=codigo2.replace(".","")
        
        #codigo3=random.randint(10000,1000000)
        #codigo4=str(codigo3)+codigo2
                
        respuesta=controlador.regis_usuaro(nombre,correo, passw2,codigo2)
        
        if respuesta=="1":
            mensaje="Sr, usuario su codigo de activacion es :\n\n"+codigo2+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"
            asunto="Codigo de activacion"
            
            respEmail=envioemail.enviar(correo,mensaje,asunto)
            if respEmail=="1":
                mensaje="Usuarios Registrado Satisfactoriamente"
            else:
                mensaje="Registrado correctamente. Email no Enviado, Servicio no disponible, lo invitamos a utilizar el siguiente ecodigo de activacion: "+codigo2    
        else:
            mensaje="ERROR, el usuario y/o correo ya existen, verifique sus datos y vuelva a intentarlo"
            
        return render_template("informacion.html",data=mensaje)
    
    
@app.route("/ActivarUsuario",methods=["GET","POST"])
def ActivarUsuario():
    if request.method=="POST":
        codigo=request.form["txtcodigo"]
        codigo=codigo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        
        respuesta=controlador.activarU(codigo)

        if len(respuesta)==0:
            mensaje="Codigo incorrecto"
            return render_template("informacion.html",data=mensaje)
        else:
            mensaje="Usuario Activado Satisfactoriamente"
            return render_template("informacion.html",data=mensaje)
        

@app.route("/EnviarMensaje",methods=["GET","POST"])
def EnviarMensaje():
    if request.method=="POST":
        asunto=request.form["asunto"]
        asunto=asunto.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        mensaje=request.form["mensaje"]
        mensaje=mensaje.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        destino=request.form["destino"]
        destino=destino.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        
        controlador.regis_mensaje(asunto,mensaje,origen,destino)
        
        mensaje2="Usted ha recibo un nuevo mensaje, por favor ingrese a la plataforma para poder observarlo en su pestaña historial.\n\nMuchas Gracias"
        asunto2="Nuevo Mensaje"
        
        envioemail.enviar(destino,mensaje2,asunto2)
        
        return "EMAIL ENVIADO SATISFACTORIAMENTE"
    
@app.route("/cargaMailEnviados",methods=["GET","POST"])
def cargaMailEnviados():
    if request.method=="POST":
      
        respuesta=controlador.enviados(origen)
        return render_template("historialCorreo.html", listaCorreo=respuesta)
    
@app.route("/cargaMailRecibidos",methods=["GET","POST"])
def cargaMailRecibidos():
    if request.method=="POST":
      
        respuesta=controlador.recibidos(origen)
        return render_template("historialCorreo.html", listaCorreo=respuesta)
    
    
    
@app.route("/actualizarPassWord",methods=["GET","POST"])
def actualizarPassWord():
    if request.method=="POST":
        
        passw=request.form["password"]
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest()
        
        controlador.actualizar_P(passw2,origen)
        
        return "Contraseña actualizada satisfactoriamente"
    