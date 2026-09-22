import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS

# AQUI JÁ ESTÁ ARRUMADO PRA SUAS PASTAS Modelos e estática
app = Flask(__name__, template_folder='Modelos', static_folder='estática')
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

# ESSA ROTA AGORA ACEITA ENVIAR E VER
@app.route('/mural/novo', methods=['GET', 'POST'])
def mural_novo():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        nome = request.form.get('nome','Anônimo')
        mensagem = request.form.get('mensagem','')
        if mensagem:
            c.execute("INSERT INTO recados (nome, mensagem) VALUES (?,?)", (nome, mensagem))
            conn.commit()
        conn.close()
        return redirect('/mural/novo')

    c.execute("SELECT nome, mensagem FROM recados ORDER BY id DESC")
    recados = c.fetchall()
    conn.close()
    return render_template('mural.html', recados=recados)

@app.route('/api/mural', methods=['GET','POST'])
def api_mural():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        d = request.get_json(silent=True) or request.form
        c.execute("INSERT INTO recados (nome, mensagem) VALUES (?,?)", (d.get('nome','Anônimo'), d.get('mensagem','')))
        conn.commit()
    c.execute("SELECT nome, mensagem FROM recados ORDER BY id DESC")
    dados = [{"nome":r[0], "mensagem":r[1]} for r in c.fetchall()]
    conn.close()
    return jsonify(dados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
