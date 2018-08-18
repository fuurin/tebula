from tebula.modules.senders.sender import BaseSender

class DummySender(BaseSender):
    def __init__(self):
        self.platform = 'Dummy'
