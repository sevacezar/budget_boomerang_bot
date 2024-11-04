class DbException(Exception):
    def __init__(self, message: str):
        self._message = message

    @property
    def message(self):
        return self._message
    
class TgException(Exception):
    def __init__(self, message: str):
        self._message = message

    @property
    def message(self):
        return self._message
    