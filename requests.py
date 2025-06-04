class Response:
    def __init__(self, json_data=None):
        self._json_data = json_data or {}
    def json(self):
        return self._json_data
    def raise_for_status(self):
        pass

def get(url, *args, **kwargs):
    return Response()
