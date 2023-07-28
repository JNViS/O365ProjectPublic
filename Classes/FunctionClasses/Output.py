from msgraph.generated.models.event_collection_response import EventCollectionResponse
from msgraph.generated.models.message_collection_response import MessageCollectionResponse 

class Output:
    # This Class Outputs to Console for the extern Script
    def cleanSubjectLine(self, subject:str|None, identifier:str):
        # This Method cleans the Subjectline for easier usage in extern Script
        subject = str(subject).split(identifier)[1].replace(" ", "")
        return str(identifier + subject + identifier)

    def processingMail(self, msgs: MessageCollectionResponse|None, identifier:str):
        # This Method prints the content of the subject from a message in the console
        if msgs and msgs.value:
            for msg in msgs.value:
                if not msg.is_read:
                    print(self.cleanSubjectLine(msg.subject, identifier) + str(msg.id))

    def processingCalendarView(self, calendarView: EventCollectionResponse|None, identifier:str):
        # This Method prints the content of the subject from a event in the console
        if calendarView and calendarView.value:
            for event in calendarView.value:
                print(self.cleanSubjectLine(event.subject, identifier))