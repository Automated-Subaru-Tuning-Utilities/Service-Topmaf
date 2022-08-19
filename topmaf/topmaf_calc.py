import sys
import numpy as np
import pandas as pd

sys.path.append("./models")
from topmaf_api_models import topmaf_input
from maf_voltages import maf_voltages

def main(data: topmaf_input):
    targets = [i.dict() for i in data.target_afr]
    print(targets)
    print(type(targets)) # outputs <class 'list'>
    for i in targets:
        print(i)
    print(type(targets[0])) # outputs <class 'dict'>
    df = pd.DataFrame(targets) # outputs numpy.int64 not iterable 
                               # TF?!??!?
    return targets[1]["load"] # yet this works
    # log_data = pd.DataFrame(data.log_data)
    # target_afr = data.target_afr
    # log_data = data.log_data

if __name__ == "__main__":
    print("testing here")