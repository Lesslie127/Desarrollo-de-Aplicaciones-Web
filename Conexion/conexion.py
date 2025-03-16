import mysql.connector

def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Leslie2003@",
        database="desarrollo_web"
    )
    return conexion
