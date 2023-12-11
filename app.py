from flask import Flask, render_template, request, jsonify,redirect,url_for,flash, request
from dotenv import load_dotenv
from config import config
from database.db_mysql import db
from forms import LoginForm
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import secrets
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import secrets
from flask_wtf import CSRFProtect
from database.models import Usuario
from flask_principal import Permission, RoleNeed
from functools import wraps
from flask import abort
import json
from flask_seasurf import SeaSurf
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()
app.secret_key = secrets.token_hex(16)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Resto del código de la aplicación Flask
# @app.route('/', methods=['GET', 'POST'])   
# def login():
#     return render_template('login.html')
@login_manager.user_loader
def load_user(user):
    print('hola jajaja', user )
    user= Usuario.obtenerUsuario_por_id(db,user)
    return user

@login_manager.user_loader
def load_user(user_id):
    user = Usuario.obtenerUsuario_por_id(db, int(user_id))
    return user


#-------------------------------------------LOGIN -------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])   
def login():
     if current_user.is_authenticated:
         return redirect('principal.html')
 
     form = LoginForm(meta={'csrf': False}) 
     if request.method == 'POST':
         if form.validate_on_submit():
             user_log = form.validate_user(db)
             print("estoy en login form", user_log)
             if user_log is not None:
                 print("bien entre login", user_log)
                 login_user(user_log)
                 return redirect(url_for("principal"))
             flash('Datos incorrectos, inténtelo nuevamente', 'error')
         else:
             flash('Datos incorrectos, inténtelo nuevamente', 'error')
 
     return render_template('login.html', form=form)
 
 
@app.route('/principal', methods=['GET', 'POST'])
@login_required
def principal():
    print(current_user,'hola usuario jajaja')
    return render_template('principal.html')

    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
   

def pagina_no_encontrada(error):
   return "<h1> La página que intentas buscar no existe... </h1>"

def status_401(error):
     return redirect('login')

if __name__ =='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.register_error_handler(401, status_401)
    app.run()