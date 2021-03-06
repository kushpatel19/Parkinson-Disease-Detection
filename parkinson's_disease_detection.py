# -*- coding: utf-8 -*-
"""Parkinson's Disease Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SGYlwcqOOPv9LHtSUSVtWaS2JD9CT4TC

Importing Required Libraries
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

"""Data Collection & Analysis"""

# Loading the data from csv file to a Pandas DataFrame
parkinsons_data = pd.read_csv('https://github.com/kushpatel19/Parkinson-Disease-Detection/blob/main/parkinsons.data')

# First 5 rows of the dataframe
parkinsons_data.head()

# Number of rows and columns in the dataframe
parkinsons_data.shape

# Getting more information about the dataset
parkinsons_data.info()

# Checking for missing values in each column
parkinsons_data.isnull().sum()

# Getting some statistical measures about the data
parkinsons_data.describe()

# Distribution of target Variable
parkinsons_data['status'].value_counts()

"""1  --> Parkinson's Disease Positive

0 --> Parkinson's Disease Negative (Healthy)

"""

# Grouping the data based on the target variable
parkinsons_data.groupby('status').mean()

"""Data Pre-Processing

Separating the features & Target
"""

X = parkinsons_data.drop(columns=['name','status'], axis=1)
Y = parkinsons_data['status']
print(X)
print(Y)

"""Splitting the data to training data & Test data"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

print(X.shape, X_train.shape, X_test.shape)

"""Data Standardization                                                           

---



Standardization is an important technique that is mostly performed as a pre-processing step before many Machine Learning models, to standardize the range of features of input data set.
"""

scaler = StandardScaler()

scaler.fit(X_train)

X_train = scaler.transform(X_train)

X_test = scaler.transform(X_test)

print(X_train)

"""Model Training                                                                  
Machine Learning Classification

Let's try all the clasification models                                        

- Support Vector Machine Model
- Logistic Regression
- AdaBoost Classifier 
- RandomForest Classifier
- GaussianNB
- K Nearest Neighbor(KNN)
- DecisionTree Classifier
- XGB Classifier 
- XGBRF Classifier
"""

from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from xgboost import XGBRFClassifier
from sklearn.ensemble import AdaBoostClassifier

def accuracy(model, title):
  model.fit(X_train, Y_train)
  predictions = model.predict(X_test)
  acc = accuracy_score(Y_test, predictions)
  print('Accuracy for', title, 'is :-', acc,'\n')

model_1 = svm.SVC(kernel='rbf')
accuracy(model_1,'Support Vector Machine Model')
model_2 = LogisticRegression()
accuracy(model_2,'Logistic Regression')
model_3 = AdaBoostClassifier()
accuracy(model_3,'Ada')
model_4 = RandomForestClassifier()
accuracy(model_4,'Random Forest')
model_5 = GaussianNB()
accuracy(model_5,'NBG')
model_6 = KNeighborsClassifier()
accuracy(model_6,'K Nearest Neighbor(KNN)')
model_7 = DecisionTreeClassifier()
accuracy(model_7,'Decision Tree')
model_8 = XGBClassifier()
accuracy(model_8,'XGB')
model_9 = XGBRFClassifier()
accuracy(model_9,'XGBRF')

"""Now, we will select the best model among them according to the highest score of accuracy

Here, SVM and AdaBoostClassifier both give same as well as highest score.    
So, we can continue with any of them. (Let's choose Support Vector Machine Model)
"""

best_model = model_1

best_model.get_params()

"""Model Evaluation

Accuracy Score
"""

# accuracy score on training data
X_train_prediction = best_model.predict(X_train)
training_data_accuracy = accuracy_score(Y_train, X_train_prediction)
print('Accuracy score of training data : ', training_data_accuracy)

# accuracy score on training data
X_test_prediction = best_model.predict(X_test)
test_data_accuracy = accuracy_score(Y_test, X_test_prediction)
print('Accuracy score of test data : ', test_data_accuracy)
print(classification_report(Y_test,X_test_prediction))

"""Building a Predictive System"""

input_data = (197.07600,206.89600,192.05500,0.00289,0.00001,0.00166,0.00168,0.00498,0.01098,0.09700,0.00563,0.00680,0.00802,0.01689,0.00339,26.77500,0.422229,0.741367,-7.348300,0.177551,1.743867,0.085569)

# changing input data to a numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the numpy array
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

# standardize the data
std_data = scaler.transform(input_data_reshaped)

prediction = best_model.predict(std_data)
print(prediction)

if (prediction[0] == 0):
  print("The Person does not have Parkinsons Disease")

else:
  print("The Person has Parkinsons Disease")

"""Hyperparameter Tuning for increasing accuracy"""

# See all the parameters
best_model.get_params()

"""Important Perameter :-                                                         
- C 
- gamma
- kernel

1. GridSearchCV
"""

from sklearn.model_selection import GridSearchCV
 
# defining parameter range
param_grid = {'C': [0.1, 1, 10, 100, 1000],
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'kernel': ['rbf','linear'],
              'cache_size': [0.1, 1, 10, 100, 1000],
              'degree' : [0.1,1,10]}
 
grid = GridSearchCV(svm.SVC(), param_grid, refit = True, verbose = 10)
 
# fitting the model for grid search
grid.fit(X_train, Y_train)

# print best parameter after tuning
print(grid.best_params_)
# print how our model looks after hyper-parameter tuning
print(grid.best_estimator_)
grid_predictions = grid.predict(X_test)
# print classification report
print(classification_report(Y_test, grid_predictions))

# # example of grid searching key hyperparametres for SVC
# from sklearn.datasets import make_blobs
# from sklearn.model_selection import RepeatedStratifiedKFold
# from sklearn.model_selection import GridSearchCV
# from sklearn.svm import SVC
# # define dataset
# # X, y = make_blobs(n_samples=1000, centers=2, n_features=100, cluster_std=20)
# # define model and parameters
# model = SVC()
# kernel = ['poly', 'rbf', 'sigmoid','linear']
# C = [100, 50, 10, 1.0, 0.1, 0.01]
# gamma=[1, 0.1, 0.01, 0.001, 0.0001]
# # gamma = ['scale']
# # define grid search
# grid = dict(kernel=kernel,C=C,gamma=gamma)
# cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
# grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring='accuracy',error_score=0)
# grid_result = grid_search.fit(X_train, Y_train)
# # summarize results
# print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
# means = grid_result.cv_results_['mean_test_score']
# stds = grid_result.cv_results_['std_test_score']
# params = grid_result.cv_results_['params']
# for mean, stdev, param in zip(means, stds, params):
#     print("%f (%f) with: %r" % (mean, stdev, param))

"""2. RandomizedSearchCV"""

from sklearn.model_selection import RandomizedSearchCV
 
# defining parameter range
param_grid = {'C': [0.1, 1, 10, 100, 1000],
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'kernel': ['rbf'],
              'cache_size': [0.1, 1, 10, 100, 1000],
              'degree' : [0.1,1,10]}
 
random_search = RandomizedSearchCV(svm.SVC(), param_grid, refit = True, verbose = 10)
 
# fitting the model for random_search
random_search.fit(X_train, Y_train)

# print best parameter after tuning
print(random_search.best_params_)
# print how our model looks after hyper-parameter tuning
print(random_search.best_estimator_)
random_search_predictions = random_search.predict(X_test)
# print classification report
print(classification_report(Y_test, random_search_predictions))

"""Before Hyperparameter Tuning  :-                                                                    
- Accuracy :-  89.74%                                                                          

After Hyperparameter Tuning  :-    
- Accuracy by GridSearchCV :- 92%
- Accuracy by RandomizedSearchCV :- 92%                                         


"""