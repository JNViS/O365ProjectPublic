from json.encoder import JSONEncoder
class Filter:
    splitter:str
    ident:str
    query:str

    def setFilterSettings(self,data):
        self.splitter = data["splitter"]
        self.ident = data["identifier"]
        self.query = data["query"]
        return self


class FilterEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__