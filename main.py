from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

ARQUIVO = "pedidos.json"

if os.path.exists(ARQUIVO):
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            pedidos_oracao = json.load(f)
    except:
        pedidos_oracao = []
else:
    pedidos_oracao = []

def salvar():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(pedidos_oracao, f, ensure_ascii=False, indent=2)

HTML_BONITO = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>App Igreja - Pedidos de Oração</title>
<style>
body { font-family: Arial; background: #f0f2f5; margin:0; padding:20px; }
.container { max-width:500px; margin:auto; background:white; padding:25px; border-radius:15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
h1 { text-align:center; color:#2c3e50; }
input, textarea { width:100%; padding:12px; margin:8px 0; border:1px solid #ddd; border-radius:8px; box-sizing:border-box; }
button { width:100%; padding:13px; background:#27ae60; color:white; border:none; border-radius:8px; font-size:16px; font-weight:bold; }
button:hover { background:#219150; }
.pedido { background:#f9f9f9; padding:12px; margin-top:10px; border-left:4px solid #27ae60; border-radius:5px; }
.nome { font-weight:bold; color:#2c3e50; }
</style>
</head>
<body>
<div class="container">
<h1>🙏 Pedidos de Oração</h1>
<p style="text-align:center; color:#666;">Igreja - Deixe seu pedido</p>
<input id="nome" placeholder="Seu nome: Ana Leide...">
<textarea id="pedido" placeholder="Seu pedido: minha familia..."></textarea>
<button onclick="enviar()">Enviar Pedido 🙏</button>
<div id="lista"></div>
</div>
<script>
async function carregar(){
  let r = await fetch('/oracao');
  let d = await r.json();
  let html = "<h3 style='margin-top:25px;'>Pedidos:</h3>";
  d.oracoes.slice().reverse().forEach(p => {
    html += `<div class='pedido'><div class='nome'>${p.nome || 'Anônimo'}</div><div>${p.pedido || ''}</div></div>`;
  });
  document.getElementById('lista').innerHTML = html;
}
async function enviar(){
  let nome = document.getElementById('nome').value;
  let pedido = document.getElementById('pedido').value;
  if(!pedido){ alert('Escreva seu pedido!'); return; }
  await fetch('/oracao', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({nome, pedido})});
  document.getElementById('pedido').value='';
  alert('Pedido enviado! Deus abençoe!');
  carregar();
}
carregar();
</script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def inicio():
    return HTML_BONITO

@app.route('/oracao', methods=['GET', 'POST'])
def oracao():
    global pedidos_oracao
    if request.method == 'POST':
        dados = request.get_json()
        if dados:
            pedidos_oracao.append(dados)
            salvar()
        return jsonify({"mensagem": "Recebido! Deus abencoe!"})
    return jsonify({"oracoes": pedidos_oracao})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
