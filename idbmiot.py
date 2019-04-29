#!/usr/bin/python

import pandas as pd
import numpy as np
from resampling import resample
from chooseSample import chooseSample
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import random
import math
from collections import Counter

def IDBMIOT(S, A, k1, k2):
    #c, p1, p2, m, D <- S & A
    c = pd.Series.sort_values(S['Class'].value_counts())
    p1 = len(A.numeric)
    p2 = len(A.nominal)
    m = len(c)
    D = c

    #resampling, get orate(c)
    orates = resample(c, D, S)
    orate = orates.orate

    print("Oversampling rate: " + str(orate))

    S = orates.samples
    S = S.dropna()

    c = pd.Series.sort_values(S['Class'].value_counts())
    m = len(c)
    D = c
    minorityClasses = c.drop(c.index[m-1])
    c = minorityClasses
    
    retransform_sample = {}

    #iterate on class
    for c1 in c.keys():
        #instance of class c1
        xs = S[S['Class'] == c1]
        class_sample_instance = len(xs)


        samples = chooseSample(S, c1, k1, k2)
        _sample = samples

        """#_samples computation
        #_sample = pd.get_dummies(samples, columns=["Class"], prefix=["class"])

        #mean
        #us = xs.mean(axis=0)

        
         #eclipse curve
        ec = 0
        it = 0 
        for i in class_sample_instance:
            ec = ec + math.pow((xs.iloc(it) - us),2) 
            it = it + 1
        
        os = math.sqrt( (1/class_sample_instance) * ec)
        #normalization
        _sample = (_sample - us)/os

        #compute N & M 
        N = 1/class_sample_instance 
        adiag = []
        g = 0
        while g < len(A.numeric):
            adiag.append(1)
            g = g + 1
        h = 0 
        while h < (m * len(A.nominal)):
            k=0
            while k<len(c.keys()):
                v = _sample.iloc[len(A.numeric)+k]
                adiag.append(2/len(v)) 
                k = k + 1
            h = h +1
        M = np.diag(adiag) """

        #get features and label
        X = _sample.drop('Class', axis=1)
        y = _sample['Class']

        #Standardise
        x_std = StandardScaler().fit_transform(X)

        #coefficent of vector varriance
        features = x_std.T 
        covariance_matrix = np.cov(features)
        V = covariance_matrix

        #convert samples into Principle component 
        pca = PCA(n_components=2)
        principalComponents = pca.fit_transform(x_std)
        principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

        #principalDf['Class'] = _sample['Class']     

        cf = _sample[['Class']]
        #finalDf = pd.append([principalDf, _sample[['Class']]], axis = 1)
        finalDf = principalDf.join(cf)


        newSampleInPC = pd.DataFrame()
        newSampleInOC = pd.DataFrame()

        #sample generation
        if(orate[c1] > 0):
            j = 0 
            while j < orate[c1]:

                #random sample choose
                maxValue = finalDf[finalDf['Class'] == c1].max()[0]
                randomSample = finalDf[np.isclose(finalDf['principal component 1'],maxValue)]

                #cal random sample
                rs = sum(random.sample(range(1, p1+m+k2), p1+m))
                randomSample['principal component 1']  = randomSample['principal component 1'] + rs
                newSampleInPC = newSampleInPC.append(randomSample)
                
                j = j + 1


        if not newSampleInPC.empty:

            ff = newSampleInPC.drop('Class', axis=1)
            # get new sample
            newSampleInOC = pca.inverse_transform(ff)

            # transform 
            column_label = X.columns
            retransform_sample =  pd.DataFrame(newSampleInOC, columns= column_label)
            retransform_sample['Class'] = c1
    

    #Addition of resamples into orginal sample
    """ if retransform_sample.empty is False:
        #print("No new sample were generated!")
        raise Exception('No new sample were generated!')
    else: """
    S.append(retransform_sample, ignore_index=True)


    #return samples
    return S



    
