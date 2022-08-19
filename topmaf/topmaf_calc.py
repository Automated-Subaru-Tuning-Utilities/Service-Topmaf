import sys
import numpy as np
import pandas as pd

sys.path.append("./models")
from topmaf_api_models import topmaf_input
from maf_voltages import maf_voltages

def main(data: topmaf_input):
    #turn input data into dataframes
    targets = [i.dict() for i in data.target_afr]
    targets = pd.DataFrame(targets)
    log_data = [i.dict() for i in data.log_data]
    log_data = pd.DataFrame(log_data)
    
    #for testing
    # print(targets)
    # print(log_data)
    print(targets.loc[0,"target_afr"])
    print(targets.loc[1,"rpm"])

    print(log_data.loc[0,"wideband_o2"])
    print(log_data.loc[0,"load"])

    return {"result": "success"}
if __name__ == "__main__":
    print("testing here")