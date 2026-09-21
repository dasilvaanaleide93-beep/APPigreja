import os, sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# SÓ ESSES DOIS PODEM POSTAR
USUARIOS = {
    "padre": "padre123",
    "elisangela": "elis123"
}

DB = "/tmp/mural.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS recados (id INTEGER PRIMARY KEY, autor TEXT, texto TEXT)")
    conn.close()
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mural")
def mural():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT autor, texto FROM recados ORDER BY id DESC")
    msgs = [{"autor": a, "texto": t} for a, t in cur.fetchall()]
    conn.close()
    return render_template("mural.html", mensagens=msgs)

@app.route("/mural/novo", methods=["POST"])
def novo():
    login = request.form.get("login","").lower().strip()
    senha = request.form.get("senha","")
    if login not in USUARIOS or USUARIOS[login]!= senha:
        return "Acesso negado! So Padre e Elisangela podem postar.", 403
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO recados (autor, texto) VALUES (?,?)", (login, request.form.get("texto")))
    conn.commit()
    conn.close()
    return redirect("/mural")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)