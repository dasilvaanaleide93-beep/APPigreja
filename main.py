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
.banner{width:100%;height:200px;display:block;object-fit:cover;object-position:center 38%;background:#fff}
.pag{display:none;padding:20px}
.pag.ativa{display:block}
#home.ativa{display:block;text-align:center;padding:20px 10px}
.icones{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:15px}
.icone{background:white;border-radius:15px;padding:18px;box-shadow:0 2px 5px #ccc;font-size:14px}
.icone b{display:block;font-size:36px;margin-bottom:5px}
.topo{ background:#8B0000;color:white;padding:10px;text-align:center;font-size:14px}
.topo button{background:none;border:none;color:white;font-size:16px}
input,textarea{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #ccc;box-sizing:border-box}
button.enviar{background:#8B0000;color:white;padding:12px;width:100%;border:none;border-radius:8px;font-size:16px}
</style>
</head>
<body>
<img class="banner" src="https://raw.githubusercontent.com/dasilvaanaleide93-beep/APPIgreja/main/santa%20terezinha.webp">

<div id="home" class="pag ativa">
<h2>Bem-vindo à Paróquia Santa Teresinha 🌹</h2>
<p>Escolha uma opção abaixo:</p>
<div class="icones">
<div class="icone" onclick="abrir('oracao')"><b>🙏</b>Oração</div>
<div class="icone" onclick="abrir('liturgia')"><b>📖</b>Liturgia</div>
<div class="icone" onclick="abrir('doacoes')"><b>❤️</b>Doações</div>
<div class="icone" onclick="abrir('mural')"><b>💬</b>Mural</div>
</div>
</div>

<div id="oracao" class="pag">
<div class="topo"><button onclick="abrir('home')">← Voltar ao Início</button></div>
<h3>Pedido de Oração 🙏</h3>
<input id="nome" placeholder="Seu nome">
<textarea id="pedido" placeholder="Digite sua oração..."></textarea>
<button class="enviar" onclick="enviar()">Enviar Pedido</button>
</div>

<div id="liturgia" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar</button></div><h3>Liturgia Diária 📖</h3><p>Em breve...</p></div>
<div id="doacoes" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar</button></div><h3>Doações ❤️</h3><p>Em breve...</p></div>
<div id="mural" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar</button></div><h3>Mural 💬</h3><p>Em breve...</p></div>

<script>
function abrir(id){
 document.querySelectorAll('.pag').forEach(p=>p.classList.remove('ativa'));
 document.getElementById(id).classList.add('ativa');
 window.scrollTo(0,0);
}
function enviar(){alert('Pedido enviado com fé! 🙏'); document.getElementById('pedido').value='';}
</script>
</body>
</html>
"""
@app.route("/")
def home(): return HTML
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)
