from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)


def extrair_texto_leitura(dados_leitura):
    """Garante que o texto da leitura seja extraído com segurança mesmo se vier vazio ou em formato diferente."""
    if not dados_leitura:
        return ""
    if isinstance(dados_leitura, dict):
        ref = dados_leitura.get("referencia") or ""
        ref_str = f" ({ref})" if ref else ""

        refrao = dados_leitura.get("refrao") or ""
        refrao_str = f"<p><b>Refrão:</b> <i>{refrao}</i></p>" if refrao else ""

        texto = dados_leitura.get("texto") or dados_leitura.get("leitura") or ""
        if texto:
            return f"{ref_str}<br>{refrao_str}{texto}"
        return ""
    elif isinstance(dados_leitura, str):
        return dados_leitura
    return ""


def buscar_liturgia():
    try:
        # Consulta com timeout de 10s
        r = requests.get("https://liturgia.up.railway.app/v3/", timeout=10)

        if r.status_code == 200:
            j = r.json()

            # Trata se o retorno for uma lista de celebrações
            dados = j[0] if isinstance(j, list) and len(j) > 0 else j

            p_leitura = ""
            s_leitura = ""
            salmo = ""
            evangelho = ""

            # Procura no array 'leituras' da versão v3
            leituras = dados.get("leituras", []) if isinstance(dados, dict) else []

            for item in leituras:
                if not isinstance(item, dict):
                    continue
                tipo = str(item.get("tipo", "")).lower()
                titulo = str(item.get("titulo", "")).lower()
                conteudo = extrair_texto_leitura(item)

                if "primeira" in tipo or "1" in tipo or "1a" in tipo or "primeira" in titulo:
                    p_leitura = conteudo
                elif "segunda" in tipo or "2" in tipo or "2a" in tipo or "segunda" in titulo:
                    s_leitura = conteudo
                elif "salmo" in tipo or "salmo" in titulo:
                    salmo = conteudo
                elif "evangelho" in tipo or "evangelho" in titulo:
                    evangelho = conteudo

            # Fallback para o formato direto caso o array 'leituras' não tenha os campos
            if isinstance(dados, dict):
                if not p_leitura and "primeiraLeitura" in dados:
                    p_leitura = extrair_texto_leitura(dados.get("primeiraLeitura"))
                if not s_leitura and "segundaLeitura" in dados:
                    s_leitura = extrair_texto_leitura(dados.get("segundaLeitura"))
                if not salmo and "salmo" in dados:
                    salmo = extrair_texto_leitura(dados.get("salmo"))
                if not evangelho and "evangelho" in dados:
                    evangelho = extrair_texto_leitura(dados.get("evangelho"))

            return {
                "liturgia": dados.get("liturgia") or dados.get("titulo") or "Liturgia do Dia",
                "cor": dados.get("cor") or "Verde",
                "primeiraLeitura": p_leitura,
                "segundaLeitura": s_leitura,
                "salmo": salmo,
                "evangelho": evangelho or "Consulte o site oficial da Canção Nova.",
                "link": "https://liturgia.cancaonova.com/",
                "data": dados.get("data") or datetime.now().strftime("%d/%m/%Y")
            }

    except Exception as e:
        print(f"Erro ao capturar liturgia: {e}")

    return {
        "liturgia": "Liturgia do Dia",
        "cor": "Verde",
        "primeiraLeitura": "",
        "segundaLeitura": "",
        "salmo": "",
        "evangelho": "Não foi possível carregar a liturgia. Acesse o site oficial.",
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
</style>
</head>
<body>
<div class="card">
  <button onclick="history.back()" style="background:#880000;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer">← Voltar</button>
  <h2>Liturgia <span id="dataHoje"></span></h2>
  <div id="conteudoLiturgia">Carregando liturgia...</div>
</div>

<script>
async function carregarLiturgia(){
  const el = document.getElementById('conteudoLiturgia');
  try {
    const res = await fetch('/api/liturgia?v=' + new Date().getTime());
    if (!res.ok) {
        throw new Error('Servidor retornou código ' + res.status);
    }
    const data = await res.json();

    document.getElementById('dataHoje').innerText = data.data ? `- ${data.data}` : '';

    let html = `<p><b>${data.liturgia}</b> <span class="badge-cor">Cor: ${data.cor}</span></p><hr>`;

    if (data.primeiraLeitura) {
      html += `<div class="secao"><h3>📖 1ª Leitura</h3><p>${data.primeiraLeitura}</p></div>`;
    }

    if (data.salmo) {
      html += `<div class="secao"><h3>🎵 Salmo Responsorial</h3><p>${data.salmo}</p></div>`;
    }

    if (data.segundaLeitura) {
      html += `<div class="secao"><h3>📖 2ª Leitura</h3><p>${data.segundaLeitura}</p></div>`;
    }

    if (data.evangelho) {
      html += `<div class="secao"><h3>✝️ Evangelho</h3><p>${data.evangelho}</p></div>`;
    }

    html += `<p><a href="${data.link}" target="_blank" style="color:#880000;">Ver no site oficial da Canção Nova</a></p>`;

    el.innerHTML = html;
  } catch(e) {
    el.innerHTML = '<p style="color:red">Ocorreu um erro ao carregar a liturgia. Tente novamente mais tarde.</p>';
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