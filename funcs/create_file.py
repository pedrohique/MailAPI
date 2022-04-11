import pandas as pd
from funcs import trat_dados
import configparser


def create_file(emails, index):
    config = configparser.ConfigParser()
    config.read('config.ini')
    caminho = config.get('DEFAULT', 'caminho_cm')
    df = emails[index]['anexos']
    empresa = emails[index]['from']
    empresa = empresa[1]
    empresa = empresa.split('@')
    empresa = empresa[1].replace('.com', '').replace('.br', '')
    data = emails[index]['data'].split(' ')
    data = data[1] + data[2] + data[3] + '-' + data[4].replace(':', '')
    tipo = emails[index]['tipo']
    #print(empresa, data, tipo)
    for i in df.values():
        df = pd.DataFrame.from_dict(i)
        if tipo == 'cadastro de funcionario':
            df = trat_dados.tratar_dados_employee(df, empresa)
        elif tipo == 'ajuste estoque':
            df = trat_dados.tratar_dados_estoque(df, empresa)
        df.to_csv(caminho + tipo.replace(' ', '') +'-'+ empresa + data + '.csv', sep=',', index=False)
        #print(type(df), df.head())
