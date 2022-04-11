import pandas as pd
from funcs import trat_dados
import configparser
import time
import os
from funcs import Send_Mail

def create_file(emails, index):
    config = configparser.ConfigParser()
    config.read('config.ini')
    caminho = config.get('DEFAULT', 'caminho_cm')
    df = emails[index]['anexos']
    empresa = emails[index]['from']
    empresa = empresa[1]
    email_retorno = empresa
    empresa = empresa.split('@')
    empresa = empresa[1].replace('.com', '').replace('.br', '')
    data = emails[index]['data'].split(' ')
    data = data[1] + data[2] + data[3] + '-' + data[4].replace(':', '')
    tipo = emails[index]['tipo']
    #print(empresa, data, tipo)
    for i in df.values():
        df = pd.DataFrame.from_dict(i)
        if tipo == '1':
            df, df_error = trat_dados.tratar_dados_employee(df, empresa)
            #dados_incorretos, dados_corretos = trat_dados.det_acao(df, df_error)
        elif tipo == '2':
            df, df_error = trat_dados.tratar_dados_estoque(df, empresa)
            #dados_incorretos, dados_corretos = trat_dados.det_acao(df, df_error)

        name = tipo.replace(' ', '') +'-'+ empresa + data + '.csv'
        df.to_csv(caminho + name, sep=',', index=False)
        time.sleep(10)
        resp = trat_dados.check_arquivo(name, caminho)
        print(name)
        if resp == True:
            Send_Mail.SendMail(emails=email_retorno, data=emails[index]['data'], status='sucess', erros=df_error, sucesso=df, tipo=tipo)
        elif resp == False:
            Send_Mail.SendMail(emails=email_retorno, data=emails[index]['data'], status='erro002', erros=df_error, sucesso=df, tipo=tipo)

        #print(type(df), df.head())


