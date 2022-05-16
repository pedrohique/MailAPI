import pandas as pd
from funcs import trat_dados
import configparser
import time
import os
from funcs import Send_Mail
import logging

def create_file(emails, index):
    logging.info(f'Iniciando processo de criação de arquivo')

    config = configparser.ConfigParser()
    config.read('config.ini')
    caminho = config.get('DEFAULT', 'caminho_cm')
    df = emails[index]['anexos'] #pega os dados do dicionario

    empresa = emails[index]['from'] #pega e trata o nome da empresa a partir do email
    empresa = empresa[1]
    email_retorno = empresa #pega o email que vai ser enviada a resposta
    empresa = empresa.split('@')
    empresa = empresa[1].replace('.com', '').replace('.br', '')

    data = emails[index]['data'].split(' ')#pega a data do envio e trata ela
    data = data[1] + data[2] + data[3] + '-' + data[4].replace(':', '')

    tipo = emails[index]['tipo']#pega o tipo da importação
    logging.info(f'email reconhecido {email_retorno}')
    for i in df.values(): #itera todos os arquivos que estão no anexo do email e converte eles para df um por vez
        df = pd.DataFrame.from_dict(i)
        if tipo == '1':
            logging.info(f'Tipo de importação - Funcionarios')
            df, df_error = trat_dados.tratar_dados_employee(df, empresa) #valida se os dados estão corretos, se estiver incorretos
            #retorna um df vazio.
        elif tipo == '2':
            logging.info(f'tipo de importação - Atualização de Estoque')
            df, df_error = trat_dados.tratar_dados_estoque(df, empresa)#valida se os dados estão corretos, se estiver incorretos
            #retorna um df vazio.

        name = 'mailAPI'+tipo.replace(' ', '') +'-'+ empresa + data + '.csv' #define o nome do arquivo

        if df.empty == False and tipo == '2':
            logging.info(f'criando arquivo na pasta update')
            df['item'] = df['item'] #esta indo com .0 a direita
            df.to_csv(caminho + name, sep=',', index=False)
        else:
            df.to_csv(caminho + name, sep=',', index=False)
        logging.info(f'Aguardando 60 segundos para virificar importação na pasta sucess')
        time.sleep(60)#tempo até conferir o arquivo na pasta
        resp = trat_dados.check_arquivo(name, caminho) #valida se o arquivo esta na pasta sucess

        if resp == True:
            logging.info(f'importação realizada com sucesso')
            Send_Mail.SendMail(emails=email_retorno, data=emails[index]['data'], status='sucess', erros=df_error, sucesso=df, tipo=tipo)
        elif resp == False:
            logging.warning(f'importação não executada.')
            Send_Mail.SendMail(emails=email_retorno, data=emails[index]['data'], status='erro002', erros=df_error, sucesso=df, tipo=tipo)



