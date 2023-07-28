from msgraph.generated.users.item.messages.messages_request_builder import MessagesRequestBuilder
from msgraph.generated.users.item.calendar_view.calendar_view_request_builder import CalendarViewRequestBuilder
from msgraph.generated.users.item.messages.item.message_item_request_builder import MessageItemRequestBuilder
from msgraph.generated.models.message import Message
from .DataStruktureClasses.Filter import Filter
from msgraph import GraphServiceClient
from Classes.FunctionClasses.MsGraph import MsGraph
from .DataStruktureClasses.Settings import Settings
from .DataStruktureClasses.Credentials import Credentials
from datetime import datetime
from Classes.FunctionClasses.Output import Output
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class GraphFunc(MsGraph):

    client: GraphServiceClient
    output:Output
    settings:Settings
    credentials:Credentials
    filter:Filter

    __filterStart:str = "contains(subject,\'"
    __filterEnd:str = "\')"
    __filter:str

    def __init__(self, jsonPath:str, msgIdStr:str): 
        # Calls the Parent class MsGraph to init the settings
        self.settings = Settings(jsonPath)
        self.credentials = self.settings.credentials
        self.filter = self.settings.filter
        Token = MsGraph(self.settings.proxySettings, self.credentials)
        self.__filter = self.__filterStart + self.filter.ident + self.__filterEnd
        # Calls the Parent class and gets a Token back for accessing the API
        self.client  = Token._getToken()
        # Initialisiert das Objekt output
        self.output = Output()
        
        # Checks if a Message ID was given
        if msgIdStr != "":
            # Starts a Routine for Updating the processed Email to read
            asyncio.run(self.routineUpdateToRead(msgIdStr))
            return
        # Calls the default Routine if no Message ID was given as an Argument
        asyncio.run(self.routineDefault())
        
    async def getMailboxInfo(self):
        # Trys to get the Mailbox Info
        try:
            # Gets the Email from Parent Class that has the Settings Class, to identifie the right Mailbox
            user = await self.client.users.by_user_id(self.settings.credentials.emailAddr).get()
            return user
        except:
            # If something failed a Error Message will be displayed
            print("Exception at GraphFunc.getMailboxInfo: Error trying to get Data from API")

    async def getCalendarView(self):
        # Creates Strings filter a CalendarView
        currentTime = str(datetime.utcnow().isoformat() + 'Z').split("T")[0]
        startTime = currentTime + "T00:00:00"
        endTime = currentTime + "T23:59:59"
        # Sets the Query for the CalendarView in a RequestBuilder
        query_param = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetQueryParameters(
            start_date_time=startTime, end_date_time=endTime, filter=self.__filter
        )
        request_config = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetRequestConfiguration(query_parameters=query_param)
        # Trys to get a CalendarView(a list of Events)
        try:
            # Gets the Email from Parent Class that has the Settings Class, to identifie the right Mailbox 
            calendarView = await self.client.users.by_user_id(self.credentials.emailAddr).calendar_view.get(request_config)
            return calendarView
        except:
            # If something failed a Error Message will be displayed
            print("Exception at GraphFunc.getCalendarView: Error trying to get Data from API")

    async def getMessage(self):
        # Header configuration for getting mails back in text form instead of HTML
        query_param = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            filter=self.__filter + " AND isRead eq false"
        )
        # Sets the header to prefer the resulting message body to use text instead of html
        request_config = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
                headers={"prefer": "outlook.body-content-type=text"}, query_parameters=query_param
            )
        try:
            # Gets the Email from Parent Class that has the Settings Class, to identifie the right Mailbox 
            messages = await self.client.users.by_user_id(self.credentials.emailAddr).messages.get(request_configuration=request_config)
            return messages
        except:
            # If something failed a Error Message will be displayed
            print("Exception at GraphFunc.getMessage: Error trying to get Data from API")
        
    
    async def updateMailtoRead(self,msgId):
        # This Method creates nessecary configurations and sends the mark read 
        post_config = MessageItemRequestBuilder.MessageItemRequestBuilderPatchRequestConfiguration(
            headers={"Content-Type": "application/json"}
        )
        # Create a Message and set the Message to Read
        request_body = Message()
        request_body.is_read = True
        try:
            # Uses Patch to set the Mail with the ID to read(only read is set in the request_body) patches the set attr in the existing message on the mailbox
            response = await self.client.users.by_user_id(self.credentials.emailAddr).messages.by_message_id(msgId).patch(request_body,request_configuration=post_config)
            return response
        except:
            print("Exception at GraphFunc.updateMailtoRead: Failed to set Mail to read")

    async def routineUpdateToRead(self,msgIdStr:str):
        try:
            # Splits the msgIdStr with the identifier
            msgIdList = msgIdStr.split(self.filter.splitter)
            counter = 1
            for id in msgIdList:
                # Breaks out of the foreach loop if a entry is empty
                if id == "":
                    break
                # Calls the Method updateMailtoRead with the arg id
                task = asyncio.create_task(self.updateMailtoRead(id))
                response = await task
                # If response contains a msg and is is_read == true then the update is complete else it failed
                if response.is_read == True: # type: ignore 
                    print ("#" + str(counter) + "\tUpdate complete")
                else:
                    print("#" + str(counter) + "\tUpdate failed")
                counter += 1
        except:
            print ("Exception at GraphFunc.routineupdatetoRead: General Failure")
        

    async def routineDefault(self):
        #Create Threads and call method
        try:
            iTask = asyncio.create_task(self.getMailboxInfo())
            mTask = asyncio.create_task(self.getMessage())
            cTask = asyncio.create_task(self.getCalendarView())
            # Call methods after finishing method in Thread
            info = await iTask
            messages = await mTask
            calendarView = await cTask
            self.output.processingMail(messages, self.filter.ident)
            self.output.processingCalendarView(calendarView, self.filter.ident)
        except:
            print("Exception at GraphFunc.routine")    