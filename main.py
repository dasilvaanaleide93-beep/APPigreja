import os
import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DB = "mural.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS recados (id INTEGER PRIMARY KEY, nome TEXT, mensagem TEXT)')
    conn.commit()
    conn.close()
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mural')
@app.route('/mural/novo')
@app.route('/mu')
def mural_page():
    return render_template('mural.html')

@app.route('/api/mural', methods=['GET','POST'])
def api_mural():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        d = request.get_json()
        c.execute("INSERT INTO recados (nome, mensagem) VALUES (?,?)", (d.get('nome','Anônimo'), d.get('mensagem','')))
        conn.commit()
        conn.close()
        return jsonify({"status":"ok"})
    else:
        c.execute("SELECT nome, mensagem FROM recados ORDER BY id DESC")
        recados = [{"nome": r[0], "mensagem": r[1]} for r in c.fetchall()]
        conn.close()
        return jsonify(recados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
