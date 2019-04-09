# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 18:25:53 2019

@author: Bruger
"""

import pandas as pd

dataset = pd.read_csv('stud-stat-anonymous.csv')

# Normalize the dataframe
transform_shape = {
  'subject': dataset.filter(regex="^Fag").columns,
  'absence': dataset.filter(regex="^Fravær").columns
}
dataset = pd.lreshape(dataset, transform_shape)

dataset = dataset.rename(index=str, columns={"Samlet fravær": "total_absence", "Klasse": "class"})

# Convert percentage to float
dataset['total_absence'] = dataset['total_absence'].str.rstrip('%').astype('float') / 100.0
dataset['absence'] = dataset['absence'].str.rstrip('%').astype('float') / 100.0

# identify clusters of students in the dataset
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=0).fit(dataset.loc[:, ['total_absence', 'absence']])

cluster_map = pd.DataFrame()
cluster_map['data_index'] = dataset.index.values
cluster_map['cluster'] = kmeans.labels_

# clusters
c1 = cluster_map[cluster_map.cluster == 0]
c2 = cluster_map[cluster_map.cluster == 1]
c3 = cluster_map[cluster_map.cluster == 2]

# students from the clusters
students1 = dataset.iloc[c1['data_index']]
students2 = dataset.iloc[c2['data_index']]
students3 = dataset.iloc[c3['data_index']]