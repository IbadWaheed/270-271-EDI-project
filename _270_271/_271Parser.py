import os
from datetime import datetime
from typing import List, Optional
import json
from _270_271._271Header import _271Header
from _270_271._271SBREligibilityInfo import _271SBREligibilityInfo
from _270_271._271Subscriber import _271Subscriber

class _271Parser:
    def __init__(self):
        self._counter = 0
        self.msgCounter = 0
        self.E = ' '
        self.C = ' '
        self.S = ' '
        self.R = '^'
        self.elements = []
        self.segments = []
        self.PatientEligibilityData = [_271Header]
        self.ISA06 = None
        self.ISA08 = None
        self.ISAControlNum = None
        self.GS02 = None
        self.GS03 = None
        self.GSControlNum = None
        self.Version = None
        self.ISADate = None
        self.hl_Payer = None

    def parse_271_file(self, file_path):
        self.PatientEligibilityData = []
        self._counter = 0

        if not os.path.exists(file_path):
            raise Exception(f"File {file_path} not found.")
        
        with open(file_path, 'r') as file:
            contents = file.read()

        if not contents.startswith("ISA") and len(contents) < 200:
            raise Exception(f"Invalid File {file_path}")

        self.E = contents[3]
        self.C = contents[104]
        self.S = contents[105]

        self.segments = contents.split(self.S)

        while len(self.segments) != self._counter + 1:
            self.elements = self.segments[self._counter].split(self.E)
            segment_type = self.elements[0].strip()
            
            if segment_type == "ISA":
                self.ISA06 = self.get_element(self.elements ,6)
                self.ISA08 = self.get_element(self.elements ,8)
                self.ISADate = self.get_date(self.get_element(self.elements , 9), self.get_element(self.elements ,10))
                self.ISAControlNum = self.get_element(self.elements , 13)
                self.R = self.get_element(self.elements , 11)
            elif segment_type == "GS":
                self.GS02 = self.get_element(self.elements , 2)
                self.GS03 = self.get_element(self.elements ,3)
                if len(self.elements) >= 9:
                    self.Version = self.get_element(self.elements ,8)
                self.GSControlNum = self.get_element(self.elements ,6)
            elif segment_type == "ST":
                self.parse_st()
            elif segment_type in ["SE", "GE", "IEA"]:
                pass

            self._counter += 1

        return self.PatientEligibilityData


    def parse_st(self):
        lstEB01Benefit = self.get_eb_01_benefit()
        lstEB02CoverageLevel = self.get_eb_02_coverage_level()
        lstEB03ServiceType = self.get_eb_03_service_type()
        lstEB04InsuranceType = self.get_eb_04_insurance_type()
        lstEB06TimePeriod = self.get_eb_06_time_period()
        lstEB09QuantityQual = self.get_eb_09_quantity_qualifier()
        lstEB11QuantityQual = self.get_eb_11_authorization()
        lstEB12PlanNetwork = self.get_eb_12_plan_network()
        lstRef = self.get_ref()
        lstDates = self.GET_DATE()
        lstAAA = self.get_aaa()

        value = ''

        header = _271Header()
        subscriber = _271Subscriber()
        elig_info = _271SBREligibilityInfo()

        prov_last_name = ''
        prov_first_name = ''
        prov_npi = ''

        header.ISA06SenderID = self.ISA06
        header.ISA08ReceiverID = self.ISA08
        header.ISADateTime = self.ISADate
        header.ISAControlNumber = self.ISAControlNum
        header.GS02SenderID = self.GS02
        header.GS03ReceiverID = self.GS03
        header.GSControlNumber = self.GSControlNum
        header.VersionNumber = self.Version
        
        
        if (self.get_element(self.elements , 1) != "271"):
            raise Exception("invalid File")
        
        header.STControlNumber = self.get_element(self.elements , 2)
        self._counter += 1
        st_condition = True
        while st_condition:
            self.elements = self.segments[self._counter].split(self.E)

            segment_type = self.get_element(self.elements , 0).strip()
            if segment_type == "HL":
                if self.get_element(self.elements , 3) == "20":
                    self._counter += 1
                    
                    self.hl_Payer = True
                    while self.hl_Payer:
                        self.elements = self.segments[self._counter].split(self.E)
                        segment_type = self.get_element(self.elements , 0).strip()
                        if segment_type == "NM1":
                            header.PayerOrgName = self.get_element(self.elements , 3)
                            if len(self.elements) > 8:
                                header.PayerID = self.get_element(self.elements , 9)
                        elif segment_type == "N3":
                            header.PayerAddress = self.get_element(self.elements , 1) 
                        elif segment_type == "N4":
                            header.PayerCity = self.get_element(self.elements , 1)
                            header.PayerState = self.get_element(self.elements , 2)
                            header.PayerZip = self.get_element(self.elements , 3)
                        elif segment_type == "PER":
                            if self.get_element(self.elements, 1) == "CX":
                                header.PayerContactName = self.get_element(self.elements, 2)
                                if self.get_element(self.elements, 3) == "TE":
                                    header.PayerTelephone = self.get_element(self.elements, 4)

                            elif self.get_element(self.elements, 1) == "BL":
                                header.PayerBillingContactName = self.get_element(self.elements, 2)
                                if self.get_element(self.elements, 3) == "TE":
                                    header.PayerBillingTelephone = self.get_element(self.elements, 4)
                                elif self.get_element(self.elements, 3) == "EM":
                                    header.PayerBillingEmail = self.get_element(self.elements, 4)

                                if len(self.elements) > 5:
                                    if self.get_element(self.elements, 5) == "TE":
                                        header.PayerBillingTelephone = self.get_element(self.elements, 6)
                                    elif self.get_element(self.elements, 5) == "EM":
                                        header.PayerBillingEmail = self.get_element(self.elements, 6)

                            elif self.get_element(self.elements, 1) == "IC":
                                if self.get_element(self.elements, 3) == "UR":
                                    header.PayerWebsite = self.get_element(self.elements, 4)

                                header.PayerContactName = self.get_element(self.elements, 2)
                                if self.get_element(self.elements, 3) == "TE":
                                    header.PayerTelephone = self.get_element(self.elements, 4)

                        elif segment_type == "HL":
                            self.hl_Payer = False
                            self._counter -= 1

                        if self.hl_Payer:
                            self._counter += 1    
                if self.get_element(self.elements, 3) == "21":
                   self._counter += 1
                   hlSubmitter = True
                   while hlSubmitter:
                       self.elements = self.segments[self._counter].split(self.E)
                       segment_type = self.get_element(self.elements, 0).strip()
               
                       if segment_type == "NM1":
                           provLastName = self.get_element(self.elements, 3)
                           provFirstName = self.get_element(self.elements, 4)
                           if len(self.elements) > 8:
                               provNPI = self.get_element(self.elements, 9)
                       elif segment_type == "HL":
                           hlSubmitter = False
                           self._counter -= 1
                       elif segment_type == "SE":
                           hlSubmitter = False
                           self._counter -= 1
                       
                       if hlSubmitter:
                           self._counter += 1
                           

                elif self.get_element(self.elements, 3) == "22":
                    subscriber = _271Subscriber(ProvLastName = provLastName, ProvFirstName = provFirstName, ProvNPI=provNPI)
                    
                    
                    self._counter += 1
                    hlSubscriber = True
                    while hlSubscriber:
                        self.elements = self.segments[self._counter].split(self.E)
                        segment_type = self.get_element(self.elements, 0).strip()
                
                        if segment_type == "TRN":
                            subscriber.TRN = self.get_element(self.elements, 2)
                        elif segment_type == "NM1":
                            subscriber.SBRLastName = self.get_element(self.elements, 3)
                            subscriber.SBRFirstName = self.get_element(self.elements, 4)
                            subscriber.SBRMiddleInitial = self.get_element(self.elements, 5)
                            if len(self.elements) > 8:
                                subscriber.SBRID = self.get_element(self.elements, 9)
                        elif segment_type == "REF":
                            if self.get_element(self.elements, 1) == "6P":
                                subscriber.PolicyNumber = self.get_element(self.elements, 2)
                            elif self.get_element(self.elements, 1) == "SY":
                                subscriber.SSN = self.get_element(self.elements, 2)
                        elif segment_type == "N3":
                            subscriber.SBRAddress = self.get_element(self.elements, 1)
                        elif segment_type == "N4":
                            subscriber.SBRCity = self.get_element(self.elements, 1)
                            subscriber.SBRState = self.get_element(self.elements, 2)
                            subscriber.SBRZipCode = self.get_element(self.elements, 3)
                        elif segment_type == "DMG":
                            subscriber.SBRDob = self.get_date(self.get_element(self.elements, 2), "")
                            subscriber.SBRGender = self.get_element(self.elements, 3)
                        elif segment_type == "DTP":
                            if self.get_element(self.elements, 1) == "346":
                                dt = self.get_element(self.elements, 3).split('-')
                                if len(dt) > 1:
                                    subscriber.PlanBeginDate = self.get_date(dt[0], '')
                                    subscriber.PlanEndDate = self.get_date(dt[1], '')
                                else:
                                    subscriber.PlanBeginDate = self.get_date(dt[0], '')
                            elif self.get_element(self.elements, 1) == "356":
                                dt = self.get_element(self.elements, 3).split('-')
                                if len(dt) > 1:
                                    subscriber.EligibilityBeginDate = self.get_date(dt[0], '')
                                    subscriber.EligibilityEndDate = self.get_date(dt[1], '')
                                else:
                                    subscriber.EligibilityBeginDate = self.get_date(dt[0], '')
                
                        elif segment_type == "AAA":
                            subscriber.AAA01 = self.get_element(self.elements, 1)
                            subscriber.AAA03 = self.get_element(self.elements, 3)
                            subscriber.AAA04 = self.get_element(self.elements, 4)
                            
                            value = lstAAA.get(subscriber.AAA03, "")
                            subscriber.AAAErrorMsg += "," + value
                            subscriber.AAAErrorMsg = subscriber.AAAErrorMsg.strip(',')
                
                        elif segment_type == "HL":
                            if subscriber not in header.ListOfSubscriberData:
                                header.ListOfSubscriberData.append(subscriber.__dict__)
                            hlSubscriber = False
                            self._counter -= 1
                
                        elif segment_type in ["EB", "SE", "GE"]:
                            if segment_type == "SE":
                                if subscriber not in header.ListOfSubscriberData:
                                    header.ListOfSubscriberData.append(subscriber.__dict__)
                            hlSubscriber = False
                            self._counter -= 1
                
                        if hlSubscriber:
                            self._counter += 1
                
                    if hlSubscriber:
                        self._counter += 1
            elif segment_type == "EB":
                # EB Segment processing

                msg_counter = 0
                
                
                # Adding Previous EB
                if elig_info.EB01CoverageType and elig_info not in subscriber.EligibilityData:
                    subscriber.EligibilityData.append(elig_info.__dict__)
                
                elig_info = _271SBREligibilityInfo()
                elig_info.ListOfReferenceIds = {}
                elig_info.ListOfDates = {}
                elig_info.Messages = []
                
                elig_info.EB01CoverageType = self.get_element(self.elements , 1)
                
                value = lstEB01Benefit.get(elig_info.EB01CoverageType, None)
                elig_info.EB01CoverageTypeV = value
                
                elig_info.EB02CoverageLevel = self.get_element(self.elements , 2)
                value = lstEB02CoverageLevel.get(elig_info.EB02CoverageLevel, None)
                elig_info.EB02CoverageLevelV = value
                
                elig_info.EB03ServiceTypeCode = self.get_element(self.elements , 3)
                eb03 = elig_info.EB03ServiceTypeCode.split(self.R)
                
                for s in eb03:
                    value = lstEB03ServiceType.get(s, None)
                    if elig_info.EB03ServiceTypeCodeV is None:
                        elig_info.EB03ServiceTypeCodeV = ""
                    elig_info.EB03ServiceTypeCodeV += f"{value}, " if value else ""
                elig_info.EB03ServiceTypeCodeV = elig_info.EB03ServiceTypeCodeV.strip().rstrip(',')
                
                elig_info.EB04InsuranceTypeCode = self.get_element(self.elements , 4)
                value = lstEB04InsuranceType.get(elig_info.EB04InsuranceTypeCode, None)
                elig_info.EB04InsuranceTypeCodeV = value
                
                if self.C in elig_info.EB04InsuranceTypeCode:
                    elig_info.EB04InsuranceTypeCodeList = elig_info.EB04InsuranceTypeCode.split(self.C)
                
                elig_info.EB05PlanCoverageDesc = self.get_element(self.elements , 5)
                elig_info.EB06TimePeriod = self.get_element(self.elements , 6)
                
                value = lstEB06TimePeriod.get(elig_info.EB06TimePeriod, None)
                elig_info.EB06TimePeriodV = value
                
                elig_info.EB07MonetoryAmount = self.get_element(self.elements , 7)
                elig_info.EB08BenefitPercent = self.get_element(self.elements , 8)
                
                elig_info.EB09QuanityQualifier = self.get_element(self.elements , 9)
                value = lstEB09QuantityQual.get(elig_info.EB09QuanityQualifier, None)
                elig_info.EB09QuanityQualifierV = value
                
                elig_info.EB10BenenfitQuantity = self.get_element(self.elements , 10)
                
                elig_info.EB11AuthorizationIndicator = self.get_element(self.elements , 11)
                value = lstEB11QuantityQual.get(elig_info.EB11AuthorizationIndicator, None)
                elig_info.EB11AuthorizationIndicatorV = value
                
                elig_info.EB12PlanNetworkIndicator = self.get_element(self.elements , 12)
                value = lstEB12PlanNetwork.get(elig_info.EB12PlanNetworkIndicator, None)
                elig_info.EB12PlanNetworkIndicatorV = value
                
                if len(self.elements) > 13:
                    eb13 = self.get_element(self.elements , 13).split(self.C)
                    elig_info.EB13_01_ServiceQual = eb13[0] if len(eb13) > 0 else None
                    elig_info.EB13_02_CPT = eb13[1] if len(eb13) > 1 else None
                    elig_info.EB13_03_Modifier1 = eb13[2] if len(eb13) > 2 else None
                    elig_info.EB13_04_Modifier2 = eb13[3] if len(eb13) > 3 else None
                    elig_info.EB13_05_Modifier3 = eb13[4] if len(eb13) > 4 else None
                    elig_info.EB13_06_Modifier4 = eb13[5] if len(eb13) > 5 else None
                    elig_info.EB13_07_Description = eb13[6] if len(eb13) > 6 else None
                    elig_info.EB13_08_ServiceQual = eb13[7] if len(eb13) > 7 else None
                
                if len(self.elements) > 14:
                    eb14 = self.get_element(self.elements , 14).split(self.C)
                    elig_info.EB14_01_DiagPointer1 = eb14[0] if len(eb14) > 0 else None
                    elig_info.EB14_02_DiagPointer2 = eb14[1] if len(eb14) > 1 else None
                    elig_info.EB14_03_DiagPointer3 = eb14[2] if len(eb14) > 2 else None
                    elig_info.EB14_04_DiagPointer4 = eb14[3] if len(eb14) > 3 else None
                
                self._counter += 1
                
                eb_loop = True
                while eb_loop:
                    self.elements = self.segments[self._counter].split(self.E)
                    segment_type = self.get_element(self.elements , 0).strip()
                
                    if segment_type == "HSD":
                        continue
                
                    elif segment_type == "REF":
                        value = lstRef.get(self.get_element(self.elements , 1), None)
                        if value and value not in elig_info.ListOfReferenceIds:
                            elig_info.ListOfReferenceIds[value] = self.get_element(self.elements , 1)
                
                    elif segment_type == "DTP":
                        dtp_code = self.get_element(self.elements , 1)
                        dtp_value = self.get_date(self.get_element(self.elements , 3), '')
                        if dtp_code == "096":
                            elig_info.DisChargeDate = dtp_value
                        elif dtp_code == "193":
                            elig_info.PeriodStartDate = dtp_value
                        elif dtp_code == "194":
                            elig_info.PeriodEndDate = dtp_value
                        elif dtp_code == "198":
                            elig_info.CompletionDate = dtp_value
                        elif dtp_code == "290":
                            elig_info.COBDate = dtp_value
                        elif dtp_code == "291":
                            elig_info.PlanDate = dtp_value
                        elif dtp_code == "292":
                            elig_info.BenefitBegin = dtp_value
                        elif dtp_code == "295":
                            pass
                        elif dtp_code == "304":
                            pass
                        elif dtp_code == "307":
                            elig_info.EligiblityDate = dtp_value
                        elif dtp_code == "318":
                            pass
                        elif dtp_code == "346":
                            elig_info.PlanBeginDate = dtp_value
                        elif dtp_code == "348":
                            elig_info.BenefitBegin = dtp_value
                        elif dtp_code == "349":
                            elig_info.BenefitEnd = dtp_value
                        elif dtp_code == "356":
                            elig_info.EligibilityBeginDate = dtp_value
                        elif dtp_code == "357":
                            elig_info.EligibilityEndDate = dtp_value
                        elif dtp_code == "435":
                            pass
                        elif dtp_code == "472":
                            elig_info.ServiceDate = dtp_value
                        elif dtp_code == "636":
                            pass
                        elif dtp_code == "771":
                            pass
                
                        value = lstDates.get(self.get_element(self.elements , 1), None)
                        if value and value not in elig_info.ListOfDates:
                            elig_info.ListOfDates[value] = self.get_date(self.get_element(self.elements , 3), '')
                
                    elif segment_type == "AAA":
                        elig_info.AAA01 = self.get_element(self.elements , 1)
                        elig_info.AAA03 = self.get_element(self.elements , 3)
                        elig_info.AAA04 = self.get_element(self.elements , 4)
                
                    if segment_type == "MSG":
                        self.msgCounter += 1
                        message_text = self.get_element(self.elements , 1)
                    
                        if self.msgCounter == 1:
                            elig_info.MessageText1 = message_text
                        elif self.msgCounter == 2:
                            elig_info.MessageText2 = message_text
                        elif self.msgCounter == 3:
                            elig_info.MessageText3 = message_text
                        elif self.msgCounter == 4:
                            elig_info.MessageText4 = message_text
                        elif self.msgCounter == 5:
                            elig_info.MessageText5 = message_text
                        elif self.msgCounter == 6:
                            elig_info.MessageText6 = message_text
                        elif self.msgCounter == 7:
                            elig_info.MessageText7 = message_text
                        elif self.msgCounter == 8:
                            elig_info.MessageText8 = message_text
                        elif self.msgCounter == 9:
                            elig_info.MessageText9 = message_text
                        elif self.msgCounter == 10:
                            elig_info.MessageText10 = message_text
                    
                        elig_info.Messages.append(message_text)

                    elif segment_type == "III":
                        pass
                
                    elif segment_type == "LS":
                        self._counter += 1
                        eb_ls_loop = True
                        while eb_ls_loop:
                            self.elements = self.segments[self._counter].split(self.E)
                            ls_segment_type = self.get_element(self.elements , 0).strip()
                
                            if ls_segment_type == "NM1":
                                elig_info.EBEntity = self.get_element(self.elements , 2)
                                elig_info.EBLastName = self.get_element(self.elements , 3)
                                elig_info.EBFirstName = self.get_element(self.elements , 4)
                                elig_info.EBMI = self.get_element(self.elements , 5)
                                if len(self.elements) > 9:
                                    elig_info.EBNPI = self.get_element(self.elements , 9)
                
                            elif ls_segment_type == "N3":
                                elig_info.EBAddress = self.get_element(self.elements , 1)
                
                            elif ls_segment_type == "N4":
                                elig_info.EBCity = self.get_element(self.elements , 1)
                                elig_info.EBState = self.get_element(self.elements , 2)
                                elig_info.EBZipCode = self.get_element(self.elements , 3)
                
                            elif ls_segment_type == "PER":
                                if self.get_element(self.elements , 1) == "CX":
                                    elig_info.EBContactPerson = self.get_element(self.elements , 2)
                                    if self.get_element(self.elements , 3) == "TE":
                                        elig_info.EBTelephoneNum = self.get_element(self.elements , 4)
                                elif self.get_element(self.elements , 1) == "BL":
                                    elig_info.EBBillingContactPerson = self.get_element(self.elements , 2)
                                    if self.get_element(self.elements , 3) == "TE":
                                        elig_info.EBBillingTelephoneNum = self.get_element(self.elements , 4)
                                    elif self.get_element(self.elements , 3) == "EM":
                                        elig_info.EBBillingEmail = self.get_element(self.elements , 4)
                                    if len(self.elements) > 5:
                                        if self.get_element(self.elements , 5) == "TE":
                                            elig_info.EBBillingContactPerson = self.get_element(self.elements , 5)
                                        elif self.get_element(self.elements , 5) == "EM":
                                            elig_info.EBBillingEmail = self.get_element(self.elements , 5)
                                elif self.get_element(self.elements , 1) == "IC":
                                    if self.get_element(self.elements , 3) == "UR":
                                        elig_info.EBWebsite = self.get_element(self.elements , 4)
                            elif ls_segment_type == "PRV":
                                elig_info.EBProviderType = self.get_element(self.elements , 1)
                                elig_info.EBTaxonomyCode = self.get_element(self.elements , 2)
                                            
                            elif ls_segment_type == "LE":
                                eb_ls_loop = False
                                eb_loop = False
                                self._counter -= 1
                                subscriber.EligibilityData.append(elig_info.__dict__)
                                break
                
                            if eb_loop:
                                self._counter += 1
                    elif segment_type == "HL":
                        subscriber.EligibilityData.append(elig_info.__dict__)
                        if subscriber not in header.ListOfSubscriberData:
                            header.ListOfSubscriberData.append(subscriber.__dict__)
                            eb_loop = False
                            self._counter -=1
                    elif segment_type == ["EB", "SE"]:
                        subscriber.EligibilityData.append(elig_info.__dict__)
                        eb_loop = False
                        self._counter -=1
                    if eb_loop:
                        self._counter += 1
                        
                if eb_loop:
                    self._counter += 1
            if segment_type in ["SE", "GE", "IEA"]:
                if elig_info not in subscriber.EligibilityData: 
                    subscriber.EligibilityData.append(elig_info.__dict__)
                self._counter -= 1 
                st_condition = False  
                if header not in self.PatientEligibilityData:
                    self.PatientEligibilityData.append( header.__dict__)   
            if st_condition:
               self._counter += 1
        if subscriber not in header.ListOfSubscriberData:
            header.ListOfSubscriberData.append(subscriber.__dict__)                
                
        

    
    
    def get_eb_01_benefit(self):
        eb_01_benefit = {
        "1": "Active",
        "2": "Active - Full Risk Capitation",
        "3": "Active - Services Capitated",
        "4": "Active - Services Capitated to Primary Care Physician",
        "5": "Active - Pending Investigation",
        "6": "Inactive",
        "7": "Inactive - Pending Eligibility Update",
        "8": "Inactive - Pending Investigation",
        "A": "Co-Insurance",
        "B": "Co-Payment",
        "C": "Deductible",
        "CB": "Coverage Basis",
        "D": "Benefit Description",
        "E": "Exclusions",
        "F": "Limitations",
        "G": "Out of Pocket (Stop Loss)",
        "H": "Unlimited",
        "I": "Non-Covered",
        "J": "Cost Containment",
        "K": "Reserve",
        "L": "Primary Care Provider",
        "M": "Pre-existing Condition",
        "MC": "Managed Care Coordinator",
        "N": "Services Restricted to Following Provider",
        "O": "Not Deemed a Medical Necessity",
        "P": "Benefit Disclaimer",
        "Q": "Second Surgical Opinion Required",
        "R": "Other or Additional Payor",
        "S": "Prior Year(s) History",
        "T": "Card(s) Reported Lost/Stolen",
        "U": "Contact Following Entity for Eligibility or Benefit Information",
        "V": "Cannot Process",
        "W": "Other Source of Data",
        "X": "Health Care Facility",
        "Y": "Spend Down"
    }

        return eb_01_benefit
    
    def get_eb_02_coverage_level(self):
        eb_02_coverage_level = {
        "CHD": "Children Only",
        "DEP": "Dependents Only",
        "ECH": "Employee and Children",
        "EMP": "Employee Only",
        "ESP": "Employee and Spouse",
        "FAM": "Family",
        "IND": "Individual",
        "SPC": "Spouse and Children",
        "SPO": "Spouse Only"
    }

        return eb_02_coverage_level
    
    
    def get_eb_03_service_type(self):
        eb_03_service_type = {
        "1": "Medical Care",
        "2": "Surgical",
        "3": "Consultation",
        "4": "Diagnostic X-Ray",
        "5": "Diagnostic Lab",
        "6": "Radiation Therapy",
        "7": "Anesthesia",
        "8": "Surgical Assistance",
        "9": "Other Medical",
        "10": "Blood Charges",
        "11": "Used Durable Medical Equipment",
        "12": "Durable Medical Equipment Purchase",
        "13": "Ambulatory Service Center Facility",
        "14": "Renal Supplies in the Home",
        "15": "Alternate Method Dialysis",
        "16": "Chronic Renal Disease (CRD) Equipment",
        "17": "Pre-Admission Testing",
        "18": "Durable Medical Equipment Rental",
        "19": "Pneumonia Vaccine",
        "20": "Second Surgical Opinion",
        "21": "Third Surgical Opinion",
        "22": "Social Work",
        "23": "Diagnostic Dental",
        "24": "Periodontics",
        "25": "Restorative",
        "26": "Endodontics",
        "27": "Maxillofacial Prosthetics",
        "28": "Adjunctive Dental Services",
        "30": "Health Benefit Plan Coverage",
        "32": "Plan Waiting Period",
        "33": "Chiropractic",
        "34": "Chiropractic Office Visits",
        "35": "Dental Care",
        "36": "Dental Crowns",
        "37": "Dental Accident",
        "38": "Orthodontics",
        "39": "Prosthodontics",
        "40": "Oral Surgery",
        "41": "Routine (Preventive) Dental",
        "42": "Home Health Care",
        "43": "Home Health Prescriptions",
        "44": "Home Health Visits",
        "45": "Hospice",
        "46": "Respite Care",
        "47": "Hospital",
        "48": "Hospital - Inpatient",
        "49": "Hospital - Room and Board",
        "50": "Hospital - Outpatient",
        "51": "Hospital - Emergency Accident",
        "52": "Hospital - Emergency Medical",
        "53": "Hospital - Ambulatory Surgical",
        "54": "Long Term Care",
        "55": "Major Medical",
        "56": "Medically Related Transportation",
        "57": "Air Transportation",
        "58": "Cabulance",
        "59": "Licensed Ambulance",
        "60": "General Benefits",
        "61": "In-vitro Fertilization",
        "62": "MRI/CAT Scan",
        "63": "Donor Procedures",
        "64": "Acupuncture",
        "65": "Newborn Care",
        "66": "Pathology",
        "67": "Smoking Cessation",
        "68": "Well Baby Care",
        "69": "Maternity",
        "70": "Transplants",
        "71": "Audiology Exam",
        "72": "Inhalation Therapy",
        "73": "Diagnostic Medical",
        "74": "Private Duty Nursing",
        "75": "Prosthetic Device",
        "76": "Dialysis",
        "77": "Otological Exam",
        "78": "Chemotherapy",
        "79": "Allergy Testing",
        "80": "Immunizations",
        "81": "Routine Physical",
        "82": "Family Planning",
        "83": "Infertility",
        "84": "Abortion",
        "85": "AIDS",
        "86": "Emergency Services",
        "87": "Cancer",
        "88": "Pharmacy",
        "89": "Free Standing Prescription Drug",
        "90": "Mail Order Prescription Drug",
        "91": "Brand Name Prescription Drug",
        "92": "Generic Prescription Drug",
        "93": "Podiatry",
        "94": "Podiatry - Office Visits",
        "95": "Podiatry - Nursing Home Visits",
        "96": "Professional (Physician)",
        "97": "Anesthesiologist",
        "98": "Professional (Physician) Visit - Office",
        "99": "Professional (Physician) Visit - Inpatient",
        "A0": "Professional (Physician) Visit - Outpatient",
        "A1": "Professional (Physician) Visit - Nursing Home",
        "A2": "Professional (Physician) Visit - Skilled Nursing Facility",
        "A3": "Professional (Physician) Visit - Home",
        "A4": "Psychiatric",
        "A5": "Psychiatric - Room and Board",
        "A6": "Psychotherapy",
        "A7": "Psychiatric - Inpatient",
        "A8": "Psychiatric - Outpatient",
        "A9": "Rehabilitation",
        "AA": "Rehabilitation - Room and Board",
        "AB": "Rehabilitation - Inpatient",
        "AC": "Rehabilitation - Outpatient",
        "AD": "Occupational Therapy",
        "AE": "Physical Medicine",
        "AF": "Speech Therapy",
        "AG": "Skilled Nursing Care",
        "AH": "Skilled Nursing Care - Room and Board",
        "AI": "Substance Abuse",
        "AJ": "Alcoholism",
        "AK": "Drug Addiction",
        "AL": "Vision (Optometry)",
        "AM": "Frames",
        "AN": "Routine Exam",
        "AO": "Lenses",
        "AQ": "Nonmedically Necessary Physical",
        "AR": "Experimental Drug Therapy",
        "B1": "Burn Care",
        "B2": "Brand Name Prescription Drug - Formulary",
        "B3": "Brand Name Prescription Drug - Non-Formulary",
        "BA": "Independent Medical Evaluation",
        "BB": "Partial Hospitalization (Psychiatric)",
        "BC": "Day Care (Psychiatric)",
        "BD": "Cognitive Therapy",
        "BE": "Massage Therapy",
        "BF": "Pulmonary Rehabilitation",
        "BG": "Cardiac Rehabilitation",
        "BH": "Pediatric",
        "BI": "Nursery",
        "BJ": "Skin",
        "BK": "Orthopedic",
        "BL": "Cardiac",
        "BM": "Lymphatic",
        "BN": "Gastrointestinal",
        "BP": "Endocrine",
        "BQ": "Neurology",
        "BR": "Eye",
        "BS": "Invasive Procedures",
        "BT": "Gynecological",
        "BU": "Obstetrical",
        "BV": "Obstetrical/Gynecological",
        "BW": "Mail Order Prescription Drug: Brand Name",
        "BX": "Mail Order Prescription Drug: Generic",
        "BY": "Physician Visit - Office: Sick",
        "BZ": "Physician Visit - Office: Well",
        "C1": "Coronary Care",
        "CA": "Private Duty Nursing - Inpatient",
        "CB": "Private Duty Nursing - Home",
        "CC": "Surgical Benefits - Professional (Physician)",
        "CD": "Surgical Benefits - Facility",
        "CE": "Mental Health Provider - Inpatient",
        "CF": "Mental Health Provider - Outpatient",
        "CG": "Mental Health Facility - Inpatient",
        "CH": "Mental Health Facility - Outpatient",
        "CI": "Substance Abuse Facility - Inpatient",
        "CJ": "Substance Abuse Facility - Outpatient",
        "CK": "Screening X-ray",
        "CL": "Screening laboratory",
        "CM": "Mammogram, High Risk Patient",
        "CN": "Mammogram, Low Risk Patient",
        "CO": "Flu Vaccination",
        "CP": "Eyewear and Eyewear Accessories",
        "CQ": "Case Management",
        "DG": "Dermatology",
        "DM": "Durable Medical Equipment",
        "DS": "Diabetic Supplies",
        "GF": "Generic Prescription Drug - Formulary",
        "GN": "Generic Prescription Drug - Non-Formulary",
        "GY": "Allergy",
        "IC": "Intensive Care",
        "MH": "Mental Health",
        "NI": "Neonatal Intensive Care",
        "ON": "Oncology",
        "PT": "Physical Therapy",
        "PU": "Pulmonary",
        "RN": "Renal",
        "RT": "Residential Psychiatric Treatment",
        "TC": "Transitional Care",
        "TN": "Transitional Nursery Care",
        "UC": "Urgent Care"
    }

        return eb_03_service_type
    
    
    
    def get_eb_04_insurance_type(self):
        insurance_type_dict = {
        "12": "Medicare Secondary Working Aged Beneficiary or Spouse with Employer Group Health Plan",
        "13": "Medicare Secondary End-Stage Renal Disease Beneficiary in the Mandated Coordination Period with an Employer,s Group Health Plan",
        "14": "Medicare Secondary, No-fault Insurance including Auto is Primary",
        "15": "Medicare Secondary Worker,s Compensation",
        "16": "Medicare Secondary Public Health Service (PHS) or Other Federal Agency",
        "41": "Medicare Secondary Black Lung",
        "42": "Medicare Secondary Veteran,s Administration",
        "43": "Medicare Secondary Disabled Beneficiary Under Age 65 with Large Group Health Plan (LGHP)",
        "47": "Medicare Secondary, Other Liability Insurance is Primary",
        "AP": "Auto Insurance Policy",
        "C1": "Commercial",
        "CO": "Consolidated Omnibus Budget Reconciliation Act (COBRA)",
        "CP": "Medicare Conditionally Primary",
        "D": "Disability",
        "DB": "Disability Benefits",
        "EP": "Exclusive Provider Organization",
        "FF": "Family or Friends",
        "GP": "Group Policy",
        "HM": "Health Maintenance Organization (HMO)",
        "HN": "Health Maintenance Organization (HMO) - Medicare Risk",
        "HS": "Special Low Income Medicare Beneficiary",
        "IN": "Indemnity",
        "IP": "Individual Policy",
        "LC": "Long Term Care",
        "LD": "Long Term Policy",
        "LI": "Life Insurance",
        "LT": "Litigation",
        "MA": "Medicare Part A",
        "MB": "Medicare Part B",
        "MC": "Medicaid",
        "MH": "Medigap Part A",
        "MI": "Medigap Part B",
        "MP": "Medicare Primary",
        "OT": "Other",
        "PE": "Property Insurance - Personal",
        "PL": "Personal",
        "PP": "Personal Payment (Cash - No Insurance)",
        "PR": "Preferred Provider Organization (PPO)",
        "PS": "Point of Service (POS)",
        "QM": "Qualified Medicare Beneficiary",
        "RP": "Property Insurance - Real",
        "SP": "Supplemental Policy",
        "TF": "Tax Equity Fiscal Responsibility Act (TEFRA)",
        "WC": "Workers Compensation",
        "WU": "Wrap Up Policy"
    }

        return insurance_type_dict
    
    
    
    def get_eb_06_time_period(self):
        time_period_dict = {
        "6": "Hour",
        "7": "Day",
        "13": "24 Hours",
        "21": "Years",
        "22": "Service Year",
        "23": "Calendar Year",
        "24": "Year to Date",
        "25": "Contract",
        "26": "Episode",
        "27": "Visit",
        "28": "Outlier",
        "29": "Remaining",
        "30": "Exceeded",
        "31": "Not Exceeded",
        "32": "Lifetime",
        "33": "Lifetime Remaining",
        "34": "Month",
        "35": "Week",
        "36": "Admission"
    }

        return time_period_dict
    
    
    def get_eb_09_quantity_qualifier(self):
        quantity_qualifier_dict = {
        "8H": "Minimum",
        "99": "Quantity Used",
        "CA": "Covered - Actual",
        "CE": "Covered - Estimated",
        "D3": "Number of Co-insurance Days",
        "DB": "Deductible Blood Units",
        "DY": "Days",
        "HS": "Hours",
        "LA": "Life-time Reserve - Actual",
        "LE": "Life-time Reserve - Estimated",
        "M2": "Maximum",
        "MN": "Month",
        "P6": "Number of Services or Procedures",
        "QA": "Quantity Approved",
        "S7": "Age, High Value",
        "S8": "Age, Low Value",
        "VS": "Visits",
        "YY": "Years"
    }

        return quantity_qualifier_dict
    
    
    def get_eb_11_authorization(self):
        authorization = {
        "N": "No",
        "U": "Unknown",
        "Y": "Yes"
    } 
        return authorization

    def get_eb_12_plan_network(self):
        _plan_network = {
            "N": "No",
            "U": "Unknown",
            "W": "Plan Network Does not apply",
            "Y": "Yes"
    }
        return _plan_network
    
    def get_ref(self):
        _ref = {
            "18": "Plan Number",
            "1L": "Group or Policy Number",
            "1W": "Member Identification Number",
            "49": "Family Unit Number",
            "6P": "Group Number",
            "9F": "Referral Number",
            "A6": "Employee Identification Number",
            "F6": "Health Insurance Claim Number",
            "G1": "Prior Authorization Number",
            "1G": "Insurance Policy Number",
            "N6": "Plan Network Identification Number",
            "NQ": "Medicaid Recipient Identification Number"
    }
        return _ref 
        
    
    def GET_DATE(self):
        GETDATE = {
            "096": "Discharge",
            "193": "Period Start",
            "194": "Period End",
            "198": "Completion",
            "290": "Coordination of Benefits",
            "291": "Plan",
            "292": "Benefit",
            "295": "Primary Care Provider",
            "304": "Latest Visit or Consultation",
            "307": "Eligibility",
            "318": "Added",
            "346": "Plan Begin",
            "347": "Plan End",
            "348": "Benefit Begin",
            "349": "Benefit End",
            "356": "Eligibility Begin",
            "357": "Eligibility End",
            "435": "Admission",
            "472": "Service",
            "636": "Date of Last Update",
            "771": "Status"
    }
        return GETDATE
        
    
    def get_aaa(self):
        _aa = {
            "71": "Patient Birth Date Does Not Match That for the Patient On the Database",
            "72": "Invalid/Missing Subscriber/Insured ID",
            "73": "Invalid/Missing Subscriber/Insured Name"
    }
        return _aa
        

    
    
    



 
        
    
    
    
    
    
    
    
    
    def get_element(self, array: List[str], index: int) -> str:
        if array is None or index >= len(array) or index < 0:
            return ''  # or raise an exception if preferred
        return array[index]  
    
    def get_element_as_dict(self, array: List[str], index: int) -> dict:
        message = self.get_element(array, index)  # Use existing get_element
        return {"text": message.text}  # Return as a dictionary
    def get_date(self, date_yyyymmdd: str, time_hhmm: str = '') -> Optional[datetime]:
        year = 0
        month = 0
        day = 0
        hour = 0
        minute = 0
        second = 0

        if len(date_yyyymmdd) == 6:
            year = int("20" + date_yyyymmdd[:2])
            month = int(date_yyyymmdd[2:4])
            day = int(date_yyyymmdd[4:6])
        elif len(date_yyyymmdd) == 8:
            year = int(date_yyyymmdd[:4])
            month = int(date_yyyymmdd[4:6])
            day = int(date_yyyymmdd[6:8])

        if time_hhmm:
            hour = int(time_hhmm[:2])
            minute = int(time_hhmm[2:4])

        try:
            return datetime(year, month, day, hour, minute, second)
        except ValueError:
            return None
     
    def get_element_date(self , elements: List[str], index: int) -> Optional[datetime]:
        value = None
        if len(elements) > index:
             value = self.get_date(elements[index])
        return value    

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if hasattr(o, 'to_dict'):
            return o.to_dict()
        return json.JSONEncoder.default(self, o)