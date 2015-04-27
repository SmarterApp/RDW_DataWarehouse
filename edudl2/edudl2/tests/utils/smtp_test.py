import asyncore
import smtpd
import threading

class SMTPTestServer(smtpd.SMTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = []

        self.thread = threading.Thread(target=asyncore.loop, kwargs={"timeout": 1})
        self.thread.daemon = True
        self.thread.start()

    def process_message(self, peer, mail_from, mail_to, data):
        self.messages.append({"mail_from": mail_from, "mail_to": mail_to, "data": data})

    def end(self):
        asyncore.close_all()
        if self.thread.is_alive():
            self.thread.join()
