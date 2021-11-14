import sqlite3
import imapclient
import pyzmail


class Storage(object):

    """Manages the storage for the downloaded mails."""

    def __init__(self):
        """Initializes the storage object. """
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def save_to_db(self, mails):
        """Saves the emails to the database.

        :emails: a list of dictionaries with information on the emails

        """
        self.create_table()
        with self.connection:
            print('Inserting only new mails.')
            sql = """INSERT OR IGNORE INTO email_received(sender, receiver, subject,
            text, html) VALUES (:sender, :receiver, :subject, :text,
            :html)"""
            self.cursor.executemany(sql, mails)


class Downloader(object):

    """Responsible for downloading the emails."""

    def __init__(self):
        """Creating the downloader. """
        print('Trying to connect to IMAP client...')
        self.imap = imapclient.IMAPClient('mail.gmail.com', ssl=True)
        self.imap.login('andreas.borowczak@gmail.com', 'quaSeu2iPs2208b')

    def save_as_dict(self, messages):
        """Saves information on the emails in a list of dictionaries.

        :messages: a list of parsed emails
        :returns: a list of dictionaries with information on each email

        """
        email_list = []
        for m in messages:
            mail = {}
            mail['sender']   = m.get_address('from')[1]
            mail['receiver'] = m.get_address('to')[1]
            mail['subject']  = m.get_subject()
            if m.text_part != None:
                mail['text_content'] = m.text_part.get_payload().decode(
                    m.text_part.charset)
            else:
                mail['text_content'] = "None"
            if m.html_part != None:
                mail['html_content'] = m.html_part.get_payload().decode(
                    m.html_part.charset)
            else:
                mail['html_content'] = "None"
            email_list.append(mail)
        print('Number of downloaded emails: ' + str(len(email_list)))
        return email_list

    def get_emails(self):
        """Looks for new mails and saves them in memory as a list of
        dictionaries.

        :returns: a list of parsed emails as dictionaries

        """
        try:
            print('Opening INBOX and looking for unseen mail.')
            self.imap.select_folder('INBOX', readonly=True)
            mails = self.imap.search(['UNSEEN'])
            raw_messages = self.imap.fetch(mails, ['BODY[]'])
            messages = [pyzmail.PyzMessage.factory(raw_messages[n][b'BODY[]'])
                        for n in raw_messages]
            email_list = self.save_as_dict(messages)
        finally:
            print('Logging out.')
            self.imap.logout()
        return email_list


def main():
    """Starts the script if run from the command line.
    """
    downloader = Downloader()
    emails = downloader.get_emails()
    storage = Storage()
    storage.save_to_db(emails)

if __name__ == "__main__":
    main()