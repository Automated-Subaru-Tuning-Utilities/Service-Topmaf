import sys
import numpy as np
import pandas as pd

sys.path.append("./models")
from topmaf_api_models import topmaf_input
from maf_voltages import maf_voltages

# step 1
# filter out any data not near 100% throttle 
def filter_data(df):
    new_data = df[df["throttle_position"] > 87]
    new_data.reset_index(drop=True, inplace=True)
    return new_data

# step 2 
# find the percent error of target afrs to wideband afrs
# this is done by matching the closest load/rpm pair in the log to the target afrmap
def afr_error(df, targets):
    #create the afr_error column
    df.loc[0, "afr_error"] = 0.0
    for i in range(1, len(df)):
        print(df.loc[i])
    
def main(data: topmaf_input):
    #turn input data into dataframes
    targets = [i.dict() for i in data.target_afr]
    targets = pd.DataFrame(targets)
    log_data = [i.dict() for i in data.log_data]
    log_data = pd.DataFrame(log_data)
    
    log_data = filter_data(log_data)
    # print(log_data)
    afr_error(log_data, targets)

    return {"result": "success"}
if __name__ == "__main__":
    print("testing here")