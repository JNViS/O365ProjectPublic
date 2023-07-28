from json.encoder import JSONEncoder

class ProxySettings:
    # This Class saves all proxy releated parameters
    proxyAdress = ""
    proxyPort = 0
    proxyUsername = ""
    proxyPassword = ""
    proxyType = 0
   
    def setProxySettings(self, data):
        # This Method sets all the attributes with the data from the json file
        self.proxyAdress = data["proxyAdress"]
        self.proxyPort = data["proxyPort"]
        self.proxyUsername = data["proxyUsername"]
        self.proxyPassword = data["proxyPassword"]
        self.proxyType = data["proxyType"]
        return self
        
    def __str__(self):
        return "ProxyUrl= " + self.proxyAdress + ", \nProxyPort= " + str(self.proxyPort) + " , \nProxyUsername= " + self.proxyUsername
    
class ProxyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__