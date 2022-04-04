from funcs import ler_mail
from funcs import  create_file
import pandas as pd


emails = ler_mail.download_gmail()

for i in emails.keys():
    create_file.create_file(emails, i)
    #print(i)
    #print(emails[i])

    # df = emails[i]['anexos']
    # empresa = emails[i]['from']
    # empresa = empresa[1]
    # empresa = empresa.split('@')
    # empresa = empresa[1].replace('.com', '').replace('.br','')
    # data = emails[i]['data'].split(' ')
    # data = data[1] + data[2] + data[3] + '-' + data[4].replace(':', '')
    # print(empresa, data)
    # for i in df.values():
    #     #print(i)
    #     df = pd.DataFrame.from_dict(i)
    #     #print(df.head())
    #     df.to_csv(empresa +'-'+ data + '.csv', sep=',')
    # #df = pd.DataFrame.from_dict(df)
    #     print(type(df), df.head())
    #print(df)