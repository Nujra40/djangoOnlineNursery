from email.mime.image import MIMEImage
import smtplib

from html2image import Html2Image

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PIL import Image
import os


def renderMail(fname, otp):

    with open("./mail/template.pre-html", "r") as template:
        template = template.read()
    
    document = template.format(fname, otp)

    with open(f"./{fname}-template.html", "w") as template:
        template.write(document)
    
    with open(f"./{fname}-template.html") as document:
        hti = Html2Image()
        hti.screenshot(html_str=document.read(), save_as=f"{fname}-template.jpg")
    
    img = Image.open(f"{fname}-template.jpg")
    area = (460, 0, 1440, 1080)
    cropped_img = img.crop(area)
    resized = cropped_img.resize((round(cropped_img.size[0]*0.7), round(cropped_img.size[1]*0.7)))
    resized.save(f"{fname}-otp.jpg")

    os.remove(f"{fname}-template.html")
    os.remove(f"{fname}-template.jpg")

    return f"./{fname}-otp.jpg"


def sendMail(to, fname, otp):
    document = renderMail(fname, otp)
    gmail_sender = 'nujra40@gmail.com'
    gmail_password = 'opxkhuezntfdpqoi'
    
    msg = MIMEMultipart('related')
    msg['Subject'] = "Authentication - OTP"
    msg['From'] = gmail_sender
    msg['To'] = to

    part2 = MIMEText(open("./mail/index.html").read(), 'html')
    msg.attach(part2)
    
    msgImage = MIMEImage(open(document, 'rb').read())

    msgImage.add_header('Content-ID', '<otpImage>')
    msg.attach(msgImage)

    MailServer = smtplib.SMTP('smtp.gmail.com', 587)
    MailServer.ehlo()
    MailServer.starttls()
    MailServer.login(gmail_sender, gmail_password)

    try:
        MailServer.sendmail(gmail_sender, to, msg.as_string())
        return True
    except:
        return False
    finally:
        os.remove(document)
        MailServer.close()
