import os, sqlite3
from flask import Flask, render_template, request
from flask_cors import CORS

# AQUI VOLTA A LER SUA PASTA BONITA Modelos
app = Flask(__name__, template_folder='Modelos', static_folder='estática')
CORS(app)
DB = "/tmp/mural.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS recados (id INTEGER PRIMARY KEY, nome TEXT, mensagem TEXT)')
    conn.commit(); conn.close()
init_db()

@app.route('/')
def home():
    try:
        # tenta abrir sua pagina bonita original
        return render_template('index.html')
    except:
        return '<h1>App Igreja Online</h1><a href="/mural/novo">Ir pro Mural</a>'

@app.route('/mural/novo', methods=['GET', 'POST'])
def mural_novo():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        nome = request.form.get('nome','Anônimo')
        mensagem = request.form.get('mensagem','')
        if mensagem:
            c.execute("INSERT INTO recados (nome, mensagem) VALUES (?,?)", (nome, mensagem))
            conn.commit()
        conn.close()
        return '<h3 style="font-family:Arial;text-align:center;padding:30px">Enviado! 🙏</h3><a href="/mural/novo" style="display:block;text-align:center;font-size:20px">Voltar pro mural</a><script>setTimeout(()=>window.location="/mural/novo",1200)</script>'

    c.execute("SELECT nome, mensagem FROM recados ORDER BY id DESC")
    recados = c.fetchall()
    conn.close()
    lista = "".join([f'<div style="background:#f0f0ff;padding:12px;border-radius:10px;margin-top:10px;font-size:18px"><b>{r[0]}:</b> {r[1]}</div>' for r in recados])

    # Se tiver um mural.html na sua pasta Modelos, ele usa. Se não tiver, usa esse bonito grande
    try:
        return render_template('mural.html', recados=recados)
    except:
        return f'''<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
        <style>body{{font-family:Arial;padding:15px;background:#eef0ff;margin:0}}.caixa{{background:white;padding:20px;border-radius:15px;max-width:500px;margin:auto;box-shadow:0 4px 15px #0002}}input,textarea{{width:100%;padding:18px;font-size:20px;border-radius:12px;border:1px solid #ccc;box-sizing:border-box}}button{{width:100%;padding:18px;font-size:22px;background:#4a47e0;color:white;border:none;border-radius:12px;font-weight:bold}}</style>
        </head><body><div class="caixa"><h2 style="text-align:center">🙏 Mural da Igreja</h2>
        <form method="POST"><input name="nome" placeholder="Seu nome"><br><br><textarea name="mensagem" rows="4" placeholder="Sua mensagem"></textarea><br><br><button type="submit">ENVIAR</button></form><hr><h3>Mensagens:</h3>{lista}</div></body></html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
