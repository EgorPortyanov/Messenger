import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import url_for

def send_verify_code(verify_code: str, email_receiver: str):
    message = MIMEMultipart()
    message["From"] = "m34922908@gmail.com"
    message["To"] = email_receiver
    message["Subject"] = "iMessenger Registration Confirm"

    url = url_for("user_app.render_verify", verify_code=verify_code, _external=True)
    body = f"Для підтвердження реєстрації перейдіть за посиланням:\n{url}"

    message.attach(MIMEText(body, "plain", "utf-8"))
    
    try:
        with smtplib.SMTP(host="64.233.184.108", port=587) as smtp:
            smtp.starttls()
            smtp.login("m34922908@gmail.com", "nrrnlbzowytuxqqw")
            
            smtp.sendmail(message["From"], message["To"], message.as_string())
            print("Лист успішно відправлено на пошту!")
    except Exception as e:
        print(f"Ошибка SMTP при отправке письма: {e}")
