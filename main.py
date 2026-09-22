import os, sqlite3
from flask import Flask, request
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
@app.route('/')
def home():
 return '<h1>App Igreja</h1><a href="/mural/novo" style="font-size:22px">Ir pro Mural Grande</a>'
@app.route('/mural/novo', methods=['GET','POST'])
def mural():
 conn = sqlite3.connect(DB); c = conn.cursor()
 if request.method == 'POST':
  c.execute("INSERT INTO recados (nome, mensagem) VALUES (?,?)", (request.form.get('nome','Anonimo'), request.form.get('mensagem','')))
  conn.commit(); conn.close()
  return '<script>window.location="/mural/novo"</script>'
 c.execute("SELECT nome, mensagem FROM recados ORDER BY id DESC")
 recados = c.fetchall(); conn.close()
 lista = "".join([f'<div style="background:#f0f0ff;padding:15px;margin:10px 0;border-radius:10px;font-size:22px"><b>{r[0]}:</b> {r[1]}</div>' for r in recados])
 return f'<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body style="font-family:Arial;padding:20px;max-width:600px;margin:auto"><h1 style="font-size:32px;text-align:center">🙏 Mural da Igreja</h1><form method="POST" style="background:white;padding:20px;border-radius:15px;box-shadow:0 2px 10px #0002"><input name="nome" placeholder="Seu nome" style="width:100%;padding:20px;font-size:22px;border-radius:10px"><br><br><textarea name="mensagem" placeholder="Sua mensagem" style="width:100%;padding:20px;font-size:22px;border-radius:10px;height:120px"></textarea><br><br><button style="width:100%;padding:20px;font-size:26px;background:#4a47e0;color:white;border:none;border-radius:12px">ENVIAR</button></form><hr>{lista}</body></html>'
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
