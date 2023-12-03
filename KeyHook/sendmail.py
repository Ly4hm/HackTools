import smtplib
import email.message
import email.policy
import email.utils


def make_and_send_email(mail_content, subscriber, subject):
    # 邮件构造
    message = email.message.EmailMessage(email.policy.SMTP)
    message["Subject"] = subject  # 主题
    message["To"] = "master"
    message["From"] = "client@cc.com"
    message["Data"] = email.utils.formatdate(localtime=True)
    message["Message-ID"] = email.utils.make_msgid()
    message.set_content(mail_content)
    
    # 邮件发送
    mail = smtplib.SMTP()
    mail.connect("smtp.163.com")  # 连接 qq 邮箱
    mail.login("xxxx@163.com", "xxxxxxx")  # 账号和授权码
    try:
        mail.sendmail(
            "mxxxx@163.com", subscriber, message.as_string()
        )  # 发送账号、接收账号和邮件信息
        print("successfully send")
    except Exception as e:
        print(f"fail to send\n{e}")


if __name__ == "__main__":
    make_and_send_email("this is a test", "xxxxx@qq.com", "作业")
