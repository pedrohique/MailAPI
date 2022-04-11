# encoding: utf-8
import cryptocode #descriptografa a senho do config file
import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from funcs import trat_dados


class SendMail:

    def __init__(self, emails, data, status, erros, sucesso, tipo):
        config = configparser.ConfigParser()
        config.read('config.ini')
        '''pega a chave do password e desencrypta'''
        key = 'i9brgroup'
        password_cript = config.get('enviar_email', 'password')
        password = cryptocode.decrypt(password_cript, key)

        self.emails = emails
        self.host = config.get('enviar_email', 'server')
        self.port = config.get('enviar_email', 'port')
        self.user = config.get('enviar_email', 'user')
        self.password = password
        self.status = status
        self.data = data
        self.erros = erros
        self.sucesso = sucesso
        self.tipo = tipo




        if type(self.emails) != list:
            self.emails = self.emails.split(',')

        def tratar_data(data_obj):
            data_str = data_obj.strftime("%d/%m/%Y %H:%M:%S")
            return data_str

        def Change_html(status, data,  erros, tipo, sucesso):
            arquivo = config.get('enviar_email', 'html_caminho')
            print(data)
            if type(data) != str:
                data_last = tratar_data(data)
            else:
                data_last = data

            if status == 'erro001':
                arquivo = 'funcs/html/HTML_erro001.html'
                with open(arquivo, encoding='utf-8') as arc:
                    soup = BeautifulSoup(arc, "html.parser", from_encoding=["latin-1", "utf-8"])
                    soup.data.replace_with(str(data_last)) #muda a data da ultima conexão
                    #soup.n_enviados.replace_with(str(erros))

                    #print(soup.prettify())
            elif status == 'erro002':
                arquivo = 'funcs/html/HTML_erro002.html'
                with open(arquivo, encoding='utf-8') as arc:
                    soup = BeautifulSoup(arc, "html.parser", from_encoding=["latin-1", "utf-8"])
                    soup.data.replace_with(str(data_last))  # muda a data da ultima conexão
                    # soup.n_enviados.replace_with(str(erros))
            elif status == 'sucess':
                qtd_fail, qtd_sucess= trat_dados.det_acao(sucesso, erros)

                arquivo = 'funcs/html/HTML_sucesso.html'
                with open(arquivo, encoding='utf-8') as arc:
                    soup = BeautifulSoup(arc, "html.parser", from_encoding=["latin-1", "utf-8"])
                    soup.data.replace_with(str(data_last))
                    soup.qtd_sucess.replace_with(str(qtd_sucess))
                    soup.qtd_fail.replace_with(str(qtd_fail))


                    # soup.n_enviados.replace_with(str(erros))

            return soup.decode()


        def Sender(server, user, password, port, emails, status, erros, tipo, sucesso):
            def connect(server, user, password, port): #conect
                con = smtplib.SMTP(server, port)
                con.login(user, password)
                return con

            def body(user, soup, emails): #edita o email
                message = soup
                email_msg = MIMEMultipart()
                email_msg['From'] = user
                email_msg['To'] = ','.join(emails) #o problema de passar emails em lista é o cabeçalho que só aceita strings
                email_msg['Subject'] = f'RESPOSTA API - I9BRGROUP'
                email_msg.attach(MIMEText(message, 'html'))
                return email_msg

            def send(con, msg, emails): #envia o email
                de = msg['From']
                to = emails #aqui pode ser passado uma lista de emails.
                if len(emails) > 0 and emails[0] != '':
                    con.sendmail(de, to, msg.as_string())
                con.quit()

            soup = Change_html(status, data, erros, tipo, sucesso)
            con = connect(server, user, password, port)
            msg = body(user,soup, emails)
            if len(emails) > 0:
                send(con, msg, emails)
                print('email enviado', emails)
            return 'email enviado com sucesso.'


        self.resp = Sender(self.host, self.user, self.password, self.port, self.emails, self.status, self.erros, self.tipo, self.sucesso)










