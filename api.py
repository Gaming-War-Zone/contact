from flask import Flask, request, render_template
import random
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)

SMTP_SERVER='smtp-relay.sendinblue.com'
SMTP_PORT=587
SMTP_LOGIN='benedict.ft1@gmail.com'
SMTP_PASSWORD='Zkt7UhOL21yd0cXa'
API_KEY='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'

def setup_message(recipient_email, result):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Inspirational Quote"
    message["From"] = SMTP_LOGIN
    message["To"] = recipient_email
    quote = get_quote(result)
    quote = MIMEText(quote, "html")
    message.attach(quote)
    return message


def send_quote(result, recipient_email=""):
    if len(sys.argv) == 2:
        recipient_email = sys.argv[-1]
    smtp_server = SMTP_SERVER
    smtp_port = SMTP_PORT
    smtp_login = SMTP_LOGIN
    password = SMTP_PASSWORD
    message = setup_message(recipient_email, result)
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.connect(smtp_server, smtp_port)
    server.login(smtp_login, password)
    response = server.sendmail(smtp_login, recipient_email, message.as_string())
    server.quit()
    return response


def get_quote(result):
    if result['email'] == 'benedicttshivhase@gmail.com':
        html = f"""\
            <html>
              <body>
                <h1>Massage from Personal Website</h1>
                <p><b>Name of sender: </b>{result['name']}</p>
                <p><b>Email: </b>{result['email']}</p>
                <p><b>Massage: {result['massage']}</b></p>
              </body>
            </html>
            """
    else:
        html = f"""\
            <html>
              <body>
                <h1>Hey {result['name']}</h1>
                <p>Thanks for contacting me, I will be responding shortly</p>
                <p>Kind Regards</p>
              </body>
            </html>
            """
    return html


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('contact.html', **locals())

@app.route("/contact/", methods=["GET", "POST"])
def contact():
    print(request.method)
    if request.method == 'POST':
        result = {}

        result['name'] = request.form['name']
        result['email'] = request.form['email'].replace(' ', '').lower()
        result['message'] = request.form['message']
        send_quote(result, 'benedicttshivhase@gmail.com')
        send_quote(result, result['email'])
        return render_template('thankyou.html',  **locals())
    return render_template('contact.html', **locals())



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)