class OnlineStorage:
    api_endpoint = ""
    input_callback = None
    name = ""

    def __init__(self, api_endpoint, input_callback, name):
        self.api_endpoint = api_endpoint
        self.input_callback = input_callback
        self.name = name
