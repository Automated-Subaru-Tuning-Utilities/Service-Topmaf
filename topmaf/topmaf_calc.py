import sys
import numpy as np
import pandas as pd

sys.path.append("./models")
from topmaf_api_models import topmaf_input
from maf_voltages import maf_voltages

def main(data: list[topmaf_input]):
    target_afr = data.target_afr
    target_afr = pd.DataFrame([item.dict() for item in target_afr])
    # log_data = pd.DataFrame(data.log_data)
    # target_afr = data.target_afr
    # log_data = data.log_data
    return target_afr

if __name__ == "__main__":
    print("testing here")