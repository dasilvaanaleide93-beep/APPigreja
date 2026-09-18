from flask import Flask
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paróquia Santa Teresinha</title>
<style>
body{margin:0;font-family:Arial;background:#fef8f0}
.banner{width:100%;height:260px;display:block;object-fit:cover;object-position:center 30%;}
#home{text-align:center;padding:15px}
h2{font-size:18px;color:#333}
p{font-size:14px;color:#555}
.icones{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}
.icone{background:#ffffff;border:1px solid #e0c9a6;border-radius:12px;padding:16px 5px;box-shadow:0 2px 4px rgba(0,0,0,0.1)}
.icone b{display:block;font-size:32px}
.icone span{display:block;margin-top:6px;font-size:14px;font-weight:bold;color:#8B0000}
.pag{display:none;padding:20px}
.pag.ativa{display:block}
.topo{background:#8B0000;padding:10px;border-radius:8px;margin-bottom:10px}
.topo button{background:none;border:none;color:white;font-size:15px}
</style>
</head>
<body>
<img class="banner" src="https://raw.githubusercontent.com/dasilvaanaleide93-beep/APPIgreja/main/santa%20terezinha.webp">

<div id="home" class="pag ativa">
<h2>Bem-vindo à Paróquia Santa Teresinha 🌹</h2>
<p>Escolha uma opção abaixo:</p>
<div class="icones">
<div class="icone" onclick="abrir('oracao')"><b>🙏</b><span>Oração</span></div>
<div class="icone" onclick="abrir('liturgia')"><b>📖</b><span>Liturgia</span></div>
<div class="icone" onclick="abrir('doacoes')"><b>❤️</b><span>Doações</span></div>
<div class="icone" onclick="abrir('mural')"><b>💬</b><span>Mural</span></div>
</div>
</div>

<div id="oracao" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar ao Início</button></div><h3>Oração 🙏</h3></div>
<div id="liturgia" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar</button></div><h3>Liturgia 📖</h3></div>
<div id="doacoes" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar</button></div><h3>Doações ❤️</h3></div>
<div id="mural" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar</button></div><h3>Mural 💬</h3></div>

<script>
function abrir(id){
 document.querySelectorAll('.pag').forEach(p=>p.classList.remove('ativa'));
 document.getElementById(id).classList.add('ativa');
 window.scrollTo(0,0);
}
</script>
</body>
</html>
"""
@app.route("/")
def home(): return HTML
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)
