from funcs import ler_mail
from funcs import create_file
from time import sleep
import logging
import pandas as pd

logging.basicConfig(filename='logFile_relat.log',  level=logging.DEBUG, filemode='w+',
                        format='%(asctime)s - %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')


while True:
    '''faz o download do email e retorna dos dados do email e filtra os assuntos, caso o assunto esteja invalido envia
    email para a pessoa informando a finalidade do assunto'''
    logging.info(f'Iniciando programa')
    emails = ler_mail.download_gmail() #
    for i in emails.keys():
        '''le os dados do email, trata os dados, e faz o envio do email informando o resultado da importação'''
        create_file.create_file(emails, i)
    sleep(60)
