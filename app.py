from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'clave_secreta'

class SimpleForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET', 'POST'])
def formulario():
    form = SimpleForm()
    if form.validate_on_submit():
        return render_template('resultado.html', nombre=form.nombre.data, apellido=form.apellido.data)
    return render_template('formulario.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

