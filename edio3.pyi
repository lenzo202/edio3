from typing import TypedDict, Optional

class EdiDocument(TypedDict):
    segment_delimiter: str
    sub_element_delimiter: str
    element_delimiter: str
    interchanges: list[InterchangeControl]


class InterchangeControl(TypedDict):
    authorization_qualifier: str
    authorization_information: str
    security_qualifier: str
    security_information: str
    sender_qualifier: str
    sender_id: str
    receiver_qualifier: str
    receiver_id: str
    date: str
    time: str
    standards_id: str
    version: str
    interchange_control_number: str
    acknowledgement_requested: str
    test_indicator: str
    functional_groups: list[FunctionalGroup]


class FunctionalGroup(TypedDict):
    functional_identifier_code: str
    application_sender_code: str
    application_receiver_code: str
    date: str
    time: str
    group_control_number: str
    responsible_agency_code: str
    version: str
    transactions: list[Transaction]
    
    
class Transaction(TypedDict):
    transaction_code: str
    transaction_name: str
    transaction_set_control_number: str
    implementation_convention_reference: Optional[str]
    segments: list[GenericSegment]
    
    
class GenericSegment(TypedDict):
    segment_abbreviation: str
    elements: list[str]
    

def rs_parse(path:str) -> EdiDocument:
    ...

def rs_loose_parse(path:str) -> EdiDocument:
    ...

def rs_to_x12_string(path:str) -> str:
    ...
    
def rs_to_json(path:str) -> str:
    ...