import email
import imaplib
from imap_tools import MailBox, AND



def download_atr_status():

    user = 'backofficei9br@gmail.com'
    password = 'i9br12345'
    server = 'smtp.gmail.com'
    pasta = 'primary'


    def connect(server, user, password):
        m = imaplib.IMAP4_SSL(server)
        m.login(user, password)
        #print(m)
        return m

    def downloaAttachmentsInEmail(m, emailid, pasta):
        resp, data = m.fetch(emailid, "(BODY.PEEK[])")
        email_body = data[0][1]
        mail = email.message_from_bytes(email_body)
        dados2 = mail.values()



        if dados2[17] == 'CribMonitor':
            for part in mail.walk():
                if part.get_content_maintype() != 'multipart' and part.get_all('Content-Disposition') is not None:
                    open(pasta + '\\' + 'atr_status' + '.csv', 'wb').write(part.get_payload(decode=True))


    def downloadAllAttachmentsInInbox(server, user, password, pasta):
        m = connect(server, user, password)
        resp, items = m.search(None, "(ALL)")
        print(resp, items)
        items = items[0].split()
        for emailid in items:
            idmail = f"b'{len(items)}'"
            if str(emailid) == idmail:
                downloaAttachmentsInEmail(m, emailid, pasta)


    #try:
    downloadAllAttachmentsInInbox(server, user, password, pasta)

    #except:
        #print('Não foi possivel baixar o relatorio, utilizaremos o relatorio antigo.')

def download_gmail():
    # pegar emails de um remetente para um destinatário
    username = 'backofficei9br@gmail.com'
    password = 'i9br12345'

    # lista de imaps: https://www.systoolsgroup.com/imap/
    meu_email = MailBox('imap.gmail.com').login(username, password)

    # criterios: https://github.com/ikvk/imap_tools#search-criteria
    lista_emails = meu_email.fetch(AND(from_="remetente", to="destinatario"))
    for email in lista_emails:
        print(email.subject)
        print(email.text)

    # pegar emails com um anexo específico
    lista_emails = meu_email.fetch(AND(from_="remetente"))
    for email in lista_emails:
        if len(email.attachments) > 0:
            for anexo in email.attachments:
                if "TituloAnexo" in anexo.filename:
                    print(anexo.content_type)
                    print(anexo.payload)
                    with open("Teste.xlsx", 'wb') as arquivo_excel:
                        arquivo_excel.write(anexo.payload)