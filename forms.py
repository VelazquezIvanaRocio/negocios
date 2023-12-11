from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,DateField,SelectField,IntegerField,EmailField
from wtforms.validators import DataRequired, Email, InputRequired,EqualTo,Length,ValidationError
from wtforms import HiddenField
from database.models import Usuario

class LoginForm(FlaskForm):

    user = StringField('Usuario', validators=[DataRequired()],render_kw={"class": "form-control"})
    password = PasswordField('Contraseña', validators=[DataRequired()],render_kw={"class": "form-control","id":"contrasenia"})
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user.errors = []  # Inicializar como lista vacía
        self.password.errors = []

    
    def validate_user(self, db):
        user = self.user.data
        password = self.password.data
        usuario = Usuario.obtenerUsuario_por_usuario(db, user)
        if usuario is not None and Usuario.revisar_contraseña_hasheada(usuario.password, password):
            usuario.password = None
            return usuario
        return None
