import easygui
import sys
import smtplib, ssl
from random import randrange


smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "tecnologiaseguranca2020@gmail.com"
password = "ricardomateus"
receiver_email = sender_email
p = randrange(1,9999)
message = " Subject: Hi there! to acess folder this is the password you need "+ str(p) +", thank you have a nice day!"

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    # TODO: Send email here
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit() 


myvar = easygui.enterbox("Enter Password?")
print(p)
if(myvar == str(p)):
    print("Hell", myvar)
    sys.exit(1)
else:
    print(myvar)
    sys.exit(-1)

   
