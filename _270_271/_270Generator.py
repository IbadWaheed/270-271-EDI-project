import os
import json
from datetime import datetime
import time

from _270_271._270Header import *
from _270_271._270Header import _270Header
from _270_271._270Output import *
from _270_271._270Data import _270Data

class _270Generator:
        
    def __init__(self):
        self.e = '*'
        self.s = '~'
        self.c = ':'
        self.r = '^'
        self.d = datetime.now
    
    

    def prepare_model(self, header_data):
        header = _270Header()

        # Mapping simple header fields
        header.isa_01_auth_qual = header_data.get("isa_01_auth_qual", "00")
        header.isa_02_auth_info = header_data.get("isa_02_auth_info", "").ljust(10, ' ')
        header.isa_03_sec_qual = header_data.get("isa_03_sec_qual", "00")
        header.isa_04_sec_info = header_data.get("isa_04_sec_info", "").ljust(10, ' ')
        header.isa_05_sender_qual = header_data.get("isa_05_sender_qual", "ZZ")
        header.isa_06_sender_id = header_data.get("isa_06_sender_id", "")
        header.isa_07_receiver_qual = header_data.get("isa_07_receiver_qual", "ZZ")
        header.isa_08_receiver_id = header_data.get("isa_08_receiver_id", "")
        header.isa_13_control_number = header_data.get("isa_13_control_number", "")
        header.isa_15_usage_indicator = header_data.get("isa_15_usage_indicator", "P")
        header.gs_02_sender_id = header_data.get("gs_02_sender_id", "")
        header.gs_03_receiver_id = header_data.get("gs_03_receiver_id", "")
        
        
        # Mapping list of Eligibility Data
        header.list_Of_Eligibility_Data = []
        elig_data_list = header_data.get("list_Of_Eligibility_Data", [])
        
        for elig_data in elig_data_list:
            data = _270Data()
            
            # Mapping Payer Information
            data.payer_org_name = elig_data.get("payer_org_name", "")
            data.payer_id = elig_data.get("payer_id", "")
            
            # Mapping Provider Information
            data.prov_last_name = elig_data.get("prov_last_name", "")
            data.prov_first_name = elig_data.get("prov_first_name", "")
            data.prov_mi = elig_data.get("prov_mi", "")
            data.prov_npi = elig_data.get("prov_npi", "")
            data.prov_taxonomy_code = elig_data.get("prov_taxonomy_code", "")
            
            # Mapping Subscriber Information
            data.sbr_last_name = elig_data.get("sbr_last_name", "")
            data.sbr_first_name = elig_data.get("sbr_first_name", "")
            data.sbr_middle_initial = elig_data.get("sbr_middle_initial", "")
            data.sbr_id = elig_data.get("sbr_id", "")
            
            data.sbr_address = elig_data.get("sbr_address", "")
            data.sbr_city = elig_data.get("sbr_city", "")
            data.sbr_state = elig_data.get("sbr_state", "")
            data.sbr_zip_code = elig_data.get("sbr_zip_code", "")
            data.sbr_dob = elig_data.get("sbr_dob", "")
            data.sbr_gender = elig_data.get("sbr_gender", "")
            data.sbr_ssn = elig_data.get("sbr_ssn", "")
            
            # Mapping Patient Information
            data.patient_relation_value = elig_data.get("patient_relation_value", "18")
            data.pat_last_name = elig_data.get("pat_last_name", "")
            data.pat_first_name = elig_data.get("pat_first_name", "")
            data.pat_middle_initial = elig_data.get("pat_middle_initial", "")
            data.pat_address = elig_data.get("pat_address", "")
            data.pat_city = elig_data.get("pat_city", "")
            data.pat_state = elig_data.get("pat_state", "")
            data.pat_zip_code = elig_data.get("pat_zip_code", "")
            data.pat_dob = elig_data.get("pat_dob", "")
            data.pat_gender = elig_data.get("pat_gender", "")
            data.service_type_codes = elig_data.get("service_type_codes", "30")
            # Mapping TRN Information
            data.trn01 = elig_data.get("trN01", "")
            
            # Mapping Eligibility Date
            data.eligibility_for_date = elig_data.get("eligibility_for_date", "")
            
            # Append each _270Data instance to the list
            header.list_Of_Eligibility_Data.append(data)
        
        return header


    def Generate270(self, header):
        output = Output()
        
        if not (self.is_null_or_empty(header)):
            
         if (header is None or header.list_Of_Eligibility_Data is None):
             output.ErrorMessage = 'header, Subscriber data cannot be empty.'
         if (self.is_null_or_empty(header.isa_13_control_number)):
             output.ErrorMessage = 'ISA13CntrlNumber feild cannot be empty'
         if (self.is_null(header.isa_15_usage_indicator)):
             output.ErrorMessage = 'ISA15 Usage Indicator can not be Empty.'   
         
         if self.is_null != output.ErrorMessage:
            
          E = self.e
          S = self.s
        
          header.isa_01_auth_qual = "00" if not header.isa_01_auth_qual else header.isa_01_auth_qual.zfill(2)
          header.isa_02_auth_info = "".ljust(10) if not header.isa_02_auth_info else header.isa_02_auth_info.ljust(10)
          header.isa_03_sec_qual = "00" if not header.isa_03_sec_qual else header.isa_03_sec_qual.zfill(2)
          header.isa_04_sec_info = "".ljust(10) if not header.isa_04_sec_info else header.isa_04_sec_info.ljust(10)
          header.isa_05_sender_qual = "ZZ" if not header.isa_05_sender_qual else header.isa_05_sender_qual.zfill(2)
          header.isa_07_receiver_qual = "ZZ" if not header.isa_07_receiver_qual else header.isa_07_receiver_qual.zfill(2)
  
          header.isa_13_control_number = header.isa_13_control_number.zfill(9)[:9]
          
          eligRequest = ""
          eligRequest += "ISA" + E + header.isa_01_auth_qual + E + header.isa_02_auth_info + E + header.isa_03_sec_qual + E + header.isa_04_sec_info + E + header.isa_05_sender_qual + E
          eligRequest += header.isa_06_sender_id.ljust(15, ' ') + E + header.isa_07_receiver_qual + E + header.isa_08_receiver_id.ljust(15, ' ') + E
          eligRequest += self.D_YYMMDD("%y%m%d") + E + self.T_HHMM("%H%M") + E + self.r + E + "00501" + E + header.isa_13_control_number + E + "1" + E + header.isa_15_usage_indicator + E + self.c + S
          
          eligRequest += "GS" + E + "HS" + E + header.gs_02_sender_id + E + header.gs_03_receiver_id + E + self.D_YYMMDD("%Y%m%d") + E + self.T_HHMM("%H%M") + E + header.isa_13_control_number + E + "X" + E + "005010X279A1" + S
          
          eligRequest += "ST" + E + "270" + E + "0001" + E + "005010X279A1" + S
          
          eligRequest += "BHT" + E + "0022" + E + "13" + E + header.isa_13_control_number + E + self.D_YYMMDD("%Y%m%d") + E + self.T_HHMM("%H%M") + S

          hl_payer = 0
          hl_counter = 0
          hl_provider = 0
          

    
          
          for data in header.list_Of_Eligibility_Data:
            msg = self.validate(header, data) 
            if not self.is_null_or_empty(msg): 
               
                result = Output.EligResult(
                    TRNNumber = data.trn01,
                    Processed = False,
                    ValidationMsg = msg
                )
            else:
                
                data.trn02 = header.isa_06_sender_id.rjust(10)

                if data.sbr_gender and data.sbr_gender.upper() == "MALE":
                    data.sbr_gender = "M"
                elif data.sbr_gender and data.sbr_gender.upper().replace(" ", "") == "FEMALE":
                    data.sbr_gender = "F"
                
                if data.pat_gender:
                    if data.pat_gender.upper() == "MALE":
                        data.pat_gender = "M"
                    elif data.pat_gender.upper().replace(" ", "") == "FEMALE":
                        data.pat_gender = "F"
                        
                prov_entity = "2" if not data.prov_first_name else "1"
        
        
                hl_payer = hl_counter + 1
                hl_counter = hl_payer + 1     
                
                
                eligRequest += "HL" + E + str(hl_payer) + E + E + "20" + E + "1" + S
                eligRequest += "NM1" + E + "PR" + E + "2" + E + data.payer_org_name + E + "" + E + E + E + E + "PI" + E + data.payer_id + S
                
                eligRequest += "HL" + E + str(hl_counter) + E + str(hl_payer) + E + "21" + E + "1" + S
                eligRequest += "NM1" + E + "1P" + E + prov_entity + E + data.prov_last_name + E + data.prov_first_name + E + data.prov_mi + E + E + E + "XX" + E + data.prov_npi + S
                if data.prov_taxonomy_code:
                    eligRequest += "PRV" + E + "BI" + E + "PXC" + E + data.prov_taxonomy_code + S
                
                hl_provider = hl_counter
                hl_counter += 1
                
                eligRequest += "HL" + E + str(hl_counter) + E + str(hl_provider) + E + "22" + E + ("0" if "18" in data.patient_relation_value else "1") + S
                if data.patient_relation_value == "18":
                    eligRequest += "TRN" + E + "1" + E + data.trn01 + E + data.trn02 + S
                    eligRequest += "NM1" + E + "IL" + E + "1" + E + data.sbr_last_name + E + data.sbr_first_name + E + data.sbr_middle_initial + E + E + E + "MI" + E + data.sbr_id + S
                    if data.sbr_dob:
                        eligRequest += "DMG" + E + "D8" + E + data.sbr_dob  + E + data.sbr_gender + S
                    if data.sbr_ssn:
                        eligRequest += "REF" + E + "SY" + E + data.sbr_ssn + S
                else:
                    hl_counter += 1
                    eligRequest += "NM1" + E + "IL" + E + "1" + E + data.sbr_last_name + E + data.sbr_first_name + E + data.sbr_middle_initial + E + E + E + "MI" + E + data.sbr_id + S
                    if data.sbr_dob:
                        eligRequest += "DMG" + E + "D8" + E + data.sbr_dob + E + data.sbr_gender + S
                    if data.sbr_ssn:
                        eligRequest += "REF" + E + "SY" + E + data.sbr_ssn + S
                
                    eligRequest += "HL" + E + str(hl_counter) + E + str(hl_counter - 1) + E + "23" + E + "0" + S
                    eligRequest += "TRN" + E + "1" + E + data.trn01 + E + data.trn02 + S
                    eligRequest += "NM1" + E + data.patient_relation_value + E + "1" + E + data.pat_last_name + E + data.pat_first_name + S
                    if data.pat_dob:
                        eligRequest += "DMG" + E + "D8" + E + data.pat_dob  + E + data.pat_gender + S
                
                    eligRequest += "INS" + E + "N" + E + data.patient_relation_value + S
                
                eligRequest += "DTP" + E + "291" + E + "D8" + E + data.eligibility_for_date  + S
                eligRequest += "EQ" + E + data.service_type_codes.replace(",", self.r) + S
                
                
                result = Output.EligResult(
                    TRNNumber = data.trn01,  # Assuming SBRData is an instance with an attribute trn01
                    Processed = True,
                    ProcessedDate = datetime.now()
                )
                
                            # Add the result to the output's Results list
                output.Results.append(result)
                
                
                # Increment the Processed counter
                # Increment Processed in result
                result.Processed += 1 
         
        
         Count = eligRequest.count(S) - 2
         
         # Append strings to eligRequest using f-strings for proper formatting
         eligRequest += f"SE{E}{Count + 1}{E}0001{S}"
         eligRequest += f"GE{E}1{E}{header.isa_13_control_number}{S}"
         eligRequest += f"IEA{E}1{E}{header.isa_13_control_number}{S}"
         
         # Set the ProcessedRequests attribute in the output
         
         
        return eligRequest

   
      
    
    def is_null_or_empty(self,value):
        return value is None or value == ""
    def is_null(self , value):
        return value is None
    def D_YYMMDD(self ,format_string):     
        return datetime.now().strftime(format_string)   
    def T_HHMM(self , format_string):
        return datetime.now().strftime(format_string)
    def validate(self ,header :_270Header, SBRData :_270Data):
        msg = ""
    
        if not SBRData.sbr_last_name or not SBRData.sbr_first_name:
            msg = "Subscriber Insured Name is required"
            msg = "Subscriber ID is required"
        elif not SBRData.patient_relation_value:
            msg = "Patient Relationship is required"
        elif not SBRData.payer_org_name:
            msg = "Payer Name is required"
        elif not SBRData.payer_id:
            msg = "Payer ID is required"
        elif not SBRData.prov_last_name:
            msg = "Provider Last Name is required"
        elif not SBRData.prov_npi:
            msg = "Provider NPI is required"
        elif SBRData.patient_relation_value != "18":
            if not SBRData.pat_last_name or not SBRData.pat_first_name:
                msg = "Patient Name is required"
            
        return msg
        
      
  
          
   
    
 

        
        
        
    
    