import sqlite3

def validar_usuaro(usuario,password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo='"+usuario+"' and password='"+password+"' and estado='1'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def listadoUsuarios(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where  estado='1' and correo<>'"+correo+"' order by nombres asc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def enviados(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora,u.nombres  from mensajeria m, usuarios u  where u.correo=m.id_usu_recibe and m.id_usu_envia='"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def recibidos(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora,u.nombres  from mensajeria m, usuarios u  where u.correo=m.id_usu_envia and m.id_usu_recibe='"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def actualizar_P(pw, correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set password='"+pw+"' where correo='"+correo+"'"
    cursor.execute(consulta)
    db.commit()
    return "1"

def regis_usuaro(nombre,correo,password,codigo):
    
    try:
        db=sqlite3.connect("mensajes.s3db")
        db.row_factory=sqlite3.Row
        cursor=db.cursor()
        consulta="insert into usuarios (nombres,correo,password,estado,codigoactivacion) values ('"+nombre+"','"+correo+"','"+password+"','0','"+codigo+"')"
        cursor.execute(consulta)
        db.commit()
        return "1"
    except :
        return "0"
    
    

def regis_mensaje(asunto,mensaje,origen,destino):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into mensajeria (asunto,mensaje,fecha,hora,id_usu_envia,id_usu_recibe,estado) values ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def activarU(codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set estado='1' where codigoactivacion='"+codigo+"'"
    print(consulta)
    cursor.execute(consulta)
    db.commit()
    
    consulta="select *from usuarios where estado='1' and  codigoactivacion='"+codigo+"'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado
    
