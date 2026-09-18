from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

def carregar(arq):
    if os.path.exists(arq):
        try:
            with open(arq, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []
def salvar(arq, dados):
    with open(arq, "w", encoding="utf-8") as f: json.dump(dados, f, ensure_ascii=False, indent=2)

oracoes = carregar("pedidos.json")
recados = carregar("mural.json")
voluntarios = carregar("voluntarios.json")

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Paróquia Santa Terezinha</title>
<style>
body{font-family:Arial;background:#f5f5f5;margin:0}
.card-top{max-width:480px;margin:15px auto;background:white;border-radius:20px;overflow:hidden;box-shadow:0 4px 15px #0001}
.banner{width:100%;height:260px;object-fit:cover;object-position:top center;display:block;background:#fdf8ef}
.sec{padding:14px 15px;font-weight:bold}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;padding:15px}
.item{text-align:center;background:#fff8ec;padding:16px 5px;border-radius:18px;border:1px solid #f5e0b8}
.item p{margin:8px 0 0;font-size:13px;font-weight:bold}
.bloco{padding:12px 15px;background:white;margin-top:10px;border-radius:15px}
.pag{display:none;max-width:480px;margin:auto;padding:20px}
.pag.ativa{display:block;background:white;min-height:100vh}
.voltar{background:#8e44ad;color:white;border:none;padding:10px 15px;border-radius:20px;margin-bottom:15px}
input,textarea{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:8px;box-sizing:border-box}
.btn{background:#8e44ad;color:white;border:none;padding:13px;width:100%;border-radius:10px;font-weight:bold}
.card{background:#f9f0ff;padding:12px;margin-top:10px;border-radius:10px;border-left:4px solid #8e44ad}
</style>
</head>
<body>
<div id="home">
<div class="card-top">
<img class="banner" src="https://raw.githubusercontent.com/dasilvaanaleide93-beep/APPIgreja/main/santa.jpg" onerror="this.src='https://upload.wikimedia.org/wikipedia/commons/2/2e/Th%C3%A9r%C3%A8se_de_Lisieux.jpg'">
<div class="sec">Eventos e Atividades</div>
<div class="grid">
<div class="item" onclick="abrir('doacoes')"><div style="font-size:44px">💝</div><p>Doações</p></div>
<div class="item" onclick="abrir('oracao')"><div style="font-size:44px">🙏</div><p>Pedido de<br>Oração</p></div>
<div class="item" onclick="abrir('liturgia')"><div style="font-size:44px">📖</div><p>Liturgia<br>Diária</p></div>
</div>
<div class="bloco"><p style="font-weight:bold;margin:0 0 10px 0">Recados</p><div class="item" style="width:110px" onclick="abrir('mural')"><div style="font-size:42px">✉️</div><p>Mural</p></div></div>
<div class="bloco"><p style="font-weight:bold;margin:0 0 10px 0">Voluntários</p><div class="item" style="width:110px" onclick="abrir('vol')"><div style="font-size:42px">👥</div><p>Seja um</p></div></div>
</div>
</div>
<div id="oracao" class="pag"><button class="voltar" onclick="abrir('home')">← Voltar</button><h2>🙏 Pedido de Oração</h2><input id="nomeO" placeholder="Seu nome"><textarea id="pedO" placeholder="Seu pedido..."></textarea><button class="btn" onclick="enviarO()">Enviar</button><div id="listaO"></div></div>
<div id="doacoes" class="pag"><button class="voltar" onclick="abrir('home')">← Voltar</button><h2>💝 Doações</h2><div style="background:#e8f5e9;padding:20px;border-radius:12px;text-align:center">PIX da Paróquia aqui<br>Barra do Garças - MT</div></div>
<div id="liturgia" class="pag"><button class="voltar" onclick="abrir('home')">← Voltar</button><h2>📖 Liturgia Diária</h2><p>Que Santa Terezinha interceda por nós! 🌹</p></div>
<div id="mural" class="pag"><button class="voltar" onclick="abrir('home')">← Voltar</button><h2>📌 Mural</h2><input id="nomeM" placeholder="Seu nome"><textarea id="msgM" placeholder="Recado..."></textarea><button class="btn" onclick="enviarM()">Postar</button><div id="listaM"></div></div>
<div id="vol" class="pag"><button class="voltar" onclick="abrir('home')">← Voltar</button><h2>👥 Voluntários</h2><input id="nomeV" placeholder="Seu nome"><input id="zapV" placeholder="WhatsApp"><textarea id="areaV" placeholder="Como quer ajudar?"></textarea><button class="btn" onclick="enviarV()">Quero ser Voluntário</button><div id="listaV"></div></div>
<script>
function abrir(id){document.getElementById('home').style.display=id=='home'?'block':'none';document.querySelectorAll('.pag').forEach(p=>p.classList.remove('ativa'));if(id!='home')document.getElementById(id).classList.add('ativa');if(id=='oracao')carregarO();if(id=='mural')carregarM();if(id=='vol')carregarV();window.scrollTo(0,0);}
async function carregarO(){let r=await fetch('/oracao');let d=await r.json();let h='';d.oracoes.slice().reverse().forEach(p=>{h+=`<div class='card'><b>${p.nome||'Anônimo'}</b><br>${p.pedido||''}</div>`});document.getElementById('listaO').innerHTML=h;}
async function enviarO(){let nome=document.getElementById('nomeO').value;let pedido=document.getElementById('pedO').value;if(!pedido)return alert('Escreva!');await fetch('/oracao',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nome,pedido})});document.getElementById('pedO').value='';alert('Enviado!');carregarO();}
async function carregarM(){let r=await fetch('/mural');let d=await r.json();let h='';d.mural.slice().reverse().forEach(p=>{h+=`<div class='card'><b>${p.nome||''}</b><br>${p.msg||''}</div>`});document.getElementById('listaM').innerHTML=h;}
async function enviarM(){let nome=document.getElementById('nomeM').value;let msg=document.getElementById('msgM').value;if(!msg)return alert('Escreva!');await fetch('/mural',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nome,msg})});document.getElementById('msgM').value='';alert('Postado!');carregarM();}
async function carregarV(){let r=await fetch('/voluntarios');let d=await r.json();let h='<h3>Voluntários:</h3>';d.voluntarios.slice().reverse().forEach(p=>{h+=`<div class='card'><b>${p.nome||''}</b> - ${p.zap||''}<br>${p.area||''}</div>`});document.getElementById('listaV').innerHTML=h;}
async function enviarV(){let nome=document.getElementById('nomeV').value;let zap=document.getElementById('zapV').value;let area=document.getElementById('areaV').value;if(!nome)return alert('Nome!');await fetch('/voluntarios',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nome,zap,area})});alert('Obrigado!');carregarV();}
</script>
</body>
</html>
"""

@app.route('/')
def home(): return HTML
@app.route('/oracao', methods=['GET','POST'])
def oracao():
    global oracoes
    if request.method=='POST':
        d=request.get_json()
        if d: oracoes.append(d); salvar("pedidos.json", oracoes)
        return jsonify({"ok":True})
    return jsonify({"oracoes":oracoes})
@app.route('/mural', methods=['GET','POST'])
def mural():
    global recados
    if request.method=='POST':
        d=request.get_json()
        if d: recados.append(d); salvar("mural.json", recados)
        return jsonify({"ok":True})
    return jsonify({"mural":recados})
@app.route('/voluntarios', methods=['GET','POST'])
def vol():
    global voluntarios
    if request.method=='POST':
        d=request.get_json()
        if d: voluntarios.append(d); salvar("voluntarios.json", voluntarios)
        return jsonify({"ok":True})
    return jsonify({"voluntarios":voluntarios})

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
