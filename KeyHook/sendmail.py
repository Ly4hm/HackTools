from email.mime.multipart import MIMEMultipart
import smtplib
import email.message
import email.policy
import email.utils

from email.mime.image import MIMEImage
from screenshotter import run as screenshotter_run


def make_and_send_email(mail_content, subscriber, subject, img_data):
    """
    构造并发送包含图像附件的邮件
    参数:
        mail_content (str): 邮件内容
        subscriber (str): 接收邮件的邮箱地址
        subject (str): 邮件主题
        img_data (bytes): 图像文件的二进制数据
    返回:
        无
    异常:
        如果发送邮件失败，将抛出异常
    """

    # 多部分邮件构造
    message = MIMEMultipart(email.policy.SMTP)  # 指定邮件策略
    message["Subject"] = subject  # 主题
    message["To"] = "master"
    message["From"] = "client@cc.com"
    message["Data"] = email.utils.formatdate(localtime=True)
    message["Message-ID"] = email.utils.make_msgid()

    # Add the plain text content to the message
    message.attach(email.message.EmailMessage(email.policy.default))
    message.get_payload()[0].set_content(mail_content)

    # Create a MIMEImage object
    image = MIMEImage(img_data)
    image.add_header("Content-Disposition", "attachment", filename="image.bmp")
    message.attach(image)

    # 邮件发送
    mail = smtplib.SMTP()
    mail.connect("smtp.163.com")  # 连接 qq 邮箱
    mail.login("xxxxxxxxxS@163.com", "xxxxxxxxxS")  # 账号和授权码
    try:
        mail.sendmail(
            "xxxxxxxxxS7@163.com", subscriber, message.as_string()
        )  # 发送账号、接收账号和邮件信息
        print("successfully send")
    except Exception as e:
        print(f"fail to send\n{e}")


if __name__ == "__main__":
    make_and_send_email("this is a test", "xxxxxxxxxS@qq.com", "作业", screenshotter_run())
