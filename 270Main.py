import json
import os
from _270_271._270Generator import _270Generator
from _270_271._270Header import _270Header
from _270_271._270Data import _270Data
from zeep import Client
from _270_271 import _MedicareHETS
from zeep.exceptions import Fault, TransportError, XMLSyntaxError
from zeep.transports import Transport
import requests



def inputOption1():
    # set the header object from database values.
    header = _270Header()

    # Mapping simple header fields
    header.isa_01_auth_qual         = "00"
    header.isa_02_auth_info         = ""
    header.isa_03_sec_qual          = "00"
    header.isa_04_sec_info          = ""
    header.isa_05_sender_qual       = "ZZ"
    header.isa_06_sender_id         = "W172A932"
    header.isa_07_receiver_qual     = "ZZ"
    header.isa_08_receiver_id       = "CMS"
    header.isa_13_control_number    = "111111111"
    header.isa_15_usage_indicator   = "P"
    header.gs_02_sender_id          = "W172A932"
    header.gs_03_receiver_id        = "CMS"
    
    
    # Mapping list of Eligibility Data
    header.list_Of_Eligibility_Data = []
   
    data = _270Data()
    
    # Mapping Payer Information
    data.payer_org_name             = "CMS"
    data.payer_id                   = "CMS"
    
    # Mapping Provider Information
    data.prov_last_name             = "MY PRACTICE NAME"
    data.prov_first_name            = ""
    data.prov_mi                    = ""
    data.prov_npi                   = "1100223344"
    data.prov_taxonomy_code         = ""
    
    # Mapping Subscriber Information
    data.sbr_last_name              = "Gamble"
    data.sbr_first_name             = "Charles"
    data.sbr_middle_initial         = ""
    data.sbr_id                     = "1000032"
    
    data.sbr_address                = ""
    data.sbr_city                   = ""
    data.sbr_state                  = ""
    data.sbr_zip_code               = ""
    data.sbr_dob                    = "19800522"
    data.sbr_gender                 = "NY"
    
    data.patient_relation_value     = "18"
    # Mapping TRN Information
    data.trn01                      = "122313335"
    
    # Mapping Eligibility Date
    data.eligibility_for_date       = "20250404"     
    data.service_type_codes         = "30"
    
    # Append each _270Data instance to the list
    header.list_Of_Eligibility_Data.append(data)
    
    return header


def inputOption2():
    # you can generate the json from your application in this format and covert to object as shown here.
    jsonStr = """{
        "isa_01_auth_qual": "00",
        "isa_02_auth_info": "",
        "isa_03_sec_qual": "00",
        "isa_04_sec_info": "",
        "isa_05_sender_qual": "ZZ",
        "isa_06_sender_id": "W172A932",
        "isa_07_receiver_qual": "ZZ",
        "isa_08_receiver_id": "CMS",
        "isa_13_control_number": "111111111",
        "isa_15_usage_indicator": "T",
        "gs_02_sender_id": "W172A932",
        "gs_03_receiver_id": "CMS",
        "list_Of_Eligibility_Data": [
            {
                "payer_org_name": "CMS",
                "payer_id": "CMS",
                "prov_last_name": "MY PRACTICE NAME",
                "prov_first_name": "",
                "prov_mi": "",
                "prov_npi": "1100223344",
                "prov_taxonomy_code": "",
                "sbr_last_name": "Gamble",
                "sbr_first_name": "Charles",
                "sbr_middle_initial": "",
                "sbr_id": "1000032",
                "sbr_address": "",
                "sbr_city": "",
                "sbr_state": "",
                "sbr_zip_code": "",
                "sbr_dob": "19800522",
                "sbr_gender": "M",
                "patient_relation_value": "18",
                "trN01": "12345678",
                "eligibility_for_date": "20250404",
                "service_type_codes" : "30"
            }
        ]
    }"""

    generator = _270Generator()

    json_data = json.loads(jsonStr) 
    edi270Obj = generator.prepare_model(json_data)
    
    return edi270Obj


def main():

    try:
        generator = _270Generator()
        
        # you can use any option for input data

        #edi270Obj = inputOption1()
        edi270Obj = inputOption2()

        edi_output = generator.Generate270(edi270Obj)
        output_file =  "EDI270.txt"
        
        with open(output_file, 'w') as edi_file_handle:
            edi_file_handle.write(edi_output)

        print(f"EDI file generated successfully: {output_file}")
        
        
        
        request_payload = _MedicareHETS.CMS270RequestPayload(Payload=edi_output)

        # Step 2: Generate the XML representation
        xml_body = request_payload.to_xml()
        
       

        print (xml_body)
        
        
        # Initialize the SOAP client
        # Create a session
        session = requests.Session()
        
        # Path to combined PEM file (cert + key)
        session.cert = '/path/to/client_cert.pem'
        
        # Optional: Verify server cert (recommended). Use CMS CA bundle if needed.
        # session.verify = '/path/to/ca_cert.pem'
        
        # Disable verification if testing only (NOT recommended in production)
        # session.verify = False
        
        # Create transport and client
        transport = Transport(session=session)
        client = Client("https://soap.hets-270-271.cms.gov/eligibility/realtime/soap", transport=transport)
        
        # Send the SOAP request
        response = client.service.COREEnvelopeRealTimeRequest(xml_body)

    except Fault as fault:
        print("SOAP Fault:")
        print(f"Code: {fault.code}")
        print(f"Message: {fault.message}")
        print(f"Detail: {fault.detail}")
    
    except TransportError as te:
        print("Transport Error:")
        print(f"Status Code: {te.status_code}")
        print(f"Message: {te.message}")
    
    except XMLSyntaxError as xe:
        print("XML Syntax Error:")
        print(xe)
    
    except Exception as e:
        print("General Exception:")
        print(str(e))
            
            
                #see the method responseEligibilityRequest may vary!!!!!!!!! 
                # result = client.service.responseEligibilityRequest(xml_body)
                
        
                # print (result)
        
 

if __name__ == "__main__":
    main()
