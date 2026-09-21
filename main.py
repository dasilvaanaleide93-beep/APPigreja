import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Cria o banco se não existir
def init_db():
    conn = sqlite3.connect('mural.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pedidos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  nome TEXT, texto TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect('/mural')

@app.route('/mural')
def mural():
    conn = sqlite3.connect('mural.db')
    c = conn.cursor()
    c.execute('SELECT nome, texto FROM pedidos ORDER BY id DESC')
    pedidos = c.fetchall()
    conn.close()
    return render_template('mural.html', pedidos=pedidos)

@app.route('/enviar', methods=['POST'])
def enviar():
    login = request.form.get('login', '')
    senha = request.form.get('senha', '')
    texto = request.form.get('texto', '')
    
    # Senha simples que você já usava
    if senha == '1234' or senha == 'paroquia':
        nome = login if login else 'Anônimo'
        conn = sqlite3.connect('mural.db')
        c = conn.cursor()
        c.execute('INSERT INTO pedidos (nome, texto) VALUES (?, ?)', (nome, texto))
        conn.commit()
        conn.close()
    
    return redirect('/mural')

# NÃO coloca app.run aqui, o Render usa o gunicorn
