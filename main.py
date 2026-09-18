from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

ARQUIVO = "pedidos.json"

if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        pedidos_oracao = json.load(f)
else:
    pedidos_oracao = []

def salvar():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(pedidos_oracao, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET'])
def inicio():
    return "App Igreja no ar! Deus abencoe 🙏 Acesse /oracao"

@app.route('/oracao', methods=['GET', 'POST'])
def oracao():
    if request.method == 'POST':
        dados = request.get_json()
        pedidos_oracao.append(dados)
        salvar()
        print(f"novo pedido: {dados}")
        return jsonify({"mensagem": "Recebido!"})
    return jsonify({"oracoes": pedidos_oracao})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
