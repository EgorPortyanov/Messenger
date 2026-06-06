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

    html_body = f"""
    <html>
    <body style="margin: 0; padding: 0; background-color: #FAF8FF; font-family: 'Inter', Helvetica, Arial, sans-serif;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 20px auto; background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E2E1EC; box-shadow: 0 4px 12px rgba(7, 10, 28, 0.05); overflow: hidden;">
            
            <tr>
                <td style="padding: 40px 30px; text-align: center;">
                    
                    <h1 style="
                        max-width: 546px;
                        margin: 0 auto 16px auto;
                        font-family: 'Inter', system-ui, -apple-system, sans-serif;
                        font-size: 28px;
                        font-weight: 600;
                        line-height: 32px;
                        letter-spacing: -0.025em;
                        color: #070A1C;
                        text-align: center;
                    ">
                        Вас вітає команда World IT !
                    </h1>

                    <p style="
                        max-width: 546px;
                        margin: 0 auto 32px auto;
                        font-family: 'Inter', system-ui, -apple-system, sans-serif;
                        font-size: 16px;
                        font-weight: 400;
                        line-height: 22px;
                        letter-spacing: 0em;
                        color: #0F172A;
                        text-align: center;
                    ">
                        Щоб завершити реєстрацію та переконатися, що саме ви є власником цієї електронної адреси, будь ласка, підтвердіть свою пошту.
                    </p>
                    
                    <a href="{url}" style="
                        display: block; 
                        max-width: 546px; 
                        height: 20px;
                        margin: 0 auto 32px auto;
                        background-color: #070A1C; 
                        color: #FAF8FF; 
                        font-family: 'Inter', system-ui, sans-serif;
                        font-size: 14px; 
                        font-weight: 500; 
                        text-decoration: none; 
                        padding: 8px 16px; 
                        border-radius: 6px; 
                        box-shadow: 0px 1px 2px 0px rgba(0, 0, 0, 0.05);
                        text-align: center;
                        line-height: 20px;
                    ">
                        Підтвердити пошту
                    </a>

                    <img src="https://i.postimg.cc/HWyGdfvZ/chatgpt.png" alt="iMessenger Иллюстрация" style="
                        display: block;
                        width: 339.55px;
                        height: 288.02px;
                        margin: 0 auto;
                        border: none;
                        outline: none;
                        text-decoration: none;
                    ">
                    
                    <div style="
                        max-width: 546px;
                        margin: 24px auto;
                        border-top: 1px solid rgba(37, 42, 82, 0.4);
                        height: 0px;
                    "></div>

                    <p style="
                        max-width: 546px;
                        margin: 0 auto;
                        font-family: 'Inter', system-ui, -apple-system, sans-serif;
                        font-size: 16px;
                        font-weight: 400;
                        line-height: 28px;
                        letter-spacing: 0em;
                        color: #0F172A;
                        text-align: center;
                    ">
                        Якщо у вас виникнуть питання — ми завжди раді допомогти!<br style="margin-bottom: 8px;">
                        <span style="font-weight: 500;"З найкращими побажаннями, команда World IT Academy</span>
                    </p>
                    
                </table>
            </tr>
            
        </table>
    </body>
    </html>
    """

    message.attach(MIMEText(html_body, "html", "utf-8"))
    
    try:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            smtp.starttls()
            smtp.login("m34922908@gmail.com", "nrrnlbzowytuxqqw")
            smtp.sendmail(message["From"], message["To"], message.as_string())
            print("Лист успішно відправлено на пошту!")
    except Exception as e:
        print(f"Ошибка SMTP при отправке письма: {e}")