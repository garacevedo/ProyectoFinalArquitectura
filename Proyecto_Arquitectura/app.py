from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
import mysql.connector as sql_db 

app = Flask(__name__,template_folder='Template')

mysql = MySQL(app)

mysql = sql_db.connector.connect(
    host=app.config['localhost'],
    user=app.config['root'],
    password=app.config[''],
    database=app.config['login']
)
@app.route('/')
def home():
    return render_template('index.html')   

@app.route('/admin')
def admin():
    return render_template('admin.html')   

# ACCESO---LOGIN
@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
   
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
       
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']
        
        cursor = mysql.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
        account = cursor.fetchone()
      
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol']=account['id_rol']
            
            if session['id_rol']==1:
                return render_template("admin.html")
            elif session ['id_rol']==2:
                return render_template("Menu.html")
        else:
            return render_template('index.html',mensaje="Usuario O Contraseña Incorrectas")

#registro---
@app.route('/registro')
def registro():
    return render_template('registro.html')  

@app.route('/crear-registro', methods= ["GET", "POST"])
def crear_registro(): 
    
    correo=request.form['txtCorreo']
    password=request.form['txtPassword']
    cursor = mysql.connection.cursor()
    cursor.execute(" INSERT INTO usuarios (correo, password, id_rol) VALUES (%s, %s, '2')",(correo,password))
    mysql.connection.commit()
    
    return render_template("index.html",mensaje2="Usuario Registrado Exitosamente")
#-----------------------------------

#-----LISTAR USUARIOS-------------
@app.route('/listar', methods= ["GET", "POST"])
def listar(): 
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    
    return render_template("listar_usuarios.html",usuarios=usuarios)


#----------------------------------

if __name__ == '__main__':
   app.secret_key = "pinchellave"
   app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
