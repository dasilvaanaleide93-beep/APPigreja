import os
import sqlite3
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

DB = "mural.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recados
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nome TEXT,
                  mensagem TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mural')
def mural_page():
    return render_template('mural.html')

@app.route('/api/mural', methods=['GET', 'POST'])
def api_mural():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        data = request.get_json()
        nome = data.get('nome', 'Anônimo')
        mensagem = data.get('mensagem', '')
        if mensagem:
            c.execute("INSERT INTO recados (nome, mensagem) VALUES (?,?)", (nome, mensagem))
            conn.commit()
        conn.close()
        return jsonify({"status": "ok"})
    else:
        c.execute("SELECT nome, mensagem FROM recados ORDER BY id DESC")
        recados = [{"nome": r[0], "mensagem": r[1]} for r in c.fetchall()]
        conn.close()
        return jsonify(recados)

@app.route('/pedidos')
def pedidos():
    try:
        with open('pedidos.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = []
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
