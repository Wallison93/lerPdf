import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="23.92.218.194",
        user="c41_dev02",
        password="db.uHL$dev02.25",
        database="c41_hold_aplicativo"
    )