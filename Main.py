import pandas as pd
try:
    sample = pd.DataFrame.from_csv('sample.csv')
except:
    import Sample_generator

import Gmail
import Classifier
from  Classifier import predictions




