from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)


def buscar_liturgia():
    # TENTATIVA 1: API Liturgia Diária Principal
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

            if ev_texto or p_texto:
                return {
                    "liturgia": j.get("liturgia", "Liturgia do Dia"),
                    "cor": j.get("cor", "Verde"),
                    "primeiraLeitura": p_texto,
                    "salmo": salmo_texto,
                    "evangelho": ev_texto,
                    "link": "https://liturgia.cancaonova.com/",
                    "data": j.get("data", datetime.now().strftime("%d/%m/%Y"))
                }
    except Exception as e:
        print(f"Tentativa 1 falhou: {e}")

    # TENTATIVA 2: API de Contingência (Canção Nova / CNBB via API alternativa)
    try:
        r = requests.get("https://liturgia.up.railway.app/v3/", timeout=5)
        if r.status_code == 200:
            j = r.json()
            dados = j[0] if isinstance(j, list) and len(j) > 0 else j

            p_leitura, salmo, evangelho = "", "", ""
            for item in dados.get("leituras", []):
                tipo = str(item.get("tipo", "")).lower()
                ref = item.get("referencia", "")
                txt = item.get("texto", "")
                if "primeira" in tipo or "1" in tipo:
                    p_leitura = f"({ref})<br>{txt}"
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
                    "salmo": salmo,
                    "evangelho": evangelho,
                    "link": "https://liturgia.cancaonova.com/",
                    "data": dados.get("data", datetime.now().strftime("%d/%m/%Y"))
                }
    except Exception as e:
        print(f"Tentativa 2 falhou: {e}")

    # TENTATIVA 3: API Reserva de Backup
    try:
        r = requests.get("https://cnbb-liturgia-api.vercel.app/api/hoje", timeout=5)
        if r.status_code == 200:
            data_backup = r.json()
            return {
                "liturgia": data_backup.get("liturgia", "Liturgia do Dia"),
                "cor": data_backup.get("cor", "Verde"),
                "primeiraLeitura": data_backup.get("primeiraLeitura", ""),
                "salmo": data_backup.get("salmo", ""),
                "evangelho": data_backup.get("evangelho", ""),
                "link": "https://liturgia.cancaonova.com/",
                "data": datetime.now().strftime("%d/%m/%Y")
            }
    except Exception as e:
        print(f"Tentativa 3 falhou: {e}")

    # RESPOSTA DE SEGURANÇA COM BOTÃO DE RECARGA
    return {
        "liturgia": "Liturgia do Dia",
        "cor": "Verde",
        "primeiraLeitura": "",
        "salmo": "",
        "evangelho": "O servidor externo da liturgia está passando por uma oscilação no momento. Você pode tentar recarregar ou acessar diretamente pelo site oficial.",
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
body { margin:0; font-family: Arial, sans-serif; background:#fef8f0; padding:20px; }
.card { background:white; border-radius:12px; padding:20px; max-width:650px; margin:20px auto; box-shadow:0 2px 8px rgba(0,0,0,0.1); }
.secao { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px; }
.secao h3 { color: #880000; margin-bottom: 5px; }
.badge-cor { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; background: #e0e0e0; }
.btn-reload { background: #880000; color: white; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; margin-top: 10px; }
</style>
</head>
<body>
<div class="card">
  <button onclick="history.back()" style="background:#880000;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer">← Voltar</button>
  <h2>Liturgia <span id="dataHoje"></span></h2>
  <div id="conteudoLiturgia">Carregando liturgia do dia...</div>
</div>

<script>
async function carregarLiturgia(){
  const el = document.getElementById('conteudoLiturgia');
  try {
    const res = await fetch('/api/liturgia?t=' + new Date().getTime());
    const data = await res.json();

    document.getElementById('dataHoje').innerText = data.data ? `- ${data.data}` : '';

    let html = `<p><b>${data.liturgia}</b> <span class="badge-cor">Cor: ${data.cor}</span></p><hr>`;

    if (data.primeiraLeitura) {
      html += `<div class="secao"><h3>📖 1ª Leitura</h3><p>${data.primeiraLeitura}</p></div>`;
    }

    if (data.salmo) {
      html += `<div class="secao"><h3>🎵 Salmo Responsorial</h3><p>${data.salmo}</p></div>`;
    }

    if (data.evangelho) {
      html += `<div class="secao"><h3>✝️ Evangelho</h3><p>${data.evangelho}</p></div>`;
    }

    html += `<p><a href="${data.link}" target="_blank" style="color:#880000; font-weight:bold;">👉 Ver no site oficial da Canção Nova / CNBB</a></p>`;
    html += `<button class="btn-reload" onclick="carregarLiturgia()">🔄 Tentar Recarregar Liturgia</button>`;

    el.innerHTML = html;
  } catch(e) {
    el.innerHTML = '<p style="color:red">Erro no carregamento: ' + e + '</p><button class="btn-reload" onclick="carregarLiturgia()">Tentar Novamente</button>';
  }
}

carregarLiturgia();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return HTML


@app.route("/api/liturgia")
def api_liturgia():
    return jsonify(buscar_liturgia())


if __name__ == "__main__":
    app.run(debug=True)