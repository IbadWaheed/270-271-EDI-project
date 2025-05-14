from typing import List, Optional
from _270_271._270Data import _270Data


class _270Header:
    def __init__(self):
        self.isa_01_auth_qual = "00"
        self.isa_03_sec_qual = "00"
        self.isa_05_sender_qual = "ZZ"
        self.isa_07_receiver_qual = "ZZ"
        # self.isa11_repetition_sep = "^"
        # self.isa12_version = "00501"
        # self.isa14_ack_requested = "1"
        self.isa_15_usage_indicator = "P"
        # self.isa16_compo_ele_sep = ":"
        self.isa_02_auth_info = "".ljust(10, ' ')
        self.isa_04_sec_info = "".ljust(10, ' ')

        self.list_Of_Eligibility_Data: List[_270Data] = []

    isa_01_auth_qual: str = None
    isa_02_auth_info: str = None
    isa_03_sec_qual: str = None
    isa_04_sec_info: str = None
    isa_05_sender_qual: str = None
    isa_06_sender_id: Optional[str] = None
    isa_07_receiver_qual: str = None
    isa_08_receiver_id: Optional[str] = None
    # isa09_date: Optional[str] = None
    # isa10_time: Optional[str] = None
    # isa11_repetition_sep: Optional[str] = None
    # isa12_version: Optional[str] = None
    isa_13_control_number: Optional[str] = None
    # isa14_ack_requested: Optional[str] = None
    isa_15_usage_indicator: str = None
    # isa16_compo_ele_sep: Optional[str] = None

    gs_02_sender_id: Optional[str] = None
    gs_03_receiver_id: Optional[str] = None

    list_Of_Eligibility_Data: List[_270Data] = None
