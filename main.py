import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DB = "/tmp/mural.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS recados (id INTEGER PRIMARY KEY, nome TEXT, mensagem TEXT)')
    conn.commit()
    conn.close()
init_db()

@app.route('/')
def home():
    return '<h1>App Igreja Online</h1><a href="/mural/novo">Ir pro Mural</a>'

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
        return '''
        <h3>Mensagem enviada!</h3>
        <a href="/mural/novo">Voltar pro mural</a>
        <script>setTimeout(()=>window.location="/mural/novo", 1500)</script>
        '''

    c.execute("SELECT nome, mensagem FROM recados ORDER BY id DESC")
    recados = c.fetchall()
    conn.close()

    lista = "".join([f"<p><b>{r[0]}:</b> {r[1]}</p>" for r in recados])

    return f'''
    <html><body>
    <h2>Mural da Igreja</h2>
    <form method="POST">
        <input name="nome" placeholder="Seu nome"><br><br>
        <textarea name="mensagem" placeholder="Sua mensagem"></textarea><br><br>
        <button type="submit">Enviar</button>
    </form>
    <hr>
    <h3>Mensagens:</h3>
    {lista}
    </body></html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
