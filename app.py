from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>¡Hola! Bienvenido a mi Proyecto Web</h1>
        <form action="/usuario" method="post">
            <label for="nombre">Ingresa tu nombre:</label>
            <input type="text" id="nombre" name="nombre" required>
            <input type="submit" value="Enviar">
        </form>
    '''

@app.route('/usuario', methods=['POST'])
def usuario():
    nombre = request.form['nombre']
    return f'<h1>Bienvenido, {nombre}!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
