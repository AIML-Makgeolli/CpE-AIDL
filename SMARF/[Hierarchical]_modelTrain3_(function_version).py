# -*- coding: utf-8 -*-
"""Copy of [Hierarchical] modelTrain3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1O64vtLbJc5Uybs9oMOhTCjfoACyqsDcp

References: 

- http://www.diva-portal.org/smash/get/diva2:1382324/FULLTEXT01.pdf
- https://stackabuse.com/hierarchical-clustering-with-python-and-scikit-learn/
"""

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn import metrics
from sklearn.model_selection import train_test_split
from numpy import sqrt, array, random, argsort
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, centroid, fcluster
import scipy.cluster.hierarchy as shc
from scipy.spatial.distance import cdist, pdist
from sklearn.neighbors import NearestCentroid



#from google.colab import drive
#drive.mount('/content/gdrive')

df =  pd.read_csv("https://raw.githubusercontent.com/AIML-Makgeolli/CpE-AIDL/main/thesis_database/Crop_recommendation.csv")
df_train = df.drop(['label','rainfall'], axis = 1)

"""Declarations"""

X_N= df_train[['N']]
X_P= df_train[['P']]
X_K= df_train[['K']]
X_temp= df_train[['temperature']]
X_moist= df_train[['humidity']]
y = df_train[['ph']]

"""Nitrogen and ph """

class hierarchical():
      def __init__(self):
    return

  def input_train(self, X_in, y_in):
    self.X = X_in
    self.y = y_in
    X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,test_size=0.3, random_state=42)
    self.data = pd.concat([X_train, y_train], axis=1).to_numpy()
    return self.data

  def dendograms(self):
    plt.figure(figsize=(7, 5))
    plt.title("Dendograms")
    dend = shc.dendrogram(shc.linkage(self.data, method='ward'))

  def cluster_fit(self, clust):
    self.cluster = AgglomerativeClustering(n_clusters = clust, affinity ='euclidean', linkage='ward')
    self.res = self.cluster.fit_predict(self.data)
    
    self.labels = self.cluster.labels_
    
    print(self.labels)
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(self.data, self.labels))
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(self.res, self.labels))
    print("Completeness: %0.3f" % metrics.completeness_score(self.res, self.labels))
    print("V-measure: %0.3f" % metrics.v_measure_score(self.res, self.labels))
    print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(self.res, self.labels))
    print("Adjusted Mutual Information: %0.3f"% metrics.adjusted_mutual_info_score(self.res, self.labels))
    return self.res
  
  def outlier(self,threshold):
    clf = NearestCentroid()
    clf.fit(self.data, self.res)
    self.centroids = clf.centroids_
    self.points = np.empty((0,len(self.data[0])), float)
    self.distances = np.empty((0,len(self.data[0])), float)
    for i, center_elem in enumerate(self.centroids):
      self.distances = np.append(self.distances, cdist([center_elem],self.data[self.res == i], 'euclidean')) 
      self.points = np.append(self.points, self.data[self.res == i], axis=0)
      
    percentile = threshold
    self.outliers = self.points[np.where(self.distances > np.percentile(self.distances, percentile))]
    outliers_df = pd.DataFrame(self.outliers,columns =['X','y'])
    return outliers_df

  def cluster_graph(self):
    plt.figure(figsize=(7, 5))
    plt.scatter(self.data[:,0], self.data[:,1], c=self.cluster.labels_, cmap='rainbow')
    plt.scatter(*zip(*self.outliers),marker="o",facecolor="None",edgecolor="g",s=70); 
    plt.scatter(*zip(*self.centroids),marker="o",facecolor="b",edgecolor="b",s=20);


hierarchical_test = hierarchical()

"""Nitrogen and pH"""

hierarchical_test.input_train(X_N,y)

hierarchical_test.dendograms()

hierarchical_test.cluster_fit(3)

hierarchical_test.outlier(80)

hierarchical_test.cluster_graph()

"""Phosphorus and pH"""

hierarchical_test.input_train(X_P,y)

hierarchical_test.dendograms()

hierarchical_test.cluster_fit(3)

hierarchical_test.outlier(80)

hierarchical_test.cluster_graph()

"""Potassium and pH"""

hierarchical_test.input_train(X_K,y)

hierarchical_test.dendograms()

hierarchical_test.cluster_fit(3)

hierarchical_test.outlier(80)

hierarchical_test.cluster_graph()

"""Temperature and pH"""

hierarchical_test.input_train(X_temp,y)

hierarchical_test.dendograms()

hierarchical_test.cluster_fit(3)

hierarchical_test.outlier(80)

hierarchical_test.cluster_graph()

"""Moisture and pH"""

hierarchical_test.input_train(X_moist,y)

hierarchical_test.dendograms()

hierarchical_test.cluster_fit(3)

hierarchical_test.outlier(80)

hierarchical_test.cluster_graph()