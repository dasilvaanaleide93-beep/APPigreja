from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)


def buscar_liturgia():
    # Tentativa 1: API Liturgia Diária Principal
    try:
        r = requests.get("https://liturgia.up.railway.app/", timeout=5)
        if r.status_code == 200:
            j = r.json()

            p_leitura = j.get("primeiraLeitura", {})
            p_texto = f"({p_leitura.get('referencia', '')})<br>{p_leitura.get('texto', '')}" if isinstance(p_leitura,
                                                                                                           dict) and p_leitura.get(
                'texto') else ""

            salmo_data = j.get("salmo", {})
            refrao = salmo_data.get("refrao", "") if isinstance(salmo_data, dict) else ""
            refrao_str = f"<p><b>Refrão:</b> <i>{refrao}</i></p>" if refrao else ""
            salmo_texto = f"({salmo_data.get('referencia', '')})<br>{refrao_str}{salmo_data.get('texto', '')}" if isinstance(
                salmo_data, dict) and salmo_data.get('texto') else ""

            ev_data = j.get("evangelho", {})
            ev_texto = f"({ev_data.get('referencia', '')})<br>{ev_data.get('texto', '')}" if isinstance(ev_data,
                                                                                                        dict) and ev_data.get(
                'texto') else ""

            s_leitura = j.get("segundaLeitura", {})
            s_texto = f"({s_leitura.get('referencia', '')})<br>{s_leitura.get('texto', '')}" if isinstance(s_leitura,
                                                                                                           dict) and s_leitura.get(
                'texto') else ""

            if ev_texto or p_texto:
                return {
                    "liturgia": j.get("liturgia", "Liturgia do Dia"),
                    "cor": j.get("cor", "Verde"),
                    "primeiraLeitura": p_texto,
                    "segundaLeitura": s_texto,
                    "salmo": salmo_texto,
                    "evangelho": ev_texto,
                    "link": "https://liturgia.cancaonova.com/",
                    "data": j.get("data", datetime.now().strftime("%d/%m/%Y"))
                }
    except Exception as e:
        print(f"Tentativa 1 falhou: {e}")

    # Tentativa 2: API V3
    try:
        r = requests.get("https://liturgia.up.railway.app/v3/", timeout=5)
        if r.status_code == 200:
            j = r.json()
            dados = j[0] if isinstance(j, list) and len(j) > 0 else j

            p_leitura, s_leitura, salmo, evangelho = "", "", "", ""
            for item in dados.get("leituras", []):
                tipo = str(item.get("tipo", "")).lower()
                ref = item.get("referencia", "")
                txt = item.get("texto", "")
                if "primeira" in tipo or "1" in tipo:
                    p_leitura = f"({ref})<br>{txt}"
                elif "segunda" in tipo or "2" in tipo:
                    s_leitura = f"({ref})<br>{txt}"
                elif "salmo" in tipo:
                    refrao = f"<p><b>Refrão:</b> <i>{item.get('refrao', '')}</i></p>" if item.get('refrao') else ""
                    salmo = f"({ref})<br>{refrao}{txt}"
                elif "evangelho" in tipo:
                    evangelho = f"({ref})<br>{txt}"

            if evangelho or p_leitura:
                return {
                    "liturgia": dados.get("liturgia", "Liturgia do Dia"),
                    "cor": dados.get("cor", "Verde"),
                    "primeiraLeitura": p_leitura,
                    "segundaLeitura": s_leitura,
                    "salmo": salmo,
                    "evangelho": evangelho,
                    "link": "https://liturgia.cancaonova.com/",
                    "data": dados.get("data", datetime.now().strftime("%d/%m/%Y"))
                }
    except Exception as e:
        print(f"Tentativa 2 falhou: {e}")

    return {
        "liturgia": "Liturgia do Dia",
        "cor": "Verde",
        "primeiraLeitura": "",
        "segundaLeitura": "",
        "salmo": "",
        "evangelho": "Não foi possível carregar a liturgia no momento. Tente novamente em instantes.",
        "link": "https://liturgia.cancaonova.com/",
        "data": datetime.now().strftime("%d/%m/%Y")
    }


HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paróquia Santa Teresinha</title>
<style>
body{margin:0;font-family:Arial, sans-serif;background:#fef8f0}
.banner{width:100%;height:260px;display:block;object-fit:cover;object-position:center 30%;}
#home{text-align:center;padding:15px}
h2{font-size:18px;color:#333}
p{font-size:14px;color:#555}
.icones{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}
.icone{background:#ffffff;border:1px solid #e0c9a6;border-radius:12px;padding:16px 5px;box-shadow:0 2px 4px rgba(0,0,0,0.1);cursor:pointer}
.icone b{display:block;font-size:32px}
.icone span{display:block;margin-top:6px;font-size:14px;font-weight:bold;color:#8B0000}
.pag{display:none;padding:20px}
.pag.ativa{display:block}
.topo{background:#8B0000;padding:10px;border-radius:8px;margin-bottom:10px}
.topo button{background:none;border:none;color:white;font-size:15px;cursor:pointer}
.secao{margin-bottom:20px;border-bottom:1px solid #eee;padding-bottom:15px}
.secao h4{color:#8B0000;margin-bottom:5px;font-size:16px}
.badge-cor{display:inline-block;padding:4px 8px;border-radius:4px;font-size:12px;font-weight:bold;background:#e0e0e0}
.btn-reload{background:#8B0000;color:white;border:none;padding:8px 12px;border-radius:6px;cursor:pointer;margin-top:10px}
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

<div id="liturgia" class="pag">
  <div class="topo"><button onclick="abrir('home')">← Voltar ao Início</button></div>
  <h3>Liturgia Diária 📖 <span id="dataLiturgia"></span></h3>
  <div id="conteudoLiturgia">Carregando liturgia...</div>
</div>

<div id="doacoes" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar ao Início</button></div><h3>Doações ❤️</h3></div>
<div id="mural" class="pag"><div class="topo"><button onclick="abrir('home')">← Voltar ao Início</button></div><h3>Mural 💬</h3></div>

<script>
function abrir(id){
 document.querySelectorAll('.pag').forEach(p=>p.classList.remove('ativa'));
 document.getElementById(id).classList.add('ativa');
 window.scrollTo(0,0);
 if(id === 'liturgia'){
    carregarLiturgia();
 }
}

async function carregarLiturgia(){
  const el = document.getElementById('conteudoLiturgia');
  try {
    const res = await fetch('/api/liturgia?t=' + new Date().getTime());
    const data = await res.json();

    document.getElementById('dataLiturgia').innerText = data.data ? `- ${data.data}` : '';

    let html = `<p><b>${data.liturgia}</b> <span class="badge-cor">Cor: ${data.cor}</span></p><hr>`;

    if (data.primeiraLeitura) {
      html += `<div class="secao"><h4>📖 1ª Leitura</h4><p>${data.primeiraLeitura}</p></div>`;
    }

    if (data.salmo) {
      html += `<div class="secao"><h4>🎵 Salmo Responsorial</h4><p>${data.salmo}</p></div>`;
    }

    if (data.segundaLeitura) {
      html += `<div class="secao"><h4>📖 2ª Leitura</h4><p>${data.segundaLeitura}</p></div>`;
    }

    if (data.evangelho) {
      html += `<div class="secao"><h4>✝️ Evangelho</h4><p>${data.evangelho}</p></div>`;
    }

    html += `<p><a href="${data.link}" target="_blank" style="color:#8B0000; font-weight:bold;">👉 Ver no site oficial da Canção Nova / CNBB</a></p>`;
    html += `<button class="btn-reload" onclick="carregarLiturgia()">🔄 Recarregar Liturgia</button>`;

    el.innerHTML = html;
  } catch(e) {
    el.innerHTML = '<p style="color:red">Erro ao carregar a liturgia: ' + e + '</p><button class="btn-reload" onclick="carregarLiturgia()">Tentar Novamente</button>';
  }
}
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return HTML


@app.route("/api/liturgia")
def api_liturgia():
    return jsonify(buscar_liturgia())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)