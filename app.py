from flask import Flask, request, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/usuario', methods=['POST'])
def usuario():
    nombre = request.form['nombre']
    return render_template('usuario.html', nombre=nombre)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
