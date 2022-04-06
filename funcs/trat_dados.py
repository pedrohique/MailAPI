import pandas as pd
import configparser
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
    #print(dados_false.head())
    return dados_true

def tratar_dados_estoque(dados, empresa):
    cribs = config.get('i9brgroup', 'cribs').replace(' ', '')
    cribs = cribs.split(',')
    dados = dados.astype(str)
    #print(cribs, type(cribs[0]))
    filtro_true = dados['Crib'].isin(cribs)
    filtro_false = ~dados['Crib'].isin(cribs)
    dados_true = dados[filtro_true]
    dados_false = dados[filtro_false]#vai ser enviado via email alertando inconsistencia nos dados
    return dados_true



