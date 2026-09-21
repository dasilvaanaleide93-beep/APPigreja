from flask import Flask, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)


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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/liturgia")
def pagina_liturgia():
    return render_template("liturgia.html")


@app.route("/api/liturgia")
def api_liturgia():
    return jsonify(buscar_liturgia())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)