from funcs import ler_mail
from funcs import create_file
from time import sleep
import logging
import pandas as pd

while True:
    emails = ler_mail.download_gmail()
    for i in emails.keys():
        create_file.create_file(emails, i)
    sleep(60)
