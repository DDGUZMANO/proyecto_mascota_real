from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa Flask-CORS
import json
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

# --- Configuración de la Base de Datos PostgreSQL ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:douguzman29@localhost/petmatch'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cuidador(db.Model):
    __tablename__ = 'cuidadores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    ubicacion = db.Column(db.String(80), nullable=False)
    experiencia = db.Column(db.Integer)
    acepta_perro = db.Column(db.Boolean)
    acepta_gato = db.Column(db.Boolean)
    # Puedes añadir más campos si los tienes en tu JSON
    # Ejemplo: contacto = db.Column(db.String(120))

    def __repr__(self):
        return f'<Cuidador {self.nombre}>'

class Mascota(db.Model):
    __tablename__ = 'mascotas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    ubicacion = db.Column(db.String(80), nullable=False)
    necesidades_especiales = db.Column(db.Boolean)
    # Puedes añadir más campos si los tienes en tu JSON
    # Ejemplo: raza = db.Column(db.String(50))

    def __repr__(self):
        return f'<Mascota {self.nombre}>'

# Ruta para la página principal (opcional, puede que ya la tengas)
@app.route('/')
def index():
    return "¡Backend de PetMatch funcionando!"

# Cargar datos desde archivos JSON
def cargar_datos(archivo):
    try:
        base_dir = Path(__file__).parent.parent
        json_path = base_dir / "datos" / f"{archivo}.json"

        print(f"Buscando archivo en: {json_path}")  # Debug

        if not json_path.exists():
            raise FileNotFoundError(f"Archivo {json_path} no existe")

        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    except Exception as e:
        print(f"🚨 Error cargando {archivo}: {str(e)}")
        return []  # Retorna lista vacía para evitar que falle la app

# --- Tus funciones de compatibilidad (sin cambios) ---
def calcular_compatibilidad_cuidador(cuidador, mascota):
    compatibilidad = 0

    # 1. Tipo de mascota (adaptado a tus campos)
    tipo_mascota = mascota["tipo"].lower()  # "perro", "gato", etc.
    if cuidador.get(f"acepta_{tipo_mascota}", False):
        compatibilidad += 1

    # 2. Ubicación (adaptado)
    if cuidador["ubicacion"] == mascota["ubicacion"]:
        compatibilidad += 2  # Peso mayor a ubicación

    # 3. Tamaño (omitido, pues no existe en tus datos actuales)

    # 4. Necesidades especiales (ejemplo adaptado)
    if mascota.get("necesidades_especiales", False):
        if cuidador["experiencia"] >= 3:  # Ajustado a tu dato "experiencia": 3
            compatibilidad += 1
        else:
            compatibilidad -= 1

    return compatibilidad

def encontrar_compatibles_cuidador(datos_formulario, base_de_datos_mascotas):
    """
    Encuentra mascotas compatibles con los datos del cuidador.

    Args:
        datos_formulario (dict): Diccionario con los datos del cuidador.
        base_de_datos_mascotas (list): Lista de diccionarios con los datos de las mascotas.

    Returns:
        list: Lista de tuplas (compatibilidad, id_mascota).
    """

    resultados_cuidador = []
    for mascota in base_de_datos_mascotas:
        compatibilidad = calcular_compatibilidad_cuidador(datos_formulario, mascota)
        resultados_cuidador.append((compatibilidad, mascota["id"]))  # Asumiendo que cada mascota tiene un "id"

    resultados_cuidador.sort(key=lambda x: x[0], reverse=True)
    return resultados_cuidador

def generar_salida_usuario_mascotas(resultados_cuidador, base_de_datos_mascotas, num_mascotas=2):
    salida_usuario_mascotas = []
    for compatibilidad, id_mascota in resultados_cuidador[:num_mascotas]:
        for mascota in base_de_datos_mascotas:
            if mascota["id"] == id_mascota:
                # Adaptamos la salida al JSON que manejas actualmente
                salida_usuario_mascotas.append({
                    "id": mascota["id"],
                    "nombre": mascota["nombre"],
                    "compatibilidad": compatibilidad
                    # Omite "url_imagen" ya que no está en tu JSON actual
                })
                break
    return salida_usuario_mascotas

# --- Nuevas funciones para la funcionalidad mascota-cuidador ---
def calcular_compatibilidad_mascota(mascota, cuidador):
    compatibilidad = 0

    # 1. Tipo de mascota
    tipo_mascota = mascota["tipo"].lower()
    if cuidador.get(f"acepta_{tipo_mascota}", False):
        compatibilidad += 1

    # 2. Ubicación
    if mascota["ubicacion"] == cuidador["ubicacion"]:
        compatibilidad += 2

    # 3. Necesidades especiales de la mascota
    if mascota.get("necesidades_especiales", False):
        if cuidador["experiencia"] >= 3:
            compatibilidad += 1
        else:
            compatibilidad -= 1

    return compatibilidad

def encontrar_compatibles_mascota(datos_mascota, base_de_datos_cuidadores):
    """
    Encuentra cuidadores compatibles con los datos de la mascota.

    Args:
        datos_mascota (dict): Diccionario con los datos de la mascota.
        base_de_datos_cuidadores (list): Lista de diccionarios con los datos de los cuidadores.

    Returns:
        list: Lista de tuplas (compatibilidad, id_cuidador).
    """
    resultados_mascota = []
    for cuidador in base_de_datos_cuidadores:
        compatibilidad = calcular_compatibilidad_mascota(datos_mascota, cuidador)
        resultados_mascota.append((compatibilidad, cuidador["id"]))  # Asumiendo que cada cuidador tiene un "id"

    resultados_mascota.sort(key=lambda x: x[0], reverse=True)
    return resultados_mascota

def generar_salida_usuario_cuidadores(resultados_mascota, base_de_datos_cuidadores, num_cuidadores=2):
    salida_usuario_cuidadores = []
    for compatibilidad, id_cuidador in resultados_mascota[:num_cuidadores]:
        for cuidador in base_de_datos_cuidadores:
            if cuidador["id"] == id_cuidador:
                salida_usuario_cuidadores.append({
                    "id": cuidador["id"],
                    "nombre": cuidador["nombre"],
                    "compatibilidad": compatibilidad
                })
                break
    return salida_usuario_cuidadores

# --- Rutas de la API ---
@app.route('/cuidadores')
def listar_cuidadores():
    return jsonify(cargar_datos("cuidadores"))

@app.route('/mascotas')
def listar_mascotas():
    return jsonify(cargar_datos("mascotas"))

@app.route('/compatibilidad', methods=['POST'])
def calcular_compatibilidad():
    datos_cuidador = request.json  # Datos del formulario del cuidador
    mascotas = cargar_datos("mascotas")

    resultados = encontrar_compatibles_cuidador(datos_cuidador, mascotas)
    mascotas_compatibles = generar_salida_usuario_mascotas(resultados, mascotas)

    return jsonify(mascotas_compatibles)

# --- Nueva ruta para la funcionalidad mascota-cuidador ---
@app.route('/compatibilidad_mascota', methods=['POST'])
def encontrar_cuidadores_compatibles():
    datos_mascota = request.json  # Datos de la mascota
    cuidadores = cargar_datos("cuidadores")

    resultados = encontrar_compatibles_mascota(datos_mascota, cuidadores)
    cuidadores_compatibles = generar_salida_usuario_cuidadores(resultados, cuidadores)

    return jsonify(cuidadores_compatibles)

@app.route('/')
def home():
    return "API de PetMatch - Usa /cuidadores, /mascotas o /compatibilidad"

if __name__ == '__main__':
    # Crea las tablas de la base de datos (solo la primera vez)
    #with app.app_context():
       # db.create_all()
    app.run(debug=True)

