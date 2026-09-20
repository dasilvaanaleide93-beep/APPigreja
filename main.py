from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)


# Habilita cabeçalho de CORS manualmente para evitar bloqueio no navegador
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


def formatar_leitura(item):
    if not isinstance(item, dict):
        return ""
    ref = item.get("referencia", "")
    ref_str = f" ({ref})" if ref else ""
    refrao = item.get("refrao") or ""
    refrao_str = f"<p><b>Refrão:</b> <i>{refrao}</i></p>" if refrao else ""
    texto = item.get("texto") or item.get("leitura") or ""
    if texto:
        return f"{ref_str}<br>{refrao_str}{texto}"
    return ""


def buscar_liturgia():
    # Tenta obter dados da API (versão v2/v3)
    urls = [
        "https://liturgia.up.railway.app/",
        "https://liturgia.up.railway.app/v2/",
        "https://liturgia.up.railway.app/v3/"
    ]

    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                j = r.json()
                dados = j[0] if isinstance(j, list) and len(j) > 0 else j

                p_leitura = ""
                s_leitura = ""
                salmo = ""
                evangelho = ""

                # Formato com array 'leituras'
                leituras = dados.get("leituras", []) if isinstance(dados, dict) else []
                for item in leituras:
                    tipo = str(item.get("tipo", "")).lower()
                    titulo = str(item.get("titulo", "")).lower()
                    conteudo = formatar_leitura(item)

                    if "primeira" in tipo or "1" in tipo or "primeira" in titulo:
                        p_leitura = conteudo
                    elif "segunda" in tipo or "2" in tipo or "segunda" in titulo:
                        s_leitura = conteudo
                    elif "salmo" in tipo or "salmo" in titulo:
                        salmo = conteudo
                    elif "evangelho" in tipo or "evangelho" in titulo:
                        evangelho = conteudo

                # Formato chave-valor simples
                if isinstance(dados, dict):
                    if not p_leitura and "primeiraLeitura" in dados:
                        p_leitura = formatar_leitura(dados.get("primeiraLeitura"))
                    if not s_leitura and "segundaLeitura" in dados:
                        s_leitura = formatar_leitura(dados.get("segundaLeitura"))
                    if not salmo and "salmo" in dados:
                        salmo = formatar_leitura(dados.get("salmo"))
                    if not evangelho and "evangelho" in dados:
                        evangelho = formatar_leitura(dados.get("evangelho"))

                if evangelho or salmo or p_leitura:
                    return {
                        "liturgia": dados.get("liturgia") or dados.get("titulo") or "Liturgia do Dia",
                        "cor": dados.get("cor") or "Verde",
                        "primeiraLeitura": p_leitura,
                        "segundaLeitura": s_leitura,
                        "salmo": salmo,
                        "evangelho": evangelho,
                        "link": "https://liturgia.cancaonova.com/",
                        "data": dados.get("data") or datetime.now().strftime("%d/%m/%Y")
                    }
        except Exception:
            continue

    # Caso a API externa esteja fora do ar, exibe aviso amigável com o link oficial
    return {
        "liturgia": "Liturgia Diária",
        "cor": "Verde",
        "primeiraLeitura": "Acesse o site oficial abaixo para ler as leituras completas de hoje.",
        "segundaLeitura": "",
        "salmo": "",
        "evangelho": "Clique no botão abaixo para ler o Evangelho do dia no portal Canção Nova / CNBB.",
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
body { margin:0; font-family: Arial, sans-serif; background:#fef8f0; padding:15px; }
.card { background:white; border-radius:12px; padding:20px; max-width:600px; margin:10px auto; box-shadow:0 2px 8px rgba(0,0,0,0.1); }
.secao { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px; }
.secao h3 { color: #880000; margin-bottom: 5px; }
.badge-cor { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; background: #e0e0e0; }
</style>
</head>
<body>
<div class="card">
<a href='{{url_for('index')}}'>voltar</a>

  <h2>Liturgia <span id="dataHoje"></span></h2>
  <div id="conteudoLiturgia">Carregando liturgia...</div>
</div>

<script>
async function carregarLiturgia(){
  const el = document.getElementById('conteudoLiturgia');
  try {
    const res = await fetch('/api/liturgia');
    const data = await res.json();

    document.getElementById('dataHoje').innerText = data.data ? '- ' + data.data : '';

    let html = '<p><b>' + (data.liturgia || 'Liturgia do Dia') + '</b> <span class="badge-cor">Cor: ' + (data.cor || 'Verde') + '</span></p><hr>';

    if (data.primeiraLeitura) {
      html += '<div class="secao"><h3>📖 1ª Leitura</h3><p>' + data.primeiraLeitura + '</p></div>';
    }

    if (data.salmo) {
      html += '<div class="secao"><h3>🎵 Salmo Responsorial</h3><p>' + data.salmo + '</p></div>';
    }

    if (data.segundaLeitura) {
      html += '<div class="secao"><h3>📖 2ª Leitura</h3><p>' + data.segundaLeitura + '</p></div>';
    }

    if (data.evangelho) {
      html += '<div class="secao"><h3>✝️ Evangelho</h3><p>' + data.evangelho + '</p></div>';
    }

    html += '<p style="text-align:center; margin-top:20px;"><a href="' + data.link + '" target="_blank" style="background:#880000; color:white; text-decoration:none; padding:10px 15px; border-radius:6px; display:inline-block;">Ver no site oficial da Canção Nova</a></p>';

    el.innerHTML = html;
  } catch(e) {
    el.innerHTML = '<p style="color:red; text-align:center;">Não foi possível carregar o conteúdo. <br><br><a href="https://liturgia.cancaonova.com/" target="_blank" style="color:#880000;">Clique aqui para abrir no site oficial</a></p>';
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
    app.run(host = '0.0.0.0', port = 10000)