from imap_tools import MailBox, AND
import logging
import pandas as pd



def acess_mail():
    '''loga na conta e traz todos os emails que não foram visualizados'''
    username = 'backofficei9br@gmail.com'
    password = 'i9br12345'
    meu_email = MailBox('imap.gmail.com').login(username, password)
    lista_emails = meu_email.fetch(AND(seen=False))
    return lista_emails

def trata_mail(email):
    list_subject = ['cadastro de funcionários', 'cadastro de funcionario', 'cadastro de item', 'cadastro de itens', 'ajuste estoque']
    email_data = {}
    dict_anexos = {}
    if len(email.attachments) > 0 and email.subject.lower() in list_subject:
        for contagem_anex, anexo in enumerate(email.attachments):
            if anexo.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                email_data['data'] = email.date_str
                email_data['from'] = [email.from_values.name, email.from_values.email]
                email_data['tipo'] = email.subject.lower()
                df = pd.read_excel(anexo.payload)
                dict_anexos[contagem_anex] = df
                contagem_anex += 1
        email_data['anexos'] = dict_anexos
    else:
        print('enviar email falando o objetivo do sistema.')
    return email_data




def download_gmail():
    '''Filtra os emails e retorna os dados'''

    lista_emails = acess_mail()

    #lista_emails = meu_email.fetch(AND(from_="remetente"))
    dict_run = {}
    for chave, email in enumerate(lista_emails):
        email_data = trata_mail(email)
        if bool(email_data) is True:
            dict_run[chave] = email_data
    return dict_run


