# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 10:41:13 2019

@author: Bruger
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

attendance_dataset = pd.read_csv('stud-stat-anonymous.csv')

# Replace spaces with underscores in column names
cols = attendance_dataset.columns
cols = cols.map(lambda x: x.replace(' ', '_'))
attendance_dataset.columns = cols

# Normalize the dataframe
transform_shape = {
  'Fag': attendance_dataset.filter(regex="^Fag").columns,
  'Fravær': attendance_dataset.filter(regex="^Fravær").columns
}
transformed_attendance_dataset = pd.lreshape(attendance_dataset, transform_shape)

# Convert percentage to float
transformed_attendance_dataset['Samlet_fravær'] = transformed_attendance_dataset['Samlet_fravær'].str.rstrip('%').astype('float') / 100.0
transformed_attendance_dataset['Fravær'] = transformed_attendance_dataset['Fravær'].str.rstrip('%').astype('float') / 100.0


# Remove rows with absence over 75%
transformed_attendance_dataset = transformed_attendance_dataset[transformed_attendance_dataset['Samlet_fravær'] <= 0.75]

# Histogram
attendance_dataset['Samlet_fravær'].hist(bins = 20, figSize = 20, rwidth = 0.8)
plt.title('Absence / students')
plt.xlabel('Absence (%)')
plt.ylabel('Frequency in sample')
plt.show()