from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

ARQUIVO = "pedidos.json"

# carrega o que já tava salvo
if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        pedidos_oracao = json.load(f)
else:
    pedidos_oracao = []

def salvar():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(pedidos_oracao, f, ensure_ascii=False, indent=2)

@app.route('/oracoes', methods=['GET', 'POST'])
def oracoes():
    if request.method == 'POST':
        dados = request.get_json()
        pedidos_oracao.append(dados)
        salvar() # <- ESSA LINHA SALVA!
        print(f"novo pedido: {dados} -> SALVO!")
        return jsonify({"mensagem": "Recebido!"})
    return jsonify({"oracoes": pedidos_oracao})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

