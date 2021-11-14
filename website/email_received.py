import email
import imaplib
import pandas as pd



EMAIL = 'andreas.borowczak@gmail.com'
PASSWORD = 'quaSeu2ips2208b'
SERVER = 'imap.gmail.com'

von = []
betreff = []
inhalt = []

mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)

mail.select('inbox')

status, data = mail.search(None, 'ALL')

mail_ids = []

for block in data:
    mail_ids += block.split()

for i in mail_ids:
    status, data = mail.fetch(i, '(RFC822)')

    for response_part in data:

        if isinstance(response_part, tuple):
            message = email.message_from_bytes(response_part[1])

            mail_from = message['from']
            mail_subject = message['subject']

            if message.is_multipart():
                mail_content = ''

                for part in message.get_payload():

                    if part.get_content_type() == 'text/plain':
                        mail_content += part.get_payload()
            else:

                mail_content = message.get_payload()

            von.append(f'From: {mail_from}')
            betreff.append(f'Subject: {mail_subject}')
            inhalt.append(f'Content: {mail_content}')
            # print(f'From: {mail_from}')
            # print(f'Subject: {mail_subject}')
            # print(f'Content: {mail_content}')
email = pd.DataFrame({'Sender': von, 'Betreff': betreff, 'Text': inhalt})
email.to_excel('email..xlsx', index=False)