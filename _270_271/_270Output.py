from datetime import *




class Output:
    def __init__(self):
        self.Transaction270 = None
        self.ErrorMessage = None
        self.ProcessedRequests = 0
        self.Results = []  # List to store EligResult objects
        self.FileSubmittedToFTP = False
        self.FTPFileName = None

    class EligResult:
        def __init__(self, TRNNumber=None, Processed=False, ValidationMsg=None, ProcessedDate=None):
            self.ValidationMsg = ValidationMsg
            self.TRNNumber = TRNNumber
            self.Processed = Processed
            self.ProcessedDate = ProcessedDate if ProcessedDate else datetime.now()