import os
from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'sonacode'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv("EMAIL"),
    "MAIL_PASSWORD": os.getenv("SENHA")
}

app.config.update(mail_settings)
mail = Mail(app)

class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    try:
        formContato = Contato(
            request.form["nome"],
            request.form["email"],
            request.form["mensagem"]
        )

        destinatarios = [
            os.getenv("EMAIL_DESTINO"),
            app.config.get("MAIL_USERNAME")
        ]

        msg = Message(
            subject=f'{formContato.nome} te enviou uma mensagem no portfólio',
            sender=app.config.get("MAIL_USERNAME"),
            recipients=destinatarios,
            body=f'''
{formContato.nome} com o e-mail {formContato.email}, te enviou a seguinte mensagem:

{formContato.mensagem}
            '''
        )
        mail.send(msg)
        flash('Mensagem enviada com sucesso!')
    except Exception as e:
        flash(f'Erro ao enviar a mensagem: {e}')
    return redirect('/')