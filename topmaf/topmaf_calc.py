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
# mostly copied from Service-Lowmaf/lowmaf/lowmaf_calc.py
def match_maf(df, maf_voltages):
    # we go from index = 0 to index = len -1 in the loop because we need a special case for the first and last indicies
    # check length once for optimization (although compiler might do this)
    maf_voltages_length = len(maf_voltages) - 1
    # for index 0, we check values >=0 and <.94
    # this is due to the way that ECUflash handles interpolation
    vals = df[(df["mass_airflow_voltage"] >= 0) & (df["mass_airflow_voltage"] < maf_voltages[0]["MafVoltage"])]
    freq = len(vals)
    if (freq > 0):
        mean = vals["afr_error"].mean()
        mean = np.around(mean, decimals=5)
        maf_voltages[0]["Correction"] = mean
        maf_voltages[0]["Frequency"] += freq
    for i in range (1, maf_voltages_length):
        vals = df[(df["mass_airflow_voltage"] >= maf_voltages[i]["MafVoltage"]) & (df["mass_airflow_voltage"] < maf_voltages[i+1]["MafVoltage"])]
        freq = len(vals)
        if (freq > 0):
            mean = vals["afr_error"].mean()
            mean = np.around(mean, decimals=5)
            maf_voltages[i]["Correction"] = mean
            maf_voltages[i]["Frequency"] += freq
    # special case for last index
    # we check values >4.69 and <= 5.0
    vals = df[(df["mass_airflow_voltage"] > maf_voltages[len(maf_voltages)-1]["MafVoltage"]) & (df["mass_airflow_voltage"] <= 5.0)]
    freq = len(vals)
    if (len(vals) > 0):
        mean = vals["afr_error"].mean()
        mean = np.around(mean, decimals=5)
        maf_voltages[maf_voltages_length]["Correction"] = mean
        maf_voltages[maf_voltages_length]["Frequency"] += freq

    return maf_voltages

def main(data: topmaf_input):
    #turn input data into dataframes
    targets = [i.dict() for i in data.target_afr]
    targets = pd.DataFrame(targets)
    log_data = [i.dict() for i in data.log_data]
    log_data = pd.DataFrame(log_data)

    #data analysis steps
    log_data = filter_data(log_data)
    log_data = afr_error(log_data, targets)
    return match_maf(log_data, maf_voltages)

if __name__ == "__main__":
    print("testing here")