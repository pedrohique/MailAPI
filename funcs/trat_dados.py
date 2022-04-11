import pandas as pd
import configparser
import os
config = configparser.ConfigParser()
config.read('config.ini')

def tratar_dados_employee(dados, empresa):
    #config.read('config.ini')
    siteid = config.get(empresa, 'siteid')
    dados = dados.astype(str)
    filtro_true = dados['Employeesiteid'] == siteid
    filtro_false = dados['Employeesiteid'] != siteid
    dados_true = dados[filtro_true]
    dados_false = dados[filtro_false] #vai ser enviado por email alertando dados incorretos
    return dados_true, dados_false

def tratar_dados_estoque(dados, empresa):
    cribs = config.get(empresa, 'cribs').replace(' ', '')
    cribs = cribs.split(',')
    dados = dados.astype(str)
    filtro_true = dados['Crib'].isin(cribs)
    filtro_false = ~dados['Crib'].isin(cribs)
    dados_true = dados[filtro_true]
    dados_false = dados[filtro_false]#vai ser enviado via email alertando inconsistencia nos dados
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
