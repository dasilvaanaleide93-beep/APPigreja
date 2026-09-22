import os, sqlite3
from flask import Flask, request, redirect
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
DB = "/tmp/mural.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS recados (id INTEGER PRIMARY KEY, nome TEXT, mensagem TEXT)')
    conn.commit(); conn.close()
init_db()

# FOTO QUE FUNCIONA - sem ciclo, direta
IMG_SANTA = "https://upload.wikimedia.org/wikipedia/commons/5/5a/Sainte_Th%C3%A9r%C3%A8se_de_l%27Enfant_J%C3%A9sus.jpg"

@app.route('/')
def home():
    return f'''
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{{font-family:Arial;margin:0;background:#fff8f0;text-align:center}}
       .banner{{background:linear-gradient(#ff9a5c,#ff6a2d);padding:30px 20px;color:white}}
       .banner img{{width:160px;height:160px;border-radius:50%;border:5px solid white;object-fit:cover;background:white}}
       .menu{{display:grid;grid-template-columns:1fr 1fr;gap:15px;padding:20px;max-width:500px;margin:auto}}
       .btn{{background:white;padding:22px 10px;border-radius:18px;text-decoration:none;color:#333;font-size:19px;font-weight:bold;box-shadow:0 3px 10px #0002;display:block}}
       .btn span{{font-size:42px;display:block;margin-bottom:5px}}
    </style></head><body>
        <div class="banner">
            <img src="{IMG_SANTA}">
            <h1 style="margin:15px 0 5px">Santa Teresinha</h1>
            <p style="margin:0;opacity:0.9">Paróquia Santa Teresinha - App da Igreja</p>
        </div>
        <div class="menu">
            <a class="btn" href="/mural/novo"><span>💌</span>Mural de Recado</a>
            <a class="btn" href="/oracoes"><span>📖</span>Orações</a>
            <a class="btn" href="/doacoes"><span>❤️</span>Doações</a>
            <a class="btn" href="/liturgia"><span>✝️</span>Liturgia</a>
        </div>
    </body></html>
    '''

@app.route('/mural/novo', methods=['GET','POST'])
def mural():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO recados (nome, mensagem) VALUES (?,?)", (request.form.get('nome','Anônimo'), request.form.get('mensagem','')))
        conn.commit(); conn.close()
        return redirect('/mural/novo')
    c.execute("SELECT nome, mensagem FROM recados ORDER BY id DESC")
    recados = c.fetchall(); conn.close()
    lista = "".join([f'<div style="background:white;padding:18px;margin:12px 0;border-radius:12px;font-size:24px;text-align:left;box-shadow:0 2px 5px #0001"><b style="color:#e65a2d">{r[0]}:</b><br>{r[1]}</div>' for r in recados])
    return f'<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body style="font-family:Arial;background:#fff8f0;padding:15px;max-width:650px;margin:auto"><a href="/" style="font-size:20px;text-decoration:none">⬅️ Voltar</a><h1 style="font-size:34px;text-align:center">💌 Mural de Recado</h1><form method="POST" style="background:white;padding:22px;border-radius:18px;box-shadow:0 3px 12px #0002"><input name="nome" placeholder="Seu nome" style="width:100%;padding:22px;font-size:24px;border-radius:12px;border:2px solid #ddd;box-sizing:border-box"><br><br><textarea name="mensagem" placeholder="Deixe sua mensagem..." style="width:100%;padding:22px;font-size:24px;border-radius:12px;border:2px solid #ddd;height:130px;box-sizing:border-box"></textarea><br><br><button style="width:100%;padding:22px;font-size:28px;background:#ff6a2d;color:white;border:none;border-radius:14px;font-weight:bold">ENVIAR</button></form><div style="margin-top:20px">{lista}</div></body></html>'

@app.route('/oracoes')
def oracoes():
    return '''
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="font-family:Arial;padding:15px;max-width:650px;margin:auto;background:#fff8f0">
    <a href="/" style="font-size:20px;text-decoration:none">⬅️ Voltar</a>
    <h1 style="text-align:center">📖 Orações</h1>

    <div style="background:white;padding:20px;border-radius:15px;margin-bottom:15px;box-shadow:0 2px 8px #0001">
    <h3 style="color:#ff6a2d">Oração a Santa Teresinha</h3>
    <p style="font-size:20px;line-height:1.7">
    Ó Santa Teresinha do Menino Jesus, que prometestes fazer cair do céu uma chuva de rosas,<br><br>
    Olhai para nossas necessidades e intercedei por nós junto a Deus.<br><br>
    Ensinai-nos o vosso caminho de infância espiritual, de amor e simplicidade.<br><br>
    Amém.
    </p>
    </div>

    <div style="background:white;padding:20px;border-radius:15px;margin-bottom:15px;box-shadow:0 2px 8px #0001">
    <h3 style="color:#ff6a2d">Pai Nosso - Completo</h3>
    <p style="font-size:20px;line-height:1.7">
    Pai nosso que estais nos céus,<br>
    santificado seja o vosso nome,<br>
    venha a nós o vosso Reino,<br>
    seja feita a vossa vontade,<br>
    assim na terra como no céu.<br><br>
    O pão nosso de cada dia nos dai hoje,<br>
    perdoai-nos as nossas ofensas,<br>
    assim como nós perdoamos a quem nos tem ofendido,<br>
    e não nos deixeis cair em tentação,<br>
    mas livrai-nos do mal.<br><br>
    Amém.
    </p>
    </div>

    <div style="background:white;padding:20px;border-radius:15px;box-shadow:0 2px 8px #0001">
    <h3 style="color:#ff6a2d">Ave Maria - Completa</h3>
    <p style="font-size:20px;line-height:1.7">
    Ave Maria, cheia de graça,<br>
    o Senhor é convosco,<br>
    bendita sois vós entre as mulheres,<br>
    e bendito é o fruto do vosso ventre, Jesus.<br><br>
    Santa Maria, Mãe de Deus,<br>
    rogai por nós, pecadores,<br>
    agora e na hora de nossa morte.<br><br>
    Amém.
    </p>
    </div>
    </body></html>
    '''

@app.route('/doacoes')
def doacoes():
    return '<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body style="font-family:Arial;padding:20px;max-width:600px;margin:auto;background:#fff8f0"><a href="/">⬅️ Voltar</a><h1>❤️ Doações</h1><div style="background:white;padding:20px;border-radius:12px;font-size:22px"><p>Ajude nossa paróquia!</p><p><b>PIX:</b> (coloque seu PIX aqui)<br><br>Que Deus abençoe!</p></div></body></html>'

@app.route('/liturgia')
def liturgia():
    return '''
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="font-family:Arial;padding:15px;max-width:650px;margin:auto;background:#fff8f0">
    <a href="/" style="font-size:20px;text-decoration:none">⬅️ Voltar</a>
    <h1 style="text-align:center">✝️ Liturgia Diária</h1>
    <p style="text-align:center;background:#ff6a2d;color:white;padding:12px;border-radius:10px;font-size:19px">
    <b>21 de Setembro de 2026 - Domingo<br>25ª Semana do Tempo Comum<br>Festa de São Mateus, Apóstolo</b><br>Cor: Vermelha
    </p>

    <div style="background:white;padding:20px;border-radius:15px;margin-bottom:15px;box-shadow:0 2px 8px #0001">
    <h3 style="color:#ff6a2d">📖 1ª Leitura - Ef 4,1-7.11-13</h3>
    <p style="font-size:19px;line-height:1.6">
    Irmãos, eu, prisioneiro no Senhor, vos exorto a caminhardes de acordo com a vocação que recebestes:
    com toda a humildade e mansidão, suportai-vos uns aos outros com paciência, no amor.
    Aplicai-vos a guardar a unidade do espírito pelo vínculo da paz.<br><br>
    Há um só Corpo e um só Espírito, como também é uma só a esperança à qual fostes chamados.
    Há um só Senhor, uma só fé, um só batismo, um só Deus e Pai de todos, que reina sobre todos, age por meio de todos e permanece em todos.<br><br>
    Cada um de nós recebeu a graça na medida em que Cristo lha deu. E foi ele quem instituiu alguns como apóstolos, outros como profetas, outros ainda como evangelistas, outros, enfim, como pastores e mestres.
    Assim, ele capacitou os santos para o ministério, para edificar o corpo de Cristo, até que cheguemos todos juntos à unidade da fé e do conhecimento do Filho de Deus.<br><br>
    <b>- Palavra do Senhor. - Graças a Deus.</b>
    </p>
    </div>

    <div style="background:white;padding:20px;border-radius:15px;margin-bottom:15px;box-shadow:0 2px 8px #0001">
    <h3 style="color:#ff6a2d">🎵 Salmo Responsorial - Sl 18(19A),2-3.4-5</h3>
    <p style="font-size:19px;line-height:1.6">
    <b>R. Seu som ressoa e se espalha em toda a terra.</b><br><br>
    Os céus proclamam a glória do Senhor, e o firmamento, a obra de suas mãos;<br>
    o dia ao dia transmite esta mensagem, a noite à noite publica esta notícia. <b>R.</b><br><br>
    Não são discursos nem frases ou palavras, nem são vozes que possam ser ouvidas;<br>
    seu som ressoa e se espalha em toda a terra, chega aos confins do universo a sua voz. <b>R.</b>
    </p>
    </div>

    <div style="background:white;padding:20px;border-radius:15px;margin-bottom:15px;box-shadow:0 2px 8px #0001">
    <h3 style="color:#ff6a2d">✝️ Evangelho - Mt 9,9-13</h3>
    <p style="font-size:19px;line-height:1.6">
    <b>- O Senhor esteja convosco. - Ele está no meio de nós.<br>
    - Proclamação do Evangelho de Jesus Cristo segundo Mateus. - Glória a vós, Senhor.</b><br><br>
    Naquele tempo, Jesus viu um homem chamado Mateus, sentado na coletoria de impostos, e disse-lhe: "Segue-me!" Ele se levantou e seguiu a Jesus.<br><br>
    Enquanto Jesus estava à mesa, em casa de Mateus, vieram muitos cobradores de impostos e pecadores e sentaram-se à mesa com Jesus e seus discípulos.<br><br>
    Alguns fariseus viram isso e perguntaram aos discípulos: "Por que vosso mestre come com os cobradores de impostos e pecadores?"<br><br>
    Jesus ouviu a pergunta e respondeu: "Aqueles que têm saúde não precisam de médico, mas sim os doentes. Ide e aprendei o que significa: 'Quero misericórdia e não sacrifício'. De fato, eu não vim para chamar os justos, mas os pecadores".<br><br>
    <b>- Palavra da Salvação. - Glória a vós, Senhor.</b>
    </p>
    </div>

    </body></html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
