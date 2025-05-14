
from _270_271._271Subscriber import _271Subscriber

class _271Header:
    def __init__(self):
        self.ISA06SenderID = None
        self.ISA08ReceiverID = None
        self.ISADateTime = None
        self.ISAControlNumber = None
        self.GS02SenderID = None
        self.GS03ReceiverID = None
        self.GSControlNumber = None
        self.STControlNumber = None
        self.VersionNumber = None

        # Information Source
        self.PayerOrgName = None
        self.PayerFirstName = None
        self.PayerID = None
        self.PayerAddress = None
        self.PayerCity = None
        self.PayerState = None
        self.PayerZip = None
        self.PayerContactName = None
        self.PayerTelephone = None
        self.PayerBillingContactName = None
        self.PayerBillingEmail = None
        self.PayerBillingTelephone = None
        self.PayerWebsite = None
        self.ListOfSubscriberData = []
                
    def  List_Of_Subscriber_Data(self , sbr :_271Subscriber):
        self.ListOfSubscriberData.append(sbr)  

        

# Assuming you have _271Subscriber class somewhere, 
# you'll need to implement or import that as well.
