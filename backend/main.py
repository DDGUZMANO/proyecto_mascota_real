from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa Flask-CORS
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

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

@app.route('/')
def home():
    return "API de PetMatch - Usa /cuidadores, /mascotas o /compatibilidad"

if __name__ == '__main__':
    app.run(debug=True)