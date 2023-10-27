import mysql.connector as sql
import smtplib, ssl

def calculate_mean(cursor):
    query = 'SELECT weight from birds;'
    cursor.execute(query)
    data = cursor.fetchall()
    sum = 0
    for i in data:
        sum += i[0]
    mean = sum / len(data)
    return mean


def send_email(message, receiver_email):
    mail_port = 587
    smtp_server = 'smtp.gmail.com'
    sender_email = 'centadlm092023@gmail.com'
    password = 'ganu sjbp zijx paaj'
    context = ssl.create_default_context()
    message2 = f'Subject:Error \nPossible sick bird at {message} '
    with smtplib.SMTP(smtp_server, mail_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message2)


send_email("[(28, '0007633FC2', '19 30 12', '26/10/23', 0)]", '191321y@student.hci.edu.sg')



