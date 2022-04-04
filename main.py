from funcs import ler_mail


emails = ler_mail.download_gmail()

for i in emails.keys():
    df = emails[i]['anexos']
    print(df)