# IMPORTACIONES: 
from flask import Flask, request, jsonify, render_template # request (permite post, get), render_template (carga html desde templates/)
from flask_cors import CORS                                # Permite peticiones desde otros dominios (frontend en otro servidor)
import pymysql                                             # Biblioteca para conectarse a BD mySQL
from datetime import datetime, timedelta                   # Manejo de horas
app = Flask(__name__)
CORS(app)                                                  # Habilitar CORS 

# CONEXION CON MYSQL
def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="hora_azul",
        cursorclass=pymysql.cursors.DictCursor            # Devuelve resultados como diccionarios
    )

# ACTUALIZAR APARCAMIENTOS LIBRES Y OCUPAR POR TIEMPO
@app.route('/activar', methods=['POST'])
def activar_estado():
    data = request.get_json()                             # Extrae codigo y tiempo en JSON
    codigo = data.get('codigo')
    tiempo = data.get('tiempo')  

    if not codigo or not (30 <= tiempo <= 150):           # Valida que el código no esté vacío y el tiempo esté en orquilla
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        expiracion = datetime.now() + timedelta(minutes=tiempo) # Calcula la hora de expiración

        conn = get_connection()                           # Instrucciones SQL
        with conn.cursor() as cursor:
            cursor.execute("UPDATE aparcamientos2 SET estado = 0 WHERE tiempo < NOW()")
            cursor.execute("""
                UPDATE aparcamientos2 
                SET estado = 1, tiempo = %s 
                WHERE codigo = %s
            """, (expiracion, codigo))
        conn.commit()
        conn.close()

        return jsonify({"mensaje": f"Estado activado para {codigo} hasta {expiracion.strftime('%H:%M:%S')}"}) # Devuelve mensaje con hora expiración
    except Exception as e:
        print("Error al activar:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

# CARGAR FRONTEND
@app.route('/')
def index():
    return render_template('html2.html')  

# INICIA FLASK
if __name__ == '__main__':
    app.run(debug=True)