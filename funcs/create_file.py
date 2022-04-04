import pandas as pd

def create_file(emails, index):
    print(emails)
    df = emails[index]['anexos']
    empresa = emails[index]['from']
    empresa = empresa[1]
    empresa = empresa.split('@')
    empresa = empresa[1].replace('.com', '').replace('.br', '')
    data = emails[index]['data'].split(' ')
    data = data[1] + data[2] + data[3] + '-' + data[4].replace(':', '')
    print(empresa, data)
    for i in df.values():
        # print(i)
        df = pd.DataFrame.from_dict(i)
        # print(df.head())
        df.to_csv(empresa + '-' + data + '.csv', sep=',')
        # df = pd.DataFrame.from_dict(df)
        print(type(df), df.head())
