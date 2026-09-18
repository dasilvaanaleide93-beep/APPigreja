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
body{margin:0;font-family:Arial,sans-serif;background:#fef8f0;color:#333}
.banner{width:100%;height:400px;display:block;object-fit:cover;object-position:center 22%;background:#fff}
#home{padding:15px;text-align:center}
.icones{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}
.icone{background:white;border-radius:12px;padding:15px 5px;box-shadow:0 2px 5px rgba(0,0,0,0.15);cursor:pointer}
.icone b{display:block;font-size:32px}
.icone span{display:block;font-size:13px;margin-top:5px;color:#8B0000;font-weight:bold}
.pag{display:none;padding:20px}
.pag.ativa{display:block}
.topo{background:#8B0000;padding:10px;border-radius:8px;margin-bottom:15px}
.topo button{background:none;border:none;color:white;font-size:15px}
input,textarea{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #ccc;box-sizing:border-box}
button.enviar{background:#8B0000;color:white;padding:12px;width:100%;border:none;border-radius:8px;font-size:16px}
h2{font-size:18px;margin:10px 0}
</style>
</head>
<body>
<img class="banner" src="https://raw.githubusercontent.com/dasilvaanaleide93-beep/APPIgreja/main/santa%20terezinha.webp">

<div id="home" class="pag ativa">
<h2>Bem-vindo à Paróquia Santa Teresinha 🌹</h2>
<p style="font-size:14px">Escolha uma opção abaixo:</p>
<div class="icones">
<div class="icone" onclick="abrir('oracao')"><b>🙏</b><span>Oração</span></div>
<div class="icone" onclick="abrir('liturgia')"><b>📖</b><span>Liturgia</span></div>
<div class="icone" onclick="abrir('doacoes')"><b>❤️</b><span>Doações</span></div>
<div class="icone" onclick="abrir('mural')"><b>💬</b><span>Mural</span></div>
</div>
</div>

<div id="oracao" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar ao Início</button></div><h3>Pedido de Oração 🙏</h3><input placeholder="Seu nome"><textarea placeholder="Digite sua oração..."></textarea><button class="enviar">Enviar Pedido</button></div>
<div id="liturgia" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar</button></div><h3>Liturgia 📖</h3><p>Em breve...</p></div>
<div id="doacoes" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar</button></div><h3>Doações ❤️</h3><p>Em breve...</p></div>
<div id="mural" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar</button></div><h3>Mural 💬</h3><p>Em breve...</p></div>

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
