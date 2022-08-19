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
    for i in range(0, len(df)):
        triple = [df.loc[i, "rpm"], df.loc[i, "load"], df.loc[i, "wideband_o2"]]
        error = afr_error_helper(triple, targets)
        df.loc[i,"afr_error"] = error
    return df

def afr_error_helper(triple, targets):
    rpm = triple[0]
    load = triple[1]
    wideband = triple[2]
    rpm_match = targets.iloc[(targets["rpm"] - rpm).abs().argsort()[:2]]
    load_match = targets.iloc[(targets["load"] - load).abs().argsort()[:2]]
    
    # match using ECU flash's interpolation scheme
    rpm_match = max(rpm_match["rpm"].tolist())
    load_match = max(load_match["load"].tolist())
    afr_match = targets[ (targets["rpm"] == rpm_match) & (targets["load"] == load_match)]
    afr_match.reset_index(drop=True, inplace=True)
    
    # handle case where user supplies an incomplete target_afr map
    if(len(afr_match) < 1):
        print(f"WARNING: Entry (Rpm: {rpm_match}, Load: {load_match}) was not found in target_afr. Defaulting to 0% error")
        error = 0
    else:
        afr_match = afr_match.loc[0,"target_afr"]
        error = 100*(wideband - afr_match)/afr_match
    return error

# step 3
# match up the corrections with the cooresponding maf voltages

def main(data: topmaf_input):
    #turn input data into dataframes
    targets = [i.dict() for i in data.target_afr]
    targets = pd.DataFrame(targets)
    log_data = [i.dict() for i in data.log_data]
    log_data = pd.DataFrame(log_data)
    
    log_data = filter_data(log_data)
    log_data = afr_error(log_data, targets)
    print(log_data)

    return {"result": "success"}
if __name__ == "__main__":
    print("testing here")