from _270_271._271SBREligibilityInfo import _271SBREligibilityInfo



class _271Subscriber:
    def __init__(self, ProvLastName=None, ProvFirstName=None, ProvMI=None, ProvQual=None, ProvNPI=None):
        self.EligibilityData = []
        self.ProvEntity = None
        self.ProvLastName = ProvLastName
        self.ProvFirstName = ProvFirstName
        self.ProvMI = ProvMI
        self.ProvQual = ProvQual
        self.ProvNPI = ProvNPI

        # NM1-IL   Subscriber name
        self.SBREntityType = None
        self.SBRLastName = None
        self.SBRFirstName = None
        self.SBRMiddleInitial = None
        self.SBRID = None

        # N3, N4 Subscriber
        self.SBRAddress = None
        self.SBRCity = None
        self.SBRState = None
        self.SBRZipCode = None

        # DMG Subscriber
        self.SBRDob = None
        self.SBRGender = None
        self.SBRSSN = None

        self.PlanNumber = None
        self.PolicyNumber = None
        self.MemberID = None
        self.CaseNumber = None
        self.FamilyUnitNumber = None
        self.SSN = None

        self.AAA01 = None
        self.AAA03 = None
        self.AAA04 = None
        self.AAAErrorMsg = None

        self.DisChargeDate = None
        self.EffectiveDate = None
        self.PlanDate = None
        self.EligibilityDate = None

        self.PlanBeginDate = None
        self.PlanEndDate = None
        self.EligibilityBeginDate = None
        self.EligibilityEndDate = None
        self.ServiceDate = None

        

        # Patient details
        self.PatientLastName = None
        self.PatientFirstName = None
        self.PatientMI = None

        self.TRN = None

        # Amounts
        self.CoInsuranceAmount = None
        self.CopayAmount = None
        self.DeductibleAmount = None
    
    
    def Eligibility_Data(self , elig : _271SBREligibilityInfo ):
        self.EligibilityData.append(elig)