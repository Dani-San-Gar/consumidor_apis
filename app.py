from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
 

# Modelo de datos
class Datos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    area = db.Column(db.String(50))
    categoria = db.Column(db.String(50))

    def to_dict(self):
        return {"id": self.id, "titulo": self.titulo, "area": self.area, "categoria": self.categoria}

# Inicializar la base de datos con datos de ejemplo
with app.app_context():
    db.create_all()
    if not Datos.query.first():
        datos_ejemplo = [
            Datos(titulo="Curso de Python", area="Tecnología", categoria="Programación"),
            Datos(titulo="Big Data", area="Tecnología", categoria="IA"),
            Datos(titulo="Marketing Digital", area="Negocios", categoria="Publicidad"),
            Datos(titulo="Aprender SQL", area="Tecnología", categoria="Bases de Datos"),
            Datos(titulo="Estrategias de Marketing", area="Negocios", categoria="Publicidad")
        ]
        db.session.add_all(datos_ejemplo)
        db.session.commit()
        print("Datos de ejemplo insertados.")

# Ruta API para obtener datos filtrados
@app.route('/api/datos/<area>/<categoria>', methods=['GET'])
def obtener_datos(area, categoria):
    datos_filtrados = Datos.query.filter_by(area=area, categoria=categoria).all()
    return jsonify([dato.to_dict() for dato in datos_filtrados])

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)