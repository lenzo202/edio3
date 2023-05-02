from edio3 import rs_loose_parse, rs_to_x12_string, rs_parse
from rich import print
import os
from pathlib import Path
from time import perf_counter
from tigershark.X12.parse import Message
from pyx12.x12context import X12ContextReader
from pyx12 import params, error_handler
from pydantic import BaseModel
from typing import Optional

# badx12 incompatibale with 3.10 + 
# ImportError: cannot import name 'Iterable' from 'collections'
# see note in 3.9 docs here https://docs.python.org/3.9/library/collections.html

class GenericSegment(BaseModel):
    segment_abbreviation: str
    elements: list[str]
    
class Transaction(BaseModel):
    transaction_code: str
    transaction_name: str
    transaction_set_control_number: str
    implementation_convention_reference: Optional[str]
    segments: list[GenericSegment]
    
class FunctionalGroup(BaseModel):
    functional_identifier_code: str
    application_sender_code: str
    application_receiver_code: str
    date: str
    time: str
    group_control_number: str
    responsible_agency_code: str
    version: str
    transactions: list[Transaction]   

class InterchangeControl(BaseModel):
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


class EdiDocument(BaseModel):
    segment_delimiter: str
    sub_element_delimiter: str
    element_delimiter: str
    interchanges: list[InterchangeControl]




TEST_FILES_DIR = Path(__file__).parent / "test_files"
TEST_FILES = [str(TEST_FILES_DIR / file) for file in os.listdir(TEST_FILES_DIR)]

param = params.params()
errh = error_handler.errh_null()

def test_pyx12() -> None:
    for file in TEST_FILES:
        with Path(file).open() as fd:
            message = X12ContextReader(param, errh, src_file_obj=fd)    
                


def test_tigershark(iterations:int)-> None:
    start = perf_counter()
    parser = Message()
    for x in range(iterations):
        for file in TEST_FILES:
            message = parser.unmarshall(Path(file).read_text("utf-8").strip())
            print(message)
            ...
    return perf_counter()-start
            

def test_edio3() -> None:
    for file in TEST_FILES:
        rust_obj = rs_parse(file)

def test_parse_error() -> None:
    test_files_dir = Path("scratch/test_files")
    path = str(test_files_dir/"edi.X12")
    #print(path)
    rust_obj = rs_parse(path)
    print(rust_obj)
    string = rs_to_x12_string(rust_obj)
    print(string)
    

def test_into_pydantic() -> None: 
    for file in TEST_FILES:
        rust_obj = rs_parse(file)
        doc = EdiDocument(**rust_obj)



__benchmarks__ =[
    (test_pyx12, test_edio3, "edio3 (to dict) vs. pyx12"),
    (test_pyx12, test_into_pydantic, "edio3 (pydantic) vs. pyx12"),
]


if __name__ == "__main__":
    # test()
    #test_parse_error()
    # test_tigershark(1)
    print(test_edio3(1000))
    print(test_into_pydantic(1000))
    print(test_pyx12(1000))