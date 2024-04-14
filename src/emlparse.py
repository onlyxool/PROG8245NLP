import os
import re
import eml_parser
import pandas as pd
from bs4 import BeautifulSoup


def msg_to_text(msg_path):
    with open(msg_path, 'rb') as fhdl:
        raw_email = fhdl.read()

    ep = eml_parser.EmlParser(include_raw_body=True)
    parsed_eml = ep.decode_email_bytes(raw_email)

    subject = parsed_eml['header']['subject']
    bodys = ''

    for body in parsed_eml['body']:
        if 'html' in body['content'].lower():
            bodys = bodys + BeautifulSoup(body['content'], 'html.parser').get_text()
        else:
            bodys = bodys + body['content']

    return subject, bodys


def search_eml(path):
    models, models_path = list(), list()
    current_folder = os.walk(path)
    for path, dir_list, file_list in current_folder:
        for file_name in file_list:
            file_abs = path+'\\'+file_name
            models.append(file_name)
            models_path.append(file_abs)

    return models, models_path


def convert(path):
    data = list()

    models, models_path = search_eml(path)
    for index, model_path in enumerate(models_path):
        subject, bodys = msg_to_text(model_path)

        # Remove punctuation marks and convert to lowercase
        subject = re.sub(r'[^\w\s]', ' ', subject.lower())
        bodys = re.sub(r'[^\w\s]', ' ', bodys.lower())

        # Remove escape character
        subject = subject.replace('\n', ' ')
        bodys = bodys.replace('\n', ' ')
        subject = subject.replace('\r', ' ')
        bodys = bodys.replace('\r', ' ')

        # Ignore the empty string
        if subject == '' or bodys == '':
            continue

        # Ignore the long string
        if len(subject) > 30000 or len(bodys) > 30000:
            continue

        # Check if a string contains chinese character
        if len(re.findall(r'[\u4e00-\u9fff]+', subject+'\n'+bodys)) > 0:
            continue
        else:
            try:
                data.append([subject, bodys])
            except:
                continue

    data = pd.DataFrame(data, columns=['Subject', 'Content'])
    data.to_csv('D:\\workspace\\conestoga\\PROG8245\\Project\\PROG8245NLP\\csv\\mail.csv')

convert('D:\\workspace\\conestoga\\PROG8245\\Project\\bckgmail\\GMAIL')