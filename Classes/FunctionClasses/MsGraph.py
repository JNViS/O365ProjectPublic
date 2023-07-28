from azure.identity import ClientSecretCredential
from kiota_authentication_azure.azure_identity_authentication_provider import AzureIdentityAuthenticationProvider
from msgraph import GraphRequestAdapter
from msgraph import GraphServiceClient
from httpx._types import ProxiesTypes
import httpx
from Classes.DataStruktureClasses.ProxySettings import ProxySettings
from Classes.DataStruktureClasses.Credentials import Credentials 
import logging

class MsGraph:
    # This Class is a Collection of methods needed for authorization and connection
    proxySettings: ProxySettings
    credentials: Credentials

    #Class needs only a call to the constructor (instance creater) for the class to Work
    def __init__(self, proxySettings:ProxySettings, credentials:Credentials):
        self.proxySettings = proxySettings
        self.credentials = credentials

    #Public Methods

    #Protected Methods

    def _getToken(self):
        # This Method returns a GraphServiceClient object that is needed, if the python script is behind a proxy
        if(not(self.proxySettings.proxyUsername == "" and self.proxySettings.proxyPassword == "")):
            return self.__getTokenProxyCredentials()
        if(not(self.proxySettings.proxyAdress == "" and self.proxySettings.proxyPort == "")):
            return self.__getTokenProxy()
        
        return self.__getTokenNoProxy() 
    
    # Private Methods
    def __getAuthUrl(self):
        return self.credentials.authority + self.credentials.tenant_id

    def __getClientSecretCredential(self):
        # This Method returns a Client object with the necessary credentials
        credential:ClientSecretCredential = ClientSecretCredential(
            self.credentials.tenant_id,
            self.credentials.client_id,
            self.credentials.client_secret
            )
        return credential
    
    def __getTokenNoProxy(self):
        # This Method returns a GraphServiceClient object that has no proxy
        logging.info('Trying to acquire Access Token') 
        auth_provider = AzureIdentityAuthenticationProvider(self.__getClientSecretCredential(), scopes=self.credentials.scope)
        request_adapter = GraphRequestAdapter(auth_provider)
        return GraphServiceClient(request_adapter)

    def __getTokenProxy(self):
        # This Method returns a GraphServiceClient object that has a proxy address and a port 
        logging.info('Trying to acquire Access Token')
        adress = str(self.proxySettings.proxyAdress) + ":" + str(self.proxySettings.proxyPort)
        proxies: ProxiesTypes = {"http://": "http://" + adress, "https://": "http://" + adress} 
        http_client = httpx.Client(proxies=proxies)
        auth_provider = AzureIdentityAuthenticationProvider(self.__getClientSecretCredential(), scopes=self.credentials.scope)
        request_adapter = GraphRequestAdapter(auth_provider)
        return GraphServiceClient(request_adapter)

    def __getTokenProxyCredentials(self):
        # This Method returns a GraphServiceClient object that has a proxy address and a port and credentials
        logging.info('Trying to acquire Access Token')
        adress = self.proxySettings.proxyUsername + ":" + self.proxySettings.proxyPassword + "@" + self.proxySettings.proxyAdress + ":" + str(self.proxySettings.proxyPort)
        proxies: ProxiesTypes = {"http://": "http://" + adress, "https://": "http://" + adress} 
        http_client = httpx.Client(proxies=proxies)
        auth_provider = AzureIdentityAuthenticationProvider(self.__getClientSecretCredential(), scopes=self.credentials.scope)
        request_adapter = GraphRequestAdapter(auth_provider)
        return GraphServiceClient(request_adapter)

