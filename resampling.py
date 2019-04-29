#!/usr/bin/python

import math
import pandas as pd

class OrateData(object):
    def __init__(self, orate, samples):
        self.orate = orate
        self.samples = samples


def resample(c, D, S): 
    n_min = pd.Series.min(D)
    n_max = len(D)
    N = S

    #maxit 
    maxit = math.ceil((n_max*(len(c)-1))/n_min)

    _D = D
    _N = N
    i = 0
    while i < maxit:
        current_no_total_samples = len(_N)
        no_of_samples_in_current_min_class = pd.Series.min(_D)
        pmin = no_of_samples_in_current_min_class/current_no_total_samples
      
        if pmin < (2/(3*len(c)-1)):
            current_min_class = pd.Series.sort_values(_D).keys()[0]
            
            #Add original data in to 
            samples_in_original_data = S[S['Class'] == current_min_class]
            _N = _N.append(samples_in_original_data)
            _D=pd.Series.sort_values(_N['Class'].value_counts())
        
        i = i + 1

    Orate = _D - D
    data = OrateData(Orate, _N)
    return data
    



        
    
