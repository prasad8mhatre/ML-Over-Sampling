#!/usr/bin/python

from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import numpy as np

#return xs
def chooseSample(S, c, k2, k1):
    xs = S[S['Class'] == c]
    #iterate over each sample of class c1
    for row in xs.iterrows():
        d1 = row[1]
        d1 = d1.drop('Class')
        y = S['Class']
        X = S.drop('Class', axis=1)
        
        #get k2 nearest neighbour using mahalanobis distance metric
        cov = np.cov(X, rowvar=False)
        knn = KNeighborsRegressor(n_neighbors=k2, metric="mahalanobis",metric_params=dict(V=cov))
        knn.fit(X, y)
    
        d = []
        d.append(d1)
        d1 = d
        
        #print(str(d1))
        neigbour = knn.kneighbors(d1)
        #print("length:"+ str(len(neigbour)))
        neighbour_length = len(neigbour)
        if(neighbour_length >= k1):
            S['wieght'] = neighbour_length/k2
            
    return S