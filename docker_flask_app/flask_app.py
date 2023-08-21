import psycopg2
from flask import Flask, request, jsonify
import os

db_params = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT")
}

conn = psycopg2.connect(**db_params)

cursor = conn.cursor()

# Create table
cursor.execute("""CREATE TABLE IF NOT EXISTS dados_gripe(
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP,
                        sexo VARCHAR(255),
                        idade INTEGER,
                        sintomas VARCHAR(255),
                        dataInicioSintomas TIMESTAMP,
                        municipio VARCHAR(255),
                        estado VARCHAR(255),
                        tomouVacinaCovid BOOLEAN);""")
conn.commit()
cursor.close()
conn.close()


app = Flask(__name__)

# CRUD routes
@app.route('/pacientes', methods=['GET'])
def get_pacientes():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM dados_gripe;")
    pacientes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(pacientes)

@app.route('/paciente', methods=['POST'])
def create_paciente():
    data = request.json
    timestamp = data['timestamp']
    sexo = data['sexo']
    idade = data['idade']
    sintomas = data['sintomas']
    dataInicioSintomas = data['dataInicioSintomas']
    municipio = data['municipio']
    estado = data['estado']
    tomouVacinaCovid = data['tomouVacinaCovid']
    
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    cursor.execute("""INSERT INTO dados_gripe (timestamp, sexo, idade, sintomas, dataInicioSintomas, municipio, estado, tomouVacinaCovid)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                   (timestamp, sexo, idade, sintomas, dataInicioSintomas, municipio, estado, tomouVacinaCovid))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Paciente criado com sucesso."})

@app.route('/paciente/<int:id>', methods=['PUT'])
def update_paciente(id):
    data = request.json
    timestamp = data['timestamp']
    sexo = data['sexo']
    idade = data['idade']
    sintomas = data['sintomas']
    dataInicioSintomas = data['dataInicioSintomas']
    municipio = data['municipio']
    estado = data['estado']
    tomouVacinaCovid = data['tomouVacinaCovid']
    
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    cursor.execute("""UPDATE dados_gripe SET timestamp = %s, sexo = %s, idade = %s, sintomas = %s,
                      dataInicioSintomas = %s, municipio = %s, estado = %s, tomouVacinaCovid = %s
                      WHERE id = %s;""",
                   (timestamp, sexo, idade, sintomas, dataInicioSintomas, municipio, estado, tomouVacinaCovid, id))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({"message": f"Paciente {id} atualizado com sucesso."})

@app.route('/paciente/<int:id>', methods=['DELETE'])
def delete_paciente(id):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM dados_gripe WHERE id = %s;", (id,))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({"message": f"Paciente {id} excluído com sucesso."})

if __name__ == '__main__':
    app.run()
