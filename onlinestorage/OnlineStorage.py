class OnlineStorage:
    api_endpoint = ""
    input_intercept = None
    name = ""

    def __init__(self, api_endpoint, input_intercept, name):
        self.api_endpoint = api_endpoint
        self.input_intercept = input_intercept
        self.name = name
