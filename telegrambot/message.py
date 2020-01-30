import threading

from telegram import Bot as BotInterface


class TextMessage:
    """
    Args:
        text (:obj:`str`): Text of the message to be sent.
        delay (:obj:`int`): Time in seconds to send message after given time.
    """
    def __init__(self, text, delay=0):
        self.text = text
        self.delay_seconds = delay

    def send(self, interface: BotInterface, chat_id):
        if self.delay_seconds <= 0:
            self._send(interface, chat_id, self.text)
        else:
            def schedule():
                import sched

                s = sched.scheduler()
                s.enter(self.delay_seconds, 1, self._send,
                        argument=(interface, chat_id, self.text))
                s.run()

            thread = threading.Thread(target=schedule)
            thread.start()

    @classmethod
    def _send(cls, interface: BotInterface, chat_id, text):
        interface.send_message(chat_id=chat_id, text=text)
