import os, sqlite3
from flask import Flask, request, render_template, redirect
from flask_cors import CORS

app = Flask(__name__, template_folder='Modelos', static_folder='estática')
# se sua pasta for com letra minúscula, tenta assim também
try:
    # tenta achar a pasta certa
    if not os.path.exists('Modelos'):
        app.template_folder = 'modelos'
    if not os.path.exists('estática'):
        app.static_folder = 'estatica'
except:
    pass

CORS(app)
DB = "/tmp/mural.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS recados (id INTEGER PRIMARY KEY, nome TEXT, mensagem TEXT)')
    conn.commit(); conn.close()
init_db()

# PÁGINA INICIAL - Já vai direto pra página da Santa Teresinha
@app.route('/')
def home():
    # tenta abrir seu arquivo original se existir
    try:
        return render_template('index.html')
    except:
        # Se não achar, mostra uma página bonita da Santa Teresinha já com os menus
        return '''
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body{font-family:Arial; margin:0; background:#fff8f0; text-align:center}
               .banner{background: linear-gradient(#ffb88c, #ff8a5b); padding:20px; color:white}
               .banner img{width:150px; height:150px; border-radius:50%; border:4px solid white; object-fit:cover}
               .menu{display:grid; grid-template-columns:1fr 1fr; gap:15px; padding:20px; max-width:500px; margin:auto}
               .btn{background:white; padding:20px; border-radius:15px; text-decoration:none; color:#333; font-size:20px; font-weight:bold; box-shadow:0 2px 8px #0002; display:block}
               .btn span{font-size:40px; display:block}
            </style>
        </head>
        <body>
            <div class="banner">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Sainte_Th%C3%A9r%C3%A8se_de_l%27Enfant_J%C3%A9sus.jpg/400px-Sainte_Th%C3%A9r%C3%A8se_de_l%27Enfant_J%C3%A9sus.jpg">
                <h1>Santa Teresinha</h1>
                <p>Paróquia Santa Teresinha - App da Igreja</p>
            </div>
            <div class="menu">
                <a class="btn" href="/mural/novo"><span>🙏</span>Mural GRANDE</a>
                <a class="btn" href="/mural/novo"><span>💌</span>Deixar Recado</a>
                <a class="btn" href="/pedidos"><span>🕯️</span>Pedidos</a>
                <a class="btn" href="/mural/novo"><span>📖</span>Orações</a>
            </div>
        </body>
        </html>
        '''

# MURAL COM LETRA GIGANTE
@app.route('/mural/novo', methods=['GET','POST'])
def mural():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO recados (nome, mensagem) VALUES (?,?)", (request.form.get('nome','Anônimo'), request.form.get('mensagem','')))
        conn.commit(); conn.close()
        return redirect('/mural/novo')
    c.execute("SELECT nome, mensagem FROM recados ORDER BY id DESC")
    recados = c.fetchall(); conn.close()
    lista = "".join([f'<div style="background:white;padding:18px;margin:12px 0;border-radius:12px;font-size:24px;text-align:left;box-shadow:0 2px 5px #0001"><b style="color:#4a47e0">{r[0]}:</b><br>{r[1]}</div>' for r in recados])
    return f'''
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="font-family:Arial;background:#f5f5ff;padding:15px;max-width:650px;margin:auto">
        <a href="/" style="font-size:20px;text-decoration:none">⬅️ Voltar pra Santa Teresinha</a>
        <h1 style="font-size:36px;text-align:center">🙏 Mural da Igreja</h1>
        <form method="POST" style="background:white;padding:22px;border-radius:18px;box-shadow:0 3px 12px #0002">
            <input name="nome" placeholder="Seu nome" style="width:100%;padding:22px;font-size:24px;border-radius:12px;border:2px solid #ddd;box-sizing:border-box">
            <br><br>
            <textarea name="mensagem" placeholder="Escreva sua mensagem, oração..." style="width:100%;padding:22px;font-size:24px;border-radius:12px;border:2px solid #ddd;height:130px;box-sizing:border-box"></textarea>
            <br><br>
            <button style="width:100%;padding:22px;font-size:28px;background:#4a47e0;color:white;border:none;border-radius:14px;font-weight:bold">ENVIAR 🙏</button>
        </form>
        <div style="margin-top:20px">{lista}</div>
    </body></html>
    '''

@app.route('/pedidos')
def pedidos():
    return redirect('/mural/novo')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
