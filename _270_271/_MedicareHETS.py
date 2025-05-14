from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class CMS270RequestPayload:
    PayloadType: str = "X12_270_Request_005010X279A1"
    ProcessingMode: str = "RealTime"
    PayloadID: str = str(uuid.uuid4())  # Generates a unique ID
    TimeStamp: str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    SenderID: str = "W172A932"  
    ReceiverID: str = "CMS"
    CORERuleVersion: str = "2.2.0"
    Payload: str = ""  # Your raw X12 270 request, must be enclosed in CDATA

    def to_xml(self) -> str:
        """
        Generate the XML representation of the payload suitable for a SOAP body.
        """
        return f"""<soapenv:Body>
    <core:Envelope xmlns:core="urn:hl7-org:v3">
        <core:PayloadType>{self.PayloadType}</core:PayloadType>
        <core:ProcessingMode>{self.ProcessingMode}</core:ProcessingMode>
        <core:PayloadID>{self.PayloadID}</core:PayloadID>
        <core:TimeStamp>{self.TimeStamp}</core:TimeStamp>
        <core:SenderID>{self.SenderID}</core:SenderID>
        <core:ReceiverID>{self.ReceiverID}</core:ReceiverID>
        <core:CORERuleVersion>{self.CORERuleVersion}</core:CORERuleVersion>
        <core:Payload><![CDATA[{self.Payload}]]></core:Payload>
    </core:Envelope>
</soapenv:Body>"""
