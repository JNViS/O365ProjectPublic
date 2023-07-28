from .ProxySettings import ProxySettings
from .Credentials import  Credentials
from .Filter import Filter
from json.encoder import JSONEncoder
import json


class Settings:
    """This Class is a object for all other settingscontainer """
    credentials:Credentials
    proxySettings:ProxySettings
    filter:Filter

    def __init__(self, jsonPath:str):
        self.credentials = Credentials()
        self.proxySettings = ProxySettings()
        self.filter = Filter()
        self.__read_json(jsonPath)

    def setSettings(self, credentials:Credentials, proxySettings:ProxySettings, filter:Filter):
        self.credentials = credentials
        self.proxySettings = proxySettings
        self.filter = filter
        return self
    

    '''Try except is a error handler instead of crashing the script, the script will handle the fault with some alternative code.
       It will try to execute some code and if it failes than the code in the except will be executet.'''
    def __read_json(self, jsonPath:str):
        """The Method, reads all necessary parameters for the python programm from a json file """
        try:
            lastIndex:int = jsonPath.split("\\").__len__() - 1
            with open("resources\\" + jsonPath.split("\\")[lastIndex]) as json_file:
                data = json.load(json_file)
                self.filter = self.filter.setFilterSettings(data["Filter"])
                self.credentials = self.credentials.setCredentials(data["Credentials"])
                self.proxySettings = self.proxySettings.setProxySettings(data["ProxySettings"])   
        except FileNotFoundError:
            print("Exception at Settings.__read_json: Error trying to read the setttings from relative path file")
            try:
                data:any
                try:
                    with open(jsonPath) as json_file:
                        data = json.load(json_file)
                except ValueError:
                    print("Exception at Settings.__read_json: Error trying to parse settings from absolute path")
                try:
                    self.filter = self.filter.setFilterSettings(data["Filter"])
                except ValueError:
                    print("Exception at Settings.__read_json: Error trying to read the setttings from the settings file")
                try: 
                    self.credentials = self.credentials.setCredentials(data["Credentials"])
                except ValueError:
                    print("Exception at Settings.__read_json: Error trying to read the Credentials from the settings file")
                try:
                    self.proxySettings = self.proxySettings.setProxySettings(data["ProxySettings"])   
                except ValueError: 
                    print("Exception at Settings.__read_json: Error trying to read the ProxySettings from the settings file")
                
            except ValueError:
                print("Exception at Settings.__read_json: Error trying to read settings from absolute path")
                
        return self
    
class SettingsEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__