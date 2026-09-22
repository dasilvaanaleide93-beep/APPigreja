import os, sqlite3
from flask import Flask, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DB = "/tmp/mural.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS recados (id INTEGER PRIMARY KEY, nome TEXT, mensagem TEXT)')
    conn.commit(); conn.close()
init_db()

# IMAGEM DA SANTA - tenta da sua pasta, se não tiver usa da internet
IMG_SANTA = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Sainte_Th%C3%A9r%C3%A8se_de_l%27Enfant_J%C3%A9sus.jpg/400px-Sainte_Th%C3%A9r%C3%A8se_de_l%27Enfant_J%C3%A9sus.jpg"

@app.route('/')
def home():
    return f'''
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{{font-family:Arial;margin:0;background:#fff8f0;text-align:center}}
       .banner{{background:linear-gradient(#ff9a5c,#ff6a2d);padding:30px 20px;color:white}}
       .banner img{{width:160px;height:160px;border-radius:50%;border:5px solid white;object-fit:cover;background:white}}
       .menu{{display:grid;grid-template-columns:1fr 1fr;gap:15px;padding:20px;max-width:500px;margin:auto}}
       .btn{{background:white;padding:22px 10px;border-radius:18px;text-decoration:none;color:#333;font-size:19px;font-weight:bold;box-shadow:0 3px 10px #0002;display:block}}
       .btn span{{font-size:42px;display:block;margin-bottom:5px}}
    </style></head><body>
        <div class="banner">
            <img src="{IMG_SANTA}" onerror="this.src='https://i.ibb.co/3m2cP3Y/santa.jpg'">
            <h1 style="margin:15px 0 5px">Santa Teresinha</h1>
            <p style="margin:0;opacity:0.9">Paróquia Santa Teresinha - App da Igreja</p>
        </div>
        <div class="menu">
            <a class="btn" href="/mural/novo"><span>💌</span>Mural de Recado</a>
            <a class="btn" href="/oracoes"><span>📖</span>Orações</a>
            <a class="btn" href="/doacoes"><span>❤️</span>Doações</a>
            <a class="btn" href="/liturgia"><span>✝️</span>Liturgia</a>
        </div>
    </body></html>
    '''

@app.route('/mural/novo', methods=['GET','POST'])
def mural():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO recados (nome, mensagem) VALUES (?,?)", (request.form.get('nome','Anônimo'), request.form.get('mensagem','')))
        conn.commit(); conn.close()
        return redirect('/mural/novo')
    c.execute("SELECT nome, mensagem FROM recados ORDER BY id DESC")
    recados = c.fetchall(); conn.close()
    lista = "".join([f'<div style="background:white;padding:18px;margin:12px 0;border-radius:12px;font-size:24px;text-align:left;box-shadow:0 2px 5px #0001"><b style="color:#e65a2d">{r[0]}:</b><br>{r[1]}</div>' for r in recados])
    return f'<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body style="font-family:Arial;background:#fff8f0;padding:15px;max-width:650px;margin:auto"><a href="/" style="font-size:20px;text-decoration:none">⬅️ Voltar</a><h1 style="font-size:34px;text-align:center">💌 Mural de Recado</h1><form method="POST" style="background:white;padding:22px;border-radius:18px;box-shadow:0 3px 12px #0002"><input name="nome" placeholder="Seu nome" style="width:100%;padding:22px;font-size:24px;border-radius:12px;border:2px solid #ddd;box-sizing:border-box"><br><br><textarea name="mensagem" placeholder="Deixe sua mensagem..." style="width:100%;padding:22px;font-size:24px;border-radius:12px;border:2px solid #ddd;height:130px;box-sizing:border-box"></textarea><br><br><button style="width:100%;padding:22px;font-size:28px;background:#ff6a2d;color:white;border:none;border-radius:14px;font-weight:bold">ENVIAR</button></form><div style="margin-top:20px">{lista}</div></body></html>'

@app.route('/oracoes')
def oracoes():
    return '<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body style="font-family:Arial;padding:20px;max-width:600px;margin:auto"><a href="/">⬅️ Voltar</a><h1>📖 Orações</h1><div style="background:white;padding:20px;border-radius:12px;font-size:22px;line-height:1.6"><h3>Oração a Santa Teresinha</h3><p>Ó Santa Teresinha, que prometestes fazer cair uma chuva de rosas, olhai para nossas necessidades e intercedei por nós.<br><br>Amém.</p></div></body></html>'

@app.route('/doacoes')
def doacoes():
    return '<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body style="font-family:Arial;padding:20px;max-width:600px;margin:auto"><a href="/">⬅️ Voltar</a><h1>❤️ Doações</h1><div style="background:white;padding:20px;border-radius:12px;font-size:22px"><p>Ajude nossa paróquia!</p><p><b>PIX:</b> (coloque seu PIX aqui)<br><br>Que Deus abençoe sua generosidade!</p></div></body></html>'

@app.route('/liturgia')
def liturgia():
    return '<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body style="font-family:Arial;padding:20px;max-width:600px;margin:auto"><a href="/">⬅️ Voltar</a><h1>✝️ Liturgia Diária</h1><div style="background:white;padding:20px;border-radius:12px;font-size:22px"><p><b>Evangelho de Hoje</b></p><p>Confira a liturgia completa em: <a href="https://liturgiadiaria.cnbb.org.br" target="_blank">liturgiadiaria.cnbb.org.br</a></p><p style="margin-top:20px;font-style:italic">"Deixai vir a mim as criancinhas, pois delas é o Reino dos Céus"</p></div></body></html>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
