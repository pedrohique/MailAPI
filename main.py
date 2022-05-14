from funcs import ler_mail
from funcs import create_file
from time import sleep
import logging
import pandas as pd

while True:
    '''faz o download do email e retorna dos dados do email e filtra os assuntos, caso o assunto esteja invalido envia
    email para a pessoa informando a finalidade do assunto'''
    emails = ler_mail.download_gmail() #
    for i in emails.keys():
        '''le os dados do email, trata os dados, e faz o envio do email informando o resultado da importação'''
        create_file.create_file(emails, i)
    sleep(60)
