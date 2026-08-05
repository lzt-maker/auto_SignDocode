import requests
import smtplib
from email.mime.text import MIMEText
import os

# -------------------------- 从GitHub Actions环境变量读取敏感信息 --------------------------
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")
COOKIE_STR = os.getenv("CHECKIN_COOKIE")
NEW_API_USER = os.getenv("NEW_API_USER")

def send_email(content):
    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = "Docode签到通知"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅邮件发送成功")
    except Exception as err:
        print("❌邮件发送失败：", err)

# -------------------------- 签到逻辑 --------------------------
url = "https://docode.cc/api/user/checkin"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": COOKIE_STR,
    "New-Api-User": NEW_API_USER,
    "Referer": "https://docode.cc/"
}

try:
    response = requests.post(url, headers=headers)
    print("状态码:", response.status_code)

    if response.status_code == 200:
        resp_json = response.json()
        message_text = resp_json["message"]
        print("响应内容:", message_text)
        send_email(message_text)
    else:
        print(f"请求非200，状态码：{response.status_code}，不发送邮件")

except Exception as e:
    print("签到请求发送失败:", e)