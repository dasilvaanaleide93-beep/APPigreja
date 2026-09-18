from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)
ARQ = "pedidos.json"

def carregar():
    if not os.path.exists(ARQ):
        return {"oracao":[],"mural":[],"voluntarios":[]}
    with open(ARQ,"r",encoding="utf-8") as f:
        return json.load(f)

def salvar(d):
    with open(ARQ,"w",encoding="utf-8") as f:
        json.dump(d,f,ensure_ascii=False,indent=2)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{margin:0;font-family:Arial;background:#fff7f8}
.banner{width:100%;height:auto;display:block;object-fit:contain;background:#fff}
.menu{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;padding:15px}
.btn{width:110px;background:white;border-radius:12px;padding:10px;text-align:center;box-shadow:0 2px 6px #0002;cursor:pointer}
.pag{display:none;padding:15px}.ativa{display:block}
.card{background:white;padding:12px;margin:8px 0;border-radius:10px;box-shadow:0 1px 4px #0001}
input,textarea{width:100%;padding:10px;margin:5px 0;border-radius:8px;border:1px solid #ccc;box-sizing:border-box}
button.env{background:#c0392b;color:white;border:none;padding:12px;border-radius:8px;width:100%;font-size:16px}
</style>
</head>
<body>
<img class="banner" src="https://raw.githubusercontent.com/dasilvaanaleide93-beep/APPIgreja/main/santa%20terezinha.webp">

<div class="menu">
<div class="btn" style="width:110px" onclick="abrir('oracao')"><div style="font-size:42px">🙏</div><p>Oracao</p></div>
<div class="btn" style="width:110px" onclick="abrir('liturgia')"><div style="font-size:42px">📖</div><p>Liturgia Diaria</p></div>
<div class="btn" style="width:110px" onclick="abrir('doa')"><div style="font-size:42px">❤️</div><p>Doacoes</p></div>
<div class="btn" style="width:110px" onclick="abrir('mural')"><div style="font-size:42px">💬</div><p>Mural</p></div>
<div class="btn" style="width:110px" onclick="abrir('vol')"><div style="font-size:42px">🙋</div><p>Seja um</p></div>
</div>

<div id="oracao" class="pag ativa"><h2>Pedido de Oracao</h2><input id="nomeO" placeholder="Seu nome"><textarea id="pedO" placeholder="Seu pedido..."></textarea><button class="env" onclick="envO()">Enviar Pedido</button><div id="listaO"></div></div>
<div id="doa" class="pag"><h2>Doacoes</h2><div style="background:#e8f5e9;padding:20px;border-radius:12px;text-align:center">PIX da Paroquia<br><b>Barra do Garcas</b></div></div>
<div id="liturgia" class="pag"><h2>Liturgia Diaria</h2><p>Que Santa Terezinha interceda por nos! 🌹</p></div>
<div id="mural" class="pag"><h2>Mural</h2><input id="nomeM" placeholder="Seu nome"><textarea id="msgM" placeholder="Recado..."></textarea><button class="env" onclick="envM()">Enviar</button><div id="listaM"></div></div>
<div id="vol" class="pag"><h2>Voluntarios</h2><input id="nomeV" placeholder="Seu nome"><input id="zapV" placeholder="WhatsApp"><textarea id="areaV" placeholder="Como quer ajudar?"></textarea><button class="env" onclick="envV()">Quero ser voluntario</button><div id="listaV"></div></div>

<script>
function abrir(id){document.querySelectorAll('.pag').forEach(p=>p.classList.remove('ativa'));if(id!='home')document.getElementById(id).classList.add('ativa');if(id=='oracao')carO();if(id=='mural')carM();if(id=='vol')carV();}
async function carO(){let r=await fetch('/oracao');let d=await r.json();let h='';d.oracao.slice().reverse().forEach(p=>{h+=`<div class='card'><b>${p.nome||'Anonimo'}</b><br>${p.pedido||''}</div>`});document.getElementById('listaO').innerHTML=h;}
async function envO(){let nome=document.getElementById('nomeO').value;let pedido=document.getElementById('pedO').value;if(!pedido)return alert('Escreva!');await fetch('/oracao',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nome,pedido})});document.getElementById('pedO').value='';carO();alert('Enviado! 🙏')}
async function carM(){let r=await fetch('/mural');let d=await r.json();let h='';d.mural.slice().reverse().forEach(p=>{h+=`<div class='card'><b>${p.nome||''}</b><br>${p.msg||''}</div>`});document.getElementById('listaM').innerHTML=h;}
async function envM(){let nome=document.getElementById('nomeM').value;let msg=document.getElementById('msgM').value;if(!msg)return alert('Escreva!');await fetch('/mural',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nome,msg})});document.getElementById('msgM').value='';carM();}
async function carV(){let r=await fetch('/voluntarios');let d=await r.json();let h='<h3>Voluntarios:</h3>';d.voluntarios.slice().reverse().forEach(p=>{h+=`<div class='card'><b>${p.nome||''}</b> - ${p.zap||''}<br>${p.area||''}</div>`});document.getElementById('listaV').innerHTML=h;}
async function envV(){let nome=document.getElementById('nomeV').value;let zap=document.getElementById('zapV').value;let area=document.getElementById('areaV').value;if(!nome)return alert('Nome!');await fetch('/vol',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nome,zap,area})});carV();alert('Obrigado!')}
carO();
</script>
</body>
</html>
"""

@app.route("/oracao", methods=["GET","POST"])
def oracao():
    d=carregar()
    if request.method=="POST":
        j=request.get_json()
        d["oracao"].append(j); salvar(d); return jsonify({"ok":True})
    return jsonify({"oracao":d["oracao"]})

@app.route("/mural", methods=["GET","POST"])
def mural():
    d=carregar()
    if request.method=="POST":
        j=request.get_json()
        d["mural"].append(j); salvar(d); return jsonify({"ok":True})
    return jsonify({"mural":d["mural"]})

@app.route("/voluntarios")
def get_vol():
    d=carregar(); return jsonify({"voluntarios":d["voluntarios"]})

@app.route("/vol", methods=["POST"])
def vol():
    d=carregar(); j=request.get_json(); d["voluntarios"].append(j); salvar(d); return jsonify({"ok":True})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
