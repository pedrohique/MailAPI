import pandas as pd
import configparser
import os
import logging


config = configparser.ConfigParser()
config.read('config.ini')

def tratar_dados_employee(dados, empresa):
    logging.info(f'Iniciando tratamento de dados de employee')
    #config.read('config.ini')
    try:

        siteid = config.get(empresa, 'siteid')
        dados = dados.astype(str)
        logging.info(f'Conferindo site id')
        try:
            filtro_true = dados['Employeesiteid'] == siteid
            filtro_false = dados['Employeesiteid'] != siteid
        except:
            filtro_true = dados['employeesiteid'] == siteid
            filtro_false = dados['employeesiteid'] != siteid
        dados_true = dados[filtro_true].astype(str)
        dados_false = dados[filtro_false].astype(str)#vai ser enviado por email alertando dados incorretos
        logging.info(f'Validação concluida com suceeo')
    except:
        logging.info(f'Site id invalido, retornando dados zerado')
        dados_true = pd.DataFrame()
        dados_false = pd.DataFrame()
    return dados_true, dados_false

def tratar_dados_estoque(dados, empresa):
    '''Faz o tratamento dos dados do arquivo retornando dois dataframes, dados_true = dados corretos que serão importados
    dados_false = dados incorretos que serão retornados para o usuario.'''
    logging.info(f'Tratando dados de atualização de estoque')
    def trata_crib(dados, empresa):
        '''Basicamente verifica se o crib indicado esta na lista de cribs permitidos pela empresa'''
        try:
            cribs = config.get(empresa, 'cribs').replace(' ', '')
            cribs = cribs.split(',')

            try:
                dados['Crib'].astype(str)
                filtro_true = dados['Crib'].isin(cribs)
                filtro_false = ~dados['Crib'].isin(cribs)
            except:
                dados['crib'].astype(str)
                filtro_true = dados['crib'].isin(cribs)
                filtro_false = ~dados['crib'].isin(cribs)
            dados_true = dados[filtro_true]
            dados_false = dados[filtro_false]#vai ser enviado via email alertando inconsistencia nos dados
        except:
            dados_true = pd.DataFrame()
            dados_false = pd.DataFrame()


        return dados_true, dados_false


    def trata_nan(dados):
        '''retorna todos os valores em branco do arquivo separando os dados em dois TRUE = dados corretos,
         FALSE = dados incorretos'''
        dados_false = dados[dados.isna().any(axis=1)]
        if len(dados_false.index) == 0:
            dados_false = dados[dados.isnull().any(axis=1)]
        dados_true = dados[~dados.isna().any(axis=1)]

        return dados_true, dados_false


    def trata_tipos(dados):
        '''No momento verifica se o campo quantity é um numero inteiro e retorna um df com os valores incorretos'''
        index = []
        dados_false = pd.DataFrame()
        for linha in dados.index:
            try:
                int(dados['quantity'].loc[linha])
            except:
                index.append(linha)

        for i in index:
            dados_false = pd.concat([dados.loc[i].to_frame(name=i).T, dados_false])#concatena os valores errados em um dataframe
            #Quando chamo o metodo to frame fazendo a serie virar df o mesmo retorna transposto preciso tranpor dnv
            #para que o o dataframe fique certo.
            dados = dados.drop(labels=i, axis=0)#deleta a linha do dataframe original


        dados_true = dados

        return dados_true, dados_false

    dados_true, dados_false_crib = trata_crib(dados, empresa) #peda os dados e trata por crib retornando true e false crib
    dados_true, dados_false_nan = trata_nan(dados_true)#pega os dados true tratados por crib e trata por valores em branco
    dados_false = pd.concat([dados_false_nan, dados_false_crib])# une os dois dfs de dados invalidos
    dados_true, dados_false_tipo = trata_tipos(dados_true) #trata os tipos de dados do df por enquanto apenas quantity
    dados_false = pd.concat([dados_false, dados_false_tipo]) #concatena novamente os dataframes de erros
    dados_false = dados_false.sort_index() #organiza o df por index
    dados_false['linha error'] = dados_false.index + 2 #cria uma coluna informando o index da linha no arquivo XLSX

    logging.info(f'retornando dados corretos e incorretos')
    return dados_true, dados_false

def det_acao(df, df_error):

    dados_corretos = len(df.index)
    dados_incorretos = len(df_error.index)
    logging.info(f'Verificando quantidades de dados - dados corretos:{dados_corretos}, dados incorreto: {dados_incorretos}')
    return dados_incorretos, dados_corretos


def check_arquivo(nome_arquivo, caminho): #valida se o arquivo esta na pasta sucess

    if nome_arquivo in os.listdir(caminho+'Success'):
        logging.info(f'Importação realizada com sucesso')
        return True
    else:
        logging.info(f'Importação falhada')
        return False
