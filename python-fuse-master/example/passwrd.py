import easygui
import sys
import smtplib, ssl
import csv
from random import randrange


def sendmail(name, email, p):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "tecnologiaseguranca2020@gmail.com"
    password = "ricardomateus"
    receiver_email = email
    # p = randrange(1,9999)
    message = " Subject: Hi there " + name + "! to acess folder this is the password you need " + str(
        p) + ", thank you have a nice day!"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


def password():

    # with open('/home/test.csv', newline='') as csvfile:
    #     data = list(csv.reader(csvfile))
    #     print(data)
    
    # for i in data:
    #     print(i[0])
    
    p = randrange(1, 9999)
    data = [['Sam', 'tecnologiaseguranca2020@gmail.com'], ['John Doe', 'tecnologiaseguranca2020@gmail.com'],
            ['Joshua', 'tecnologiaseguranca2020@gmail.com']]
    myuser = easygui.enterbox("Wich User are you?")
    
    for i in data:
        if i[0] == myuser:
            sendmail(i[0], i[1], p)
    
    fieldNames = ['Nome', 'Password']
    myvar = easygui.multenterbox('Fill in the blanks', 'Authorizer', fieldNames)
    print("this is p-->", p)
    print("pass-->", myvar[1])
    if myvar[1] == str(p):
        print("Hell", myvar)
        return 1
    else:
        # print(myvar)
        return -1

# password()


