from typing import Optional
from datetime import datetime

class _270Data:
    
    # Payer Information
    payer_org_name: Optional[str] = None
    payer_id: Optional[str] = None

    # Provider Information
    prov_last_name: Optional[str] = None
    prov_first_name: Optional[str] = None
    prov_mi: Optional[str] = None
    prov_npi: Optional[str] = None
    prov_taxonomy_code: Optional[str] = None

    # Subscriber Name
    sbr_last_name: Optional[str] = None
    sbr_first_name: Optional[str] = None
    sbr_middle_initial: Optional[str] = None
    sbr_id: Optional[str] = None

    # Subscriber Address
    sbr_address: Optional[str] = None
    sbr_city: Optional[str] = None
    sbr_state: Optional[str] = None
    sbr_zip_code: Optional[str] = None

    # Subscriber DMG
    sbr_dob: Optional[datetime] = None
    sbr_gender: Optional[str] = None
    sbr_ssn: Optional[str] = None

    # Patient Relation
    patient_relation_value: str

    # Patient Name
    pat_last_name: Optional[str] = None
    pat_first_name: Optional[str] = None
    pat_middle_initial: Optional[str] = None

    # Patient Address
    pat_address: Optional[str] = None
    pat_city: Optional[str] = None
    pat_state: Optional[str] = None
    pat_zip_code: Optional[str] = None

    # Patient DMG
    pat_dob: Optional[datetime] = None
    pat_gender: Optional[str] = None

    # TRN
    trn01: Optional[str] = None
    eligibility_for_date: datetime
    service_type_codes: str