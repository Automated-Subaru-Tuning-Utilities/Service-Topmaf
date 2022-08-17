from pydantic import BaseModel

# FastAPI request and response models provide a lot of utility and benefits
# For this project, some benefits to note:
# 1. Type Checking: Pydantic models will make sure any api data conforms to the right type
# 2. Explicitly defined input/output: makes the code more readable
# 3. Filtering: security and reusability
#   Lets say we have a main api endpoint that returns 10 fields of data
#   We can reuse this api for multiple purposes by filtering for only the fields that we need
#   This also can potentially provide a security benefit by filtering before transport of data, to prevent sensitive info disclosure

   
class target_afr(BaseModel):
    load: float
    rpm: int
    target_afr: float

class log_data(BaseModel):
    mass_airflow_voltage: float
    throttle_position: float
    load: float
    rpm: int
    wideband_o2: float

class topmaf_input(BaseModel):
    target_afr: list[target_afr]
    log_data: list[log_data]
 
class topmaf_output(BaseModel):
    MafVoltage: float
    Correction: float
    Frequency: int
