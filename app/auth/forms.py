from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,IntegerField,DecimalField,BooleanField
from wtforms.validators import DataRequired,Email,Length,NumberRange

class LoginForm(FlaskForm):
    name = StringField(label="username",render_kw={"placeholder":"username"},validators=[DataRequired(),Length(0,50)])
    hash_password = PasswordField(label="password",render_kw={"placeholder":"password"},validators=[DataRequired(),Length(0,30)])


class RegisterForm(FlaskForm):
    name = StringField(label="username",render_kw={"placeholder":"username"},validators=[DataRequired(),Length(0,50)])
    hash_password = PasswordField(label="hash_password",render_kw={"placeholder":"password"},validators=[DataRequired(),Length(0,30)])
    email = EmailField(label="email",render_kw={"placeholder":"email"},validators=[DataRequired(),Length(0,50)])
    phone = StringField(label="phone",render_kw={"placeholder":"phone"},validators=[DataRequired(),Length(11,11)])
    is_customer = BooleanField(label="is_customer")