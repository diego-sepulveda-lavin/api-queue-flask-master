from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import os

from twilio.rest import Client


class Queue:

    def __init__(self):
        #CONGIG TWILIO
        self.account_sid = os.environ.get('ACCOUNT_SID')
        self.auth_token = os.environ.get('AUTH_TOKEN')
        self.client = Client(self.account_sid, self.auth_token)

        self._queue = [{'nombre': 'Pedro'},{'nombre': 'Juan'}]
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'LIFO'

    def enqueue(self, new_user):
        self._queue.append(new_user)
        self.send_sms_added(new_user)

    def dequeue(self):
        if self._mode == 'FIFO':
            if self._queue:
                processed_user = self._queue.pop(0)
                self.send_sms_processed(processed_user)
                return processed_user
            else:
                return None
        elif self._mode == 'LIFO':
            if self._queue:
                processed_user = self._queue.pop(-1)
                self.send_sms_processed(processed_user)
                return processed_user
            else:
                return None

    def get_queue(self):
        return self._queue

    def size(self):
        return len(self._queue)

    def send_sms_added(self,new_user):
        if self._mode == 'FIFO':
            message = self.client.messages.create(
                body=f"Estimado(a) {new_user['nombre']}, en la lista de espera hay {self.size()-1} usuarios antes que tú.",
                from_=os.environ.get('PHONE'),
                to=os.environ.get('USERPHONE')
             )
            print(message.sid)
        elif self._mode == 'LIFO':
            message = self.client.messages.create(
                body=f"Estimado(a) {new_user['nombre']}, eres el/la próximo(a) usuario(a) que será atendido(a).",
                from_=os.environ.get('PHONE'),
                to=os.environ.get('USERPHONE')
             )
            print(message.sid)
    
    def send_sms_processed(self,processed_user):
        message = self.client.messages.create(
                body=f"Estimado(a) {processed_user['nombre']}, es tu turno de atención, por favor dirígete al mesón de atención.",
                from_=os.environ.get('PHONE'),
                to=os.environ.get('USERPHONE')
             )
        print(message.sid)
        

