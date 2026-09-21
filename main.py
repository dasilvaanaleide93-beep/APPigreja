import json, os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

ARQUIVO_MURAL = "mural.json"

# AQUI VOCÊS 3 - pode trocar as senhas depois
USUARIOS = {
    "padre": "padre123",
    "elisangela": "elis123",
    "ana": "teste123" # esse é você, pode colocar seu nome
}

def carregar():
    if not os.path.exists(ARQUIVO_MURAL):
        return []
    with open(ARQUIVO_MURAL, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar(lista):
    with open(ARQUIVO_MURAL, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mural")
def mural():
    mensagens = carregar()
    return render_template("mural.html", mensagens=mensagens)

@app.route("/mural/novo", methods=["POST"])
def novo():
    login = request.form.get("login").lower().strip()
    senha = request.form.get("senha")

    # verifica se o login existe e a senha bate
    if login not in USUARIOS or USUARIOS[login]!= senha:
        return "Login ou senha errados! Fale com a Ana.", 403

    mensagens = carregar()
    mensagens.insert(0, {
        "autor": login,
        "texto": request.form.get("texto")
    })
    salvar(mensagens)
    return redirect("/mural")

if __name__ == "__main__":
    app.run(debug=True)