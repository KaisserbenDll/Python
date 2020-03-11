# -*- coding: utf-8 -*-
"""Employee_Attrition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ch7e0ZiuPTVuJIogs-ZfJnGLYrw3Pfl7
"""

# Description: This program predicts employee attrition.

#Resources: 
# 1. Scikit - learn : https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
# 2. Kaggle Data Set : https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset 
# 3. Building an Employee Churn Model in Python to Develop a Strategic Retention Plan: https://towardsdatascience.com/building-an-employee-churn-model-in-python-to-develop-a-strategic-retention-plan-57d5bd882c2d

#Import Libraries
import numpy as np
import pandas as pd
import seaborn as sns

#Load the data 
from google.colab import files # Use to load data on Google Colab 
uploaded = files.upload() # Use to load data on Google Colab

#Store the data into the df variable
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv') 
df.head(7) #Print the first 7 rows

#Get the number of rows and number of columns in the data
df.shape

#Get the column data types
df.dtypes

#Count the empty (NaN, NAN, na) values in each column
df.isna().sum()

#Another check for any null / missing values
df.isnull().values.any()

#View some basic statistical details like percentile, mean, standard deviation etc.
df.describe()

#Get a count of the number of employee attrition, the number of employees that stayed (no) and the number that left (yes)
df['Attrition'].value_counts()

#Visualize this count 
sns.countplot(df['Attrition'])

#Show the number of employees that left and stayed by age
import matplotlib.pyplot as plt
fig_dims = (12, 4)
fig, ax = plt.subplots(figsize=fig_dims)

#ax = axis
sns.countplot(x='Age', hue='Attrition', data = df, palette="colorblind", ax = ax,  edgecolor=sns.color_palette("dark", n_colors = 1));

#Print all of the object data types and their unique values
for column in df.columns:
    if df[column].dtype == object:
        print(str(column) + ' : ' + str(df[column].unique()))
        print(df[column].value_counts())
        print("_________________________________________________________________")

#Remove unneeded columns

#Remove the column EmployeeNumber
df = df.drop('EmployeeNumber', axis = 1) # A number assignment to the employee
#Remove the column StandardHours
df = df.drop('StandardHours', axis = 1) #Contains only value 80 e.g. df['StandardHours'].unique()
#Remove the column EmployeeCount
df = df.drop('EmployeeCount', axis = 1) #Contains only the value 1 e.g. df['EmployeeCount'].unique()
#Remove the column EmployeeCount
df = df.drop('Over18', axis = 1) #Contains only the value 'Yes'

#Get the correlation of the columns
df.corr()

#Visualize the correlation
plt.figure(figsize=(14,14))  #14in by 14in
sns.heatmap(df.corr(), annot=True, fmt='.0%')

#Transform non-numeric columns into numerical columns
from sklearn.preprocessing import LabelEncoder

for column in df.columns:
        if df[column].dtype == np.number:
            continue
        df[column] = LabelEncoder().fit_transform(df[column])

#Create a new column at the end of the dataframe that contains the same value 
df['Age_Years'] = df['Age']

#Remove the first column called age 
df = df.drop('Age', axis = 1)

#Show the dataframe
df

#Split the data into independent 'X' and dependent 'Y' variables
X = df.iloc[:, 1:df.shape[1]].values #Notice I started from index  2 to 31, essentially removing the id column & diagnosis
Y = df.iloc[:, 0].values #Get the target variable 'diagnosis' located at index=1

# Split the dataset into 75% Training set and 25% Testing set
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.25, random_state = 0)

#Use Random Forest Classification algorithm
  from sklearn.ensemble import RandomForestClassifier
  forest = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
  forest.fit(X_train, Y_train)

#Get the accuracy on the training data
forest.score(X_train, Y_train)

#Show the confusion matrix and accuracy for  the model on the test data
#Classification accuracy is the ratio of correct predictions to total predictions made.
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(Y_test, forest.predict(X_test))
  
TN = cm[0][0]
TP = cm[1][1]
FN = cm[1][0]
FP = cm[0][1]
  
print(cm)
print('Model Testing Accuracy = "{}!"'.format(  (TP + TN) / (TP + TN + FN + FP)))
print()# Print a new line

# Return the feature importances (the higher, the more important the feature).
importances = pd.DataFrame({'feature':df.iloc[:, 1:df.shape[1]].columns,'importance':np.round(forest.feature_importances_,3)}) #Note: The target column is at position 0
importances = importances.sort_values('importance',ascending=False).set_index('feature')
importances

#Visualize the importance
importances.plot.bar()