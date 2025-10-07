#!/usr/bin/env python3
import os
import base64
from email.mime.text import MIMEText
from email.utils import formataddr

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# DB (usa o models.py que te mandei antes)
from models import Contato, init_db, get_session

load_dotenv()  # lê variáveis do .env, se existir

app = Flask(__name__, static_folder='.')
CORS(app)

# ---------- inicializa banco ----------
try:
    init_db()
    print("✅ Database initialized successfully")
except Exception as e:
    print(f"⚠️  Database initialization failed: {str(e)}")


# ---------- headers anti-cache ----------
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# ---------- arquivos estáticos ----------
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)


# ---------- endpoint principal do formulário ----------
@app.route('/send-email', methods=['POST'])
def send_email():
    """
    Salva o contato no banco e (opcionalmente) envia e-mail.
    Por ora, deixamos o envio desativado com DISABLE_EMAIL=1.
    """
    session = None
    try:
        data = request.get_json(silent=True) or {}
        nome = (data.get('nome') or '').strip()
        email = (data.get('email') or '').strip()
        mensagem = (data.get('mensagem') or '').strip()

        if not all([nome, email, mensagem]):
            return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios.'}), 400

        # salva no banco
        session = get_session()
        novo = Contato(nome=nome, email=email, mensagem=mensagem)
        session.add(novo)
        session.commit()
        print(f"✅ Contato salvo: {nome} <{email}>")

        # caminho atual: NÃO enviar e-mail (retorna sucesso)
        if os.getenv('DISABLE_EMAIL', '1') == '1':
            return jsonify({
                'success': True,
                'message': 'Contato enviado com sucesso! (notificação por e-mail desativada)'
            }), 200

        # --- se quiser reativar o envio no futuro, remova o bloco acima
        # e implemente aqui a chamada do seu provedor (Gmail OAuth2, Brevo etc.)

    except Exception as e:
        if session:
            session.rollback()
        print(f"❌ Erro em /send-email: {e}")
        return jsonify({'success': False, 'message': 'Não foi possível enviar agora. Tente novamente.'}), 500
    finally:
        if session:
            session.close()


# ---------- endpoint de debug para listar últimos contatos ----------
@app.get('/debug/contatos')
def listar_contatos():
    sess = get_session()
    try:
        itens = sess.query(Contato).order_by(Contato.id.desc()).limit(200).all()
        return jsonify([
            {
                "id": c.id,
                "nome": c.nome,
                "email": c.email,
                "mensagem": c.mensagem,
                "criado_em": c.criado_em.isoformat()
            } for c in itens
        ])
    finally:
        sess.close()


# ---------- main ----------
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
