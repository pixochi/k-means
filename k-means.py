# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 18:25:53 2019

@author: Bruger
"""

import pandas as pd
import re

dataset = pd.read_csv('stud-stat-anonymous.csv')

# =============================================================================
# # Normalize the dataframe
# transform_shape = {
#   'subject': dataset.filter(regex="^Fag").columns,
#   'absence': dataset.filter(regex="^Fravær").columns
# }
# dataset = pd.lreshape(dataset, transform_shape)
# =============================================================================


# Translate column names to English
dataset = dataset.rename(columns=lambda x: re.sub('Fravær?.','absence',x))
dataset = dataset.rename(columns=lambda x: re.sub('Fag.?','subject',x))
dataset = dataset.rename(index=str, columns={"Samlet fravær": "average_absence", "Klasse": "class"})

# Convert absence percentage to float
absence_columns_selector = ['absence' in x for x in dataset.columns]
absence_columns_indexes = dataset.columns[absence_columns_selector]
absence_columns_indexes

dataset[absence_columns_indexes] = (dataset[absence_columns_indexes]
    .replace('%', '', regex=True)
    .convert_objects(convert_numeric=True) / 100.0
)

absence_columns = dataset[absence_columns_indexes]
absence_columns_indexes
dataset['median_absence'] = absence_columns.drop(['average_absence'], 1).median(1)

# identify clusters of students in the dataset
from sklearn.cluster import KMeans

kmean_input = pd.DataFrame(dataset[['median_absence', 'average_absence']])

kmeans = KMeans(n_clusters=3, random_state=0).fit(kmean_input)

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

students1[['median_absence', 'average_absence']].describe()
students2[['median_absence', 'average_absence']].describe()
students3[['median_absence', 'average_absence']].describe()

# make a plot for the clusters
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 12))
plt.scatter(dataset['median_absence'], dataset['average_absence'], c=kmeans.labels_.astype(float))
plt.title("K-means")
plt.xlabel("Median")
plt.ylabel("Mean")
plt.show()