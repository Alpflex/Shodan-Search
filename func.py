# -*- coding: utf-8 -*-

#########################Importerar moduler
import urllib.request
import shodan
import smtplib, ssl


from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


##############Shodan API nyckel för att kunna koppla dig mot shodan
SHODAN_API_KEY = 'KEY'
api = shodan.Shodan(SHODAN_API_KEY)

#####################En sök funktion. Tar först fram din utgående ip och sedan söker i Shodan
def hostsearch():

        try:
            external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

            print(external_ip)
            host = api.host('192.71.41.231')

            print("""
                    IP: {}
                    Organization: {}
                    Operating System: {}
            """.format(host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a')))


        except shodan.APIError as e:
            print('Error: {}'.format(e))
#####################################################################################


##################################En utförligt sök funktion som söker efter företagsnamn, kan skriva till en fil samt maila filen.
def searchcompany():
    try:

        companyname = input('Skriv in ditt företags namn som du vill söka i Shodan eller andra namn som är kopplat mot företaget som dotterbolag? ')
        search = api.search(companyname)


        report = input('Vill du ha resultatet till en fill ja/nej')
        if report == 'ja':

            #file = open("utmatning.txt", "w")

            import os
            file = open("utmatning.txt", "w", encoding="utf-8")
            #os.remove("utmatning.txt")
            #file = open("utmatning.txt", "x")

            file.write(str('Resultat var funna: {}'.format(search['total'])))

            for result in search['matches']:
                file = open("utmatning.txt", "a", encoding="utf-8")
                file.write(str('\n'))

                file.write(str('IP: {}'.format(result['ip_str'])))
                file.write(str('\n'))
                file.write(str(''))
                file.write(str(result['data']))
                file.write(str('\n'))
                file.write(str('\n'))
                file.close()



            mail = input('Vill du skicka rapporten till en email adress? ja/nej')
            if mail == 'ja':
                mailsecurity()



            for result in search['matches']:
                print('IP: {}'.format(result['ip_str']))
                print(result['data'])
                print('')
        elif report == 'nej':

            print('Resultat var funna: {}'.format(search['total']))
        else:
            print('Var good och välj ett av alternativerna, ja/nej, försök igen!')
            searchcompany()



    except shodan.APIError as e:
        print('Error: {}'.format(e))

#######################################################################################################################




###################################################Funktion som skickar mail med filen
def sendmail():


    subject = "Repport från Shodan"
    body = "Detta mail har skickat till dig ifrån Shodan programent, detta följer med en document. Var good och inte svara på detta mail."
    sender_email = "EMAIL"
    receiver_email = email
    password = input("Skriv in lössenordet: ")

    # Skapar veriable som är viktiga till mail
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    # Text som följer med mejlet
    message.attach(MIMEText(body, "plain"))

    filename = "utmatning.txt"

    # Öppnar filen och lägger till in i mejlet
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encodar filen till ASCII
    encoders.encode_base64(part)

    # rubrik
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # conventerar till en string
    message.attach(part)
    text = message.as_string()

    # loggar in till mailservern
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
#########################################################################################################

def mailsecurity():
    from emailrep import EmailRep
    emailrep = EmailRep('EMAILKEY')
    global email
    email = input('Skriv in mejlet som du vill skicka till: ')

    resultat = (emailrep.query(email))

    print("----------------------------------------------------------------")
    for c, v in resultat.items():
        print(c, v)
    print("----------------------------------------------------------------")

    svar = input("Vill du fortsätta skicka ditt mail till den angivna mejlet? ja/nej")
    if svar == 'ja':
        sendmail()
