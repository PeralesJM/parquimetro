# IMPORTACIONES: 
from flask import Flask, request, jsonify, render_template # request (permite post, get), render_template (carga html desde templates/)
from flask_cors import CORS                                # Permite peticiones desde otros dominios (frontend en otro servidor)
from datetime import datetime, timedelta                   # Manejo de horas
from supabase import create_client, Client
import os
app = Flask(__name__)
CORS(app)                                                  # Habilitar CORS 

# CONEXION CON MYSQL
SUPABASE_URL = "https://qovpbfngsyaenrwaxoix.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFvdnBiZm5nc3lhZW5yd2F4b2l4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NzI5NDI3NSwiZXhwIjoyMDYyODcwMjc1fQ.Y0PW-AkWBvgSzm7bygTUD85fLuHdy0Im7k4oad21qOc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
        supabase.table("aparcamientos") \
            .update({"estado": 0}) \
            .lte("tiempo", datetime.utcnow().isoformat()) \
            .execute()
        # Luego, actualizar el aparcamiento concreto
        response = supabase.table("aparcamientos") \
            .update({"estado": 1, "tiempo": expiracion.isoformat()}) \
            .eq("codigo", codigo) \
            .execute()
        if response.data:
            return jsonify({"mensaje": f"Estado activado para {codigo} hasta {expiracion.strftime('%H:%M:%S')}"}), 200
        else:
            return jsonify({"error": "No se encontró el aparcamiento con ese código"}), 404
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