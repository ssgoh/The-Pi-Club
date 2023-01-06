#https://mail.google.com/mail/u/0/#inbox/KtbxLvhNVNlLqfmgZHbxdhVfpTHlCxQgqB?projector=1
import smtplib
from email.message import EmailMessage

def email_alert(subject,body,to):
    msg=EmailMessage()
    msg.set_content(body)
    
    msg['subject']=subject
    msg['to'] = to
    user="praspberry060@gmail.com"
    password="eajvptvfrrrgqvjh"  #app password, not the sign in password
    msg['from']=user
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()
    
if __name__ == '__main__':
    email_alert('Test',"Hello World","iamssgoh@gmail.com")