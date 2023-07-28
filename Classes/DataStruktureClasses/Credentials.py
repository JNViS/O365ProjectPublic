from json.encoder import JSONEncoder

class Credentials:
    # This Class saves all credentials releated parameters
    tenant_id:str
    client_id:str 
    client_secret:str
    scope = []
    authority = "https://login.microsoftonline.com/"
    tokenEndPoint = "https://graph.microsoft.com/v1.0"
    selectArgs:str
    emailAddr:str

    def setCredentials(self, data):
        # This Method sets all the attributes with the data from the json file
        self.tenant_id = data["tenant_id"]
        self.client_id = data["client_id"]
        self.client_secret = data["client_secret"]
        self.scope = data["scope"]
        self.tokenEndPoint = data["tokenEndPoint"]
        self.selectArgs = data["selectArgs"]
        self.emailAddr = data["emailAddress"]
        self.authority = self.authority + self.tenant_id
        return self
        
    def __str__(self):
        return "TenantID= " + self.tenant_id + ", \nClientID= " + self.client_id + " ,\nSelectArgs= " + self.selectArgs.__str__()
        
    
class CredentialsEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
    

