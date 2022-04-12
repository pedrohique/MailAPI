import pandas as pd
import configparser
import os
config = configparser.ConfigParser()
config.read('config.ini')

def tratar_dados_employee(dados, empresa):
    #config.read('config.ini')
    try:
        siteid = config.get(empresa, 'siteid')
        dados = dados.astype(str)
        try:
            filtro_true = dados['Employeesiteid'] == siteid
            filtro_false = dados['Employeesiteid'] != siteid
        except:
            filtro_true = dados['employeesiteid'] == siteid
            filtro_false = dados['employeesiteid'] != siteid
        dados_true = dados[filtro_true]
        dados_false = dados[filtro_false] #vai ser enviado por email alertando dados incorretos
    except:
        dados_true = pd.DataFrame()
        dados_false = pd.DataFrame()
    return dados_true, dados_false

def tratar_dados_estoque(dados, empresa):
    try:
        cribs = config.get(empresa, 'cribs').replace(' ', '')
        cribs = cribs.split(',')
        dados = dados.astype(str)
        try:
            filtro_true = dados['Crib'].isin(cribs)
            filtro_false = ~dados['Crib'].isin(cribs)
        except:
            filtro_true = dados['crib'].isin(cribs)
            filtro_false = ~dados['crib'].isin(cribs)
        dados_true = dados[filtro_true]
        dados_false = dados[filtro_false]#vai ser enviado via email alertando inconsistencia nos dados
    except:
        dados_true = pd.DataFrame()
        dados_false = pd.DataFrame()

    return dados_true, dados_false

def det_acao(df, df_error):
    dados_corretos = len(df.index)
    dados_incorretos = len(df_error.index)
    return dados_incorretos, dados_corretos


def check_arquivo(nome_arquivo, caminho):
    #for arquivo in os.listdir(caminho+'Sucess'):
    if nome_arquivo in os.listdir(caminho+'Sucess'):
        return True
    else:
        return False
