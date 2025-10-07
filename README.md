# Guia Turístico – Coromandel

Site simples e bonito para apresentar pontos turísticos de **Coromandel**, curiosidades e um **formulário de contato**.  
Backend em **Flask** serve os arquivos estáticos, registra os contatos em **SQLite** e retorna confirmação.  
O envio de e-mail está **desativado por padrão** (pode ser habilitado depois).

---

## ✨ Páginas

- **Início** (`index.html`) — apresentação do site
- **Pontos Turísticos** (`pagina2.html`) — cards com fotos
- **Curiosidades** (`pagina3.html`) — lista de curiosidades
- **Contato** (`pagina4.html`) — formulário (nome, e-mail, mensagem)

---

## 🧰 Tecnologias

- **Frontend:** HTML5, CSS3 (Poppins), JavaScript (vanilla)
- **Backend:** Python 3, **Flask**, **Flask-CORS**
- **Banco:** **SQLite** (arquivo `contatos.db`)
- **Utilitários:** `requests`, `python-dotenv`, `google-api-python-client` *(para futuro envio por Gmail OAuth2)*

---

## ✅ Pré-requisitos

- Python 3.10+
- (Opcional) VS Code com extensão **Python**

---

## ▶️ Como rodar

 - Apertar F5 no VS Code ou no terminal: python start.py
   
