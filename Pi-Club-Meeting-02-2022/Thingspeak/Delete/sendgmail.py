import smtplib, ssl
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "iamsswu@gmail.com"
password = "Aquarius090317"

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server,port)
    server.starttls(context=context) # Secure the connection
    server.login(sender_email, password)
    # TODO: Send email here
    #sender_email = "iamsswu@gmail.com"
    receiver_email = "iamssgoh@gmail.com"
    message = """\
    Subject: Hi there
    This message is sent from Python."""
    server.sendmail(sender_email, receiver_email, message)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit() 