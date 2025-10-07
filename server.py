import os
import base64
from email.mime.text import MIMEText
from email.utils import formataddr

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from models import Contato, init_db, get_session

load_dotenv() 

app = Flask(__name__, static_folder='.')
CORS(app)

try:
    init_db()
    print("✅ Database initialized successfully")
except Exception as e:
    print(f"⚠️  Database initialization failed: {str(e)}")

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/send-email', methods=['POST'])
def send_email():
 
    session = None
    try:
        data = request.get_json(silent=True) or {}
        nome = (data.get('nome') or '').strip()
        email = (data.get('email') or '').strip()
        mensagem = (data.get('mensagem') or '').strip()

        if not all([nome, email, mensagem]):
            return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios.'}), 400

        session = get_session()
        novo = Contato(nome=nome, email=email, mensagem=mensagem)
        session.add(novo)
        session.commit()
        print(f"✅ Contato salvo: {nome} <{email}>")

        if os.getenv('DISABLE_EMAIL', '1') == '1':
            return jsonify({
                'success': True,
                'message': 'Contato enviado com sucesso! (notificação por e-mail desativada)'
            }), 200

    except Exception as e:
        if session:
            session.rollback()
        print(f"❌ Erro em /send-email: {e}")
        return jsonify({'success': False, 'message': 'Não foi possível enviar agora. Tente novamente.'}), 500
    finally:
        if session:
            session.close()

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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
