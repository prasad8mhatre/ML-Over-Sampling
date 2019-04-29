#import all required modules
from idbmiot import IDBMIOT
import pandas as pd
import numpy as np
from resampling import resample
from chooseSample import chooseSample
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import random
import math
from sklearn.cross_validation import KFold, train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score  
from sklearn.metrics import roc_auc_score
import time
import matplotlib.pyplot as plt 

def run():
    # import dataset
    # import dataset
    loc = "data/new-thyroid.csv"
    df = pd.read_csv(loc, sep=',', header=None)
    columns = ['T3resin', 'Thyroxin', 'Triiodothyronine', 'Thyroidstimulating', 'TSH_value', 'Class']
    df.columns = columns

    S = df


    class AttributeIndicator(object):
        def __init__(self):
            self.nominal = [5]
            self.numeric = [0,1,2,3,4]

    A = AttributeIndicator()

    k1 = 2
    k2 = 4


    print("Total Data size: " + str(len(S)))

    c = pd.Series.sort_values(S['Class'].value_counts())
    p1 = len(A.numeric)
    p2 = len(A.nominal)
    m = len(c)
    D = c

    #resampling, get orate(c)
    orates = resample(c, D, S)
    orate = orates.orate

    print("Oversampling rate: " + str(orate))


    #Perform oversampling
    #newS = IDBMIOT(S,A, k1, k2)

    #afterTimeInMillis = int(round(time.time() * 1000))

    #excutionTime = afterTimeInMillis - beforeTimeInMillis

    #Get distribution for sample original/after sampling
    #print ("Distribution of class labels before resampling {}".format(S['Class'].value_counts()))
    #print ("Distribution of class labels after resampling {}".format(newS['Class'].value_counts()))

    #print(str(excutionTime))

run()