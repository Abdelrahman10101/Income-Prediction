# -*- coding: utf-8 -*-
"""Income prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fYDvb0cJfPmKGwWuSPQlHdPzzw7Mwg2h

# Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif

logreg = LogisticRegression()
logreg_corr = LogisticRegression()
logreg_rank = LogisticRegression()
logreg_ig = LogisticRegression()

# %matplotlib inline 

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_csv("/content/drive/MyDrive/نسخة من train_data.csv")

data['capital-total'] = data['capital-gain'] + (-1 * data['capital-loss'])
data = data.drop(['capital-gain', 'capital-loss'], axis=1)

"""# Data Preprocessing

**1-Data cleaning**

Duplicates
"""

data = data.drop_duplicates()

"""Missing Values"""

print (data.isnull().sum())

data=data.dropna()

unique_values = {}
for column in data:
    unique_values[column] = data[column].unique()

print(unique_values)

workclass_mode = data['workclass'].mode()[0]
data['workclass'] = data['workclass'].replace(' ?', workclass_mode)

occupation_mode = data['occupation'].mode()[0]
data['occupation'] = data['occupation'].replace(' ?', occupation_mode)

native_country_mode = data['native-country'].mode()[0]
data['native-country'] = data['native-country'].replace(' ?', native_country_mode)

"""Outliers"""

sns.set(style="ticks", color_codes=True)
sns.boxplot(data['age'])
plt.show()

q1, q3 = np.percentile(data['age'], [25, 75])
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
num_outliers = len(data[(data['age'] < lower_bound) | (data['age'] > upper_bound)])
print("Number of outliers in 'age' feature:", num_outliers)



sns.set(style="ticks", color_codes=True)
sns.boxplot(data['hours-per-week'])
plt.show()

q1, q3 = np.percentile(data['hours-per-week'], [25, 75])
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
num_outliers = len(data[(data['hours-per-week'] < lower_bound) | (data['hours-per-week'] > upper_bound)])
print("Number of outliers in 'hours-per-week' feature:", num_outliers)

"""**2-Encoding categorical variables**"""

# data['workclass']=data['workclass'].replace(" State-gov",0)
# data['workclass']=data['workclass'].replace(" Self-emp-not-inc",1)
# data['workclass']=data['workclass'].replace(" Private",2)
# data['workclass']=data['workclass'].replace(" Federal-gov",3)
# data['workclass']=data['workclass'].replace(" Local-gov",4)
# data['workclass']=data['workclass'].replace(" Self-emp-inc",5)
# data['workclass']=data['workclass'].replace(" Without-pay",6)
# data['workclass']=data['workclass'].replace(" Never-worked",7)

data['education'] = data['education'].replace(' Preschool', 0)
data['education'] = data['education'].replace(' 1st-4th', 1)
data['education'] = data['education'].replace(' 5th-6th', 2)
data['education'] = data['education'].replace(' 7th-8th', 3)
data['education'] = data['education'].replace(' 9th', 4)
data['education'] = data['education'].replace(' 10th', 5)
data['education'] = data['education'].replace(' 11th', 6)   
data['education'] = data['education'].replace(' 12th', 7)
data['education'] = data['education'].replace(' HS-grad', 8)
data['education'] = data['education'].replace(' Some-college', 9)
data['education'] = data['education'].replace(' Assoc-acdm', 10)
data['education'] = data['education'].replace(' Assoc-voc', 11)
data['education'] = data['education'].replace(' Bachelors', 12)
data['education'] = data['education'].replace(' Masters', 13)
data['education'] = data['education'].replace(' Prof-school', 14)
data['education'] = data['education'].replace(' Doctorate', 15)

# data['marital-status']=data['marital-status'].replace(' Never-married',0)
# data['marital-status']=data['marital-status'].replace(' Married-civ-spouse',1)
# data['marital-status']=data['marital-status'].replace(' Divorced',2)
# data['marital-status']=data['marital-status'].replace(' Married-spouse-absent',3)
# data['marital-status']=data['marital-status'].replace(' Separated',4)
# data['marital-status']=data['marital-status'].replace(' Married-AF-spouse',5)
# data['marital-status']=data['marital-status'].replace(' Widowed',6)

# data['occupation'] = data['occupation'].replace(' Adm-clerical', 0)
# data['occupation'] = data['occupation'].replace(' Exec-managerial', 1)
# data['occupation'] = data['occupation'].replace(' Handlers-cleaners', 2)
# data['occupation'] = data['occupation'].replace(' Prof-specialty', 3)
# data['occupation'] = data['occupation'].replace(' Other-service', 4)
# data['occupation'] = data['occupation'].replace(' Sales', 5)
# data['occupation'] = data['occupation'].replace(' Craft-repair', 6)
# data['occupation'] = data['occupation'].replace(' Transport-moving', 7)
# data['occupation'] = data['occupation'].replace(' Farming-fishing', 8)
# data['occupation'] = data['occupation'].replace(' Machine-op-inspct', 9)
# data['occupation'] = data['occupation'].replace(' Tech-support', 10)
# data['occupation'] = data['occupation'].replace(' Protective-serv', 11)
# data['occupation'] = data['occupation'].replace(' Armed-Forces', 12)
# data['occupation'] = data['occupation'].replace(' Priv-house-serv', 13)

# data['relationship'] = data['relationship'].replace(' Not-in-family', 0)
# data['relationship'] = data['relationship'].replace(' Husband', 1)
# data['relationship'] = data['relationship'].replace(' Wife', 2)
# data['relationship'] = data['relationship'].replace(' Own-child', 3)
# data['relationship'] = data['relationship'].replace(' Unmarried', 4)
# data['relationship'] = data['relationship'].replace(' Other-relative', 5)

# data['race'] = data['race'].replace(' White', 0)
# data['race'] = data['race'].replace(' Black', 1)
# data['race'] = data['race'].replace(' Asian-Pac-Islander', 2)
# data['race'] = data['race'].replace(' Amer-Indian-Eskimo', 3)
# data['race'] = data['race'].replace(' Other', 4)

# data['sex'] = data['sex'].replace(' Male', 0)
# data['sex'] = data['sex'].replace(' Female', 1)

# data['native-country'] = data['native-country'].replace(' United-States', 0)
# data['native-country'] = data['native-country'].replace(' Cambodia', 1)
# data['native-country'] = data['native-country'].replace(' England', 2)
# data['native-country'] = data['native-country'].replace(' Puerto-Rico', 3)
# data['native-country'] = data['native-country'].replace(' Canada', 4)
# data['native-country'] = data['native-country'].replace(' Germany', 5)
# data['native-country'] = data['native-country'].replace(' Outlying-US(Guam-USVI-etc)', 6)
# data['native-country'] = data['native-country'].replace(' India', 7)
# data['native-country'] = data['native-country'].replace(' Japan', 8)
# data['native-country'] = data['native-country'].replace(' Greece', 9)
# data['native-country'] = data['native-country'].replace(' South', 10)
# data['native-country'] = data['native-country'].replace(' China', 11)
# data['native-country'] = data['native-country'].replace(' Cuba', 12)
# data['native-country'] = data['native-country'].replace(' Iran', 13)
# data['native-country'] = data['native-country'].replace(' Honduras', 14)
# data['native-country'] = data['native-country'].replace(' Philippines', 15)
# data['native-country'] = data['native-country'].replace(' Italy', 16)
# data['native-country'] = data['native-country'].replace(' Poland', 17)
# data['native-country'] = data['native-country'].replace(' Jamaica', 18)
# data['native-country'] = data['native-country'].replace(' Vietnam', 19)
# data['native-country'] = data['native-country'].replace(' Mexico', 20)
# data['native-country'] = data['native-country'].replace(' Portugal', 21)
# data['native-country'] = data['native-country'].replace(' Ireland', 22)
# data['native-country'] = data['native-country'].replace(' France', 23)
# data['native-country'] = data['native-country'].replace(' Dominican-Republic', 24)
# data['native-country'] = data['native-country'].replace(' Laos', 25)
# data['native-country'] = data['native-country'].replace(' Ecuador', 26)
# data['native-country'] = data['native-country'].replace(' Taiwan', 27)
# data['native-country'] = data['native-country'].replace(' Haiti', 28)
# data['native-country'] = data['native-country'].replace(' Columbia', 29)
# data['native-country'] = data['native-country'].replace(' Hungary', 30)
# data['native-country'] = data['native-country'].replace(' Guatemala', 31)
# data['native-country'] = data['native-country'].replace(' Nicaragua', 32)
# data['native-country'] = data['native-country'].replace(' Scotland', 33)
# data['native-country'] = data['native-country'].replace(' Thailand', 34)
# data['native-country'] = data['native-country'].replace(' Yugoslavia', 35)
# data['native-country'] = data['native-country'].replace(' El-Salvador', 36)
# data['native-country'] = data['native-country'].replace(' Trinadad&Tobago', 37)
# data['native-country'] = data['native-country'].replace(' Peru', 38)
# data['native-country'] = data['native-country'].replace(' Hong', 39)
# data['native-country'] = data['native-country'].replace(' Holand-Netherlands', 40)

# data['Income '] = data['Income '].replace(' <=50K', 0)
# data['Income '] = data['Income '].replace(' >50K', 1)

data = data.apply(LabelEncoder().fit_transform)
data.head()

"""# Feature Selection

"""

corr_matrix = data.corr()
income_corr = corr_matrix['Income ']
income_related_features = income_corr.drop('Income ')
sorted_corr = income_related_features.sort_values(ascending=False)
print(sorted_corr)

#from mlxtend.feature_selection import SequentialFeatureSelector


X = data.drop(columns=['Income '])
y = data['Income ']

# Create a logistic regression model
#lr = LogisticRegression()

# Forward stepwise selection
# sfs_forward = SequentialFeatureSelector(lr, k_features=5, forward=True, scoring='accuracy', cv=5)
# sfs_forward.fit(X, y)
# selected_features_forward = sfs_forward.k_feature_names_

# Backward stepwise selection
# sfs_backward = SequentialFeatureSelector(lr, k_features=5, forward=False, scoring='accuracy', cv=5)
# sfs_backward.fit(X, y)
# selected_features_backward = sfs_backward.k_feature_names_

# print('Forward stepwise selection: ', selected_features_forward)
# print('Backward stepwise selection: ', selected_features_backward)


#education-num     0.323388
#age               0.229109
#hours-per-week    0.228966
#capital-total     0.212918
#workclass         0.097422
#marital-status    0.000763
#fnlwgt           -0.017083
#education        -0.049630
#native-country   -0.055517
#occupation       -0.055844
#race             -0.078403
#relationship     -0.167260
#sex              -0.206807

#'education-num'   'race'   'capital-total'

from sklearn.feature_selection import RFE

feature_names = list(X.columns)
# Create an RFE object and fit it to the data
rfe = RFE(estimator=logreg, n_features_to_select=5, step=1)
rfe.fit(X, y)

# Get the ranked features with their corresponding names
ranked_features = [(rank, name) for rank, name in zip(rfe.ranking_, feature_names)]
ranked_features.sort()

print('Ranking of features:')
for rank, name in ranked_features:
    print(f'{rank}. {name}')

# Get the top 5 features
top_features = [name for rank, name in ranked_features if rank == 1]
data_rank = data[top_features + ['Income ']]

data_rank = data_rank.drop_duplicates()

print(top_features)

# Compute correlation matrix
corr = data.corr()['Income '].abs().sort_values(ascending=False)

# Drop all features except the top 5
selected_features = corr.nlargest(6).index.tolist()[1:]
data_corr = data[selected_features + ['Income ']]

data_corr = data_corr.drop_duplicates()

sns.pairplot(data_corr)

"""Information Gain"""

mutual_info = mutual_info_classif(X, y)

# Create a DataFrame to store the mutual information scores for each feature
features = pd.DataFrame({"feature": X.columns, "mutual_info": mutual_info})

# Sort the features by their mutual information scores in descending order
features = features.sort_values("mutual_info", ascending=False)

# Select the top 5 features based on their mutual information scores
ig_features = features.head(5)["feature"].values
ig_features=ig_features.tolist()
# Print the selected features
print(ig_features)

# Drop all features except the top 5 and the target variable
data_ig = data[ig_features+ ["Income "]]

# Remove duplicate rows if necessary
data_ig = data_ig.drop_duplicates()

"""# Classification Models

**1-Correlation**

1-Logistic Regression
"""

train_X_corr = data_corr.drop('Income ', axis=1)
train_y_corr = data_corr['Income ']

logreg_corr.fit(train_X_corr, train_y_corr)

train_y_corr_pred_logreg = logreg_corr.predict(train_X_corr)
accuracy = accuracy_score(train_y_corr, train_y_corr_pred_logreg)
print("Accuracy:", accuracy)

"""2-SVM"""

svm_corr = SVC()
svm_corr.fit(train_X_corr, train_y_corr)
train_y_corr_pred_svm = svm_corr.predict(train_X_corr)
accuracy = accuracy_score(train_y_corr, train_y_corr_pred_svm )
print("Accuracy:", accuracy)

"""3- Decision Tree"""

dt_corr = DecisionTreeClassifier()
dt_corr.fit(train_X_corr, train_y_corr)
train_y_corr_pred_dt = dt_corr.predict(train_X_corr)
accuracy = accuracy_score(train_y_corr, train_y_corr_pred_dt)
print("Accuracy:", accuracy)

dt_corr_regul = DecisionTreeClassifier(ccp_alpha=0.01)  # set the ccp_alpha parameter to apply pruning
dt_corr_regul.fit(train_X_corr, train_y_corr)
train_y_corr_regul_pred_dt = dt_corr_regul.predict(train_X_corr)
accuracy = accuracy_score(train_y_corr, train_y_corr_regul_pred_dt)
print("Accuracy:", accuracy)

from sklearn.model_selection import cross_val_score

#dt = DecisionTreeClassifier()
scores = cross_val_score(dt_corr, train_X_corr, train_y_corr, cv=5)
print("Accuracy without regularization: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

#dt_regul = DecisionTreeClassifier(ccp_alpha=0.01)
scores = cross_val_score(dt_corr_regul, train_X_corr, train_y_corr, cv=5)
print("Accuracy with regularization: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

"""**2-Ranked Features**

1-Logistic Regression
"""

train_X_rank = data_rank.drop('Income ', axis=1)
train_y_rank = data_rank['Income ']

logreg_rank.fit(train_X_rank, train_y_rank)

train_y_rank_pred_logreg = logreg_rank.predict(train_X_rank)
accuracy = accuracy_score(train_y_rank, train_y_rank_pred_logreg)
print("Accuracy:", accuracy)

"""2-SVM"""

svm_rank = SVC()
svm_rank.fit(train_X_rank, train_y_rank)
train_y_rank_pred_svm = svm_rank.predict(train_X_rank)
accuracy = accuracy_score(train_y_rank, train_y_rank_pred_svm)
print("Accuracy:", accuracy)

"""3-Decision Tree"""

dt_rank = DecisionTreeClassifier()
dt_rank.fit(train_X_rank, train_y_rank)
train_y_rank_pred_dt = dt_rank.predict(train_X_rank)
accuracy = accuracy_score(train_y_rank, train_y_rank_pred_dt)
print("Accuracy:", accuracy)

dt_rank_regul = DecisionTreeClassifier(ccp_alpha=0.01)  # set the ccp_alpha parameter to apply pruning
dt_rank_regul.fit(train_X_rank, train_y_rank)
train_y_rank_regul_pred_dt = dt_rank_regul.predict(train_X_rank)
accuracy = accuracy_score(train_y_rank, train_y_rank_regul_pred_dt)
print("Accuracy:", accuracy)

"""**3-IG Features**"""

#logreg_ig
train_X_ig = data_ig.drop('Income ', axis=1)
train_y_ig = data_ig['Income ']

"""1-Logistic Regression"""

logreg_ig.fit(train_X_ig, train_y_ig)

train_y_ig_pred_logreg = logreg_ig.predict(train_X_ig)
accuracy = accuracy_score(train_y_ig, train_y_ig_pred_logreg)
print("Accuracy:", accuracy)

"""2-SVM"""

svm_ig = SVC()
svm_ig.fit(train_X_ig, train_y_ig)
train_y_ig_pred_svm = svm_ig.predict(train_X_ig)
accuracy = accuracy_score(train_y_ig, train_y_ig_pred_svm)
print("Accuracy:", accuracy)

"""3-Decision Tree"""

dt_ig = DecisionTreeClassifier()
dt_ig.fit(train_X_ig, train_y_ig)
train_y_ig_pred_dt = dt_ig.predict(train_X_ig)
accuracy = accuracy_score(train_y_ig, train_y_ig_pred_dt)
print("Accuracy:", accuracy)

dt_ig_regul = DecisionTreeClassifier(ccp_alpha=0.01)  # set the ccp_alpha parameter to apply pruning
dt_ig_regul.fit(train_X_ig, train_y_ig)
train_y_ig_regul_pred_dt = dt_ig_regul.predict(train_X_ig)
accuracy = accuracy_score(train_y_ig, train_y_ig_regul_pred_dt)
print("Accuracy:", accuracy)

"""# Test Data: Preprocessing"""

test_data = pd.read_csv("/content/drive/MyDrive/نسخة من test_data.csv")

test_data['capital-total'] =test_data['capital-gain'] + (-1 * test_data['capital-loss'])
test_data = test_data.drop(['capital-gain', 'capital-loss'], axis=1)

test_data = test_data.drop_duplicates()

print (test_data.isnull().sum())

unique_values = {}
for column in test_data:
    unique_values[column] = test_data[column].unique()

print(unique_values)

workclass_mode = test_data['workclass'].mode()[0]
test_data['workclass'] = test_data['workclass'].replace(' ?', workclass_mode)

occupation_mode = test_data['occupation'].mode()[0]
test_data['occupation'] = test_data['occupation'].replace(' ?', occupation_mode)

native_country_mode = test_data['native-country'].mode()[0]
test_data['native-country'] = test_data['native-country'].replace(' ?', native_country_mode)

test_data['education'] = test_data['education'].replace(' Preschool', 0)
test_data['education'] = test_data['education'].replace(' 1st-4th', 1)
test_data['education'] = test_data['education'].replace(' 5th-6th', 2)
test_data['education'] = test_data['education'].replace(' 7th-8th', 3)
test_data['education'] = test_data['education'].replace(' 9th', 4)
test_data['education'] = test_data['education'].replace(' 10th', 5)
test_data['education'] = test_data['education'].replace(' 11th', 6)   
test_data['education'] = test_data['education'].replace(' 12th', 7)
test_data['education'] = test_data['education'].replace(' HS-grad', 8)
test_data['education'] = test_data['education'].replace(' Some-college', 9)
test_data['education'] = test_data['education'].replace(' Assoc-acdm', 10)
test_data['education'] = test_data['education'].replace(' Assoc-voc', 11)
test_data['education'] = test_data['education'].replace(' Bachelors', 12)
test_data['education'] = test_data['education'].replace(' Masters', 13)
test_data['education'] = test_data['education'].replace(' Prof-school', 14)
test_data['education'] = test_data['education'].replace(' Doctorate', 15)

test_data = test_data.apply(LabelEncoder().fit_transform)

# test_data['workclass'] = test_data['workclass'].replace(" State-gov", 0)
# test_data['workclass'] = test_data['workclass'].replace(" Self-emp-not-inc", 1)
# test_data['workclass'] = test_data['workclass'].replace(" Private", 2)
# test_data['workclass'] = test_data['workclass'].replace(" Federal-gov", 3)
# test_data['workclass'] = test_data['workclass'].replace(" Local-gov", 4)
# test_data['workclass'] = test_data['workclass'].replace(" Self-emp-inc", 5)
# test_data['workclass'] = test_data['workclass'].replace(" Without-pay", 6)
# test_data['workclass'] = test_data['workclass'].replace(" Never-worked", 7)

# test_data['education'] = test_data['education'].replace(' Bachelors', 0)
# test_data['education'] = test_data['education'].replace(' HS-grad', 1)
# test_data['education'] = test_data['education'].replace(' 11th', 2)
# test_data['education'] = test_data['education'].replace(' Masters', 3)
# test_data['education'] = test_data['education'].replace(' 9th', 4)
# test_data['education'] = test_data['education'].replace(' Some-college', 5)
# test_data['education'] = test_data['education'].replace(' Assoc-acdm', 6)
# test_data['education'] = test_data['education'].replace(' Assoc-voc', 7)
# test_data['education'] = test_data['education'].replace(' 7th-8th', 8)
# test_data['education'] = test_data['education'].replace(' Doctorate', 9)
# test_data['education'] = test_data['education'].replace(' Prof-school', 10)
# test_data['education'] = test_data['education'].replace(' 5th-6th', 11)
# test_data['education'] = test_data['education'].replace(' 10th', 12)
# test_data['education'] = test_data['education'].replace(' 1st-4th', 13)
# test_data['education'] = test_data['education'].replace(' Preschool', 14)
# test_data['education'] = test_data['education'].replace(' 12th', 15)

# test_data['marital-status'] = test_data['marital-status'].replace(' Never-married', 0)
# test_data['marital-status'] = test_data['marital-status'].replace(' Married-civ-spouse', 1)
# test_data['marital-status'] = test_data['marital-status'].replace(' Divorced', 2)
# test_data['marital-status'] = test_data['marital-status'].replace(' Married-spouse-absent', 3)
# test_data['marital-status'] = test_data['marital-status'].replace(' Separated', 4)
# test_data['marital-status'] = test_data['marital-status'].replace(' Married-AF-spouse', 5)
# test_data['marital-status'] = test_data['marital-status'].replace(' Widowed', 6)

# test_data['occupation'] = test_data['occupation'].replace(' Adm-clerical', 0)
# test_data['occupation'] = test_data['occupation'].replace(' Exec-managerial', 1)
# test_data['occupation'] = test_data['occupation'].replace(' Handlers-cleaners', 2)
# test_data['occupation'] = test_data['occupation'].replace(' Prof-specialty', 3)
# test_data['occupation'] = test_data['occupation'].replace(' Other-service', 4)
# test_data['occupation'] = test_data['occupation'].replace(' Sales', 5)
# test_data['occupation'] = test_data['occupation'].replace(' Craft-repair', 6)
# test_data['occupation'] = test_data['occupation'].replace(' Transport-moving', 7)
# test_data['occupation'] = test_data['occupation'].replace(' Farming-fishing', 8)
# test_data['occupation'] = test_data['occupation'].replace(' Machine-op-inspct', 9)
# test_data['occupation'] = test_data['occupation'].replace(' Tech-support', 10)
# test_data['occupation'] = test_data['occupation'].replace(' Protective-serv', 11)
# test_data['occupation'] = test_data['occupation'].replace(' Armed-Forces', 12)
# test_data['occupation'] = test_data['occupation'].replace(' Priv-house-serv', 13)

# test_data['relationship'] = test_data['relationship'].replace(' Not-in-family', 0)
# test_data['relationship'] = test_data['relationship'].replace(' Husband', 1)
# test_data['relationship'] = test_data['relationship'].replace(' Wife', 2)
# test_data['relationship'] = test_data['relationship'].replace(' Own-child', 3)
# test_data['relationship'] = test_data['relationship'].replace(' Unmarried', 4)
# test_data['relationship'] = test_data['relationship'].replace(' Other-relative', 5)

# test_data['race'] = test_data['race'].replace(' White', 0)
# test_data['race'] = test_data['race'].replace(' Black', 1)
# test_data['race'] = test_data['race'].replace(' Asian-Pac-Islander', 2)
# test_data['race'] = test_data['race'].replace(' Amer-Indian-Eskimo', 3)
# test_data['race'] = test_data['race'].replace(' Other', 4)

# test_data['sex'] = test_data['sex'].replace(' Male', 0)
# test_data['sex'] = test_data['sex'].replace(' Female', 1)

# test_data['native-country'] = test_data['native-country'].replace(' United-States', 0)
# test_data['native-country'] = test_data['native-country'].replace(' Cambodia', 1)
# test_data['native-country'] = test_data['native-country'].replace(' England', 2)
# test_data['native-country'] = test_data['native-country'].replace(' Puerto-Rico', 3)
# test_data['native-country'] = test_data['native-country'].replace(' Canada', 4)
# test_data['native-country'] = test_data['native-country'].replace(' Germany', 5)
# test_data['native-country'] = test_data['native-country'].replace(' Outlying-US(Guam-USVI-etc)', 6)
# test_data['native-country'] = test_data['native-country'].replace(' India', 7)
# test_data['native-country'] = test_data['native-country'].replace(' Japan', 8)
# test_data['native-country'] = test_data['native-country'].replace(' Greece', 9)
# test_data['native-country'] = test_data['native-country'].replace(' South', 10)
# test_data['native-country'] = test_data['native-country'].replace(' China', 11)
# test_data['native-country'] = test_data['native-country'].replace(' Cuba', 12)
# test_data['native-country'] = test_data['native-country'].replace(' Iran', 13)
# test_data['native-country'] = test_data['native-country'].replace(' Honduras', 14)
# test_data['native-country'] = test_data['native-country'].replace(' Philippines', 15)
# test_data['native-country'] = test_data['native-country'].replace(' Italy', 16)
# test_data['native-country'] = test_data['native-country'].replace(' Poland', 17)
# test_data['native-country'] = test_data['native-country'].replace(' Jamaica', 18)
# test_data['native-country'] = test_data['native-country'].replace(' Vietnam', 19)
# test_data['native-country'] = test_data['native-country'].replace(' Mexico', 20)
# test_data['native-country'] = test_data['native-country'].replace(' Portugal', 21)
# test_data['native-country'] = test_data['native-country'].replace(' Ireland', 22)
# test_data['native-country'] = test_data['native-country'].replace(' France', 23)
# test_data['native-country'] = test_data['native-country'].replace(' Dominican-Republic', 24)
# test_data['native-country'] = test_data['native-country'].replace(' Laos', 25)
# test_data['native-country'] = test_data['native-country'].replace(' Ecuador', 26)
# test_data['native-country'] = test_data['native-country'].replace(' Taiwan', 27)
# test_data['native-country'] = test_data['native-country'].replace(' Haiti', 28)
# test_data['native-country'] = test_data['native-country'].replace(' Columbia', 29)
# test_data['native-country'] = test_data['native-country'].replace(' Hungary', 30)
# test_data['native-country'] = test_data['native-country'].replace(' Guatemala', 31)
# test_data['native-country'] = test_data['native-country'].replace(' Nicaragua', 32)
# test_data['native-country'] = test_data['native-country'].replace(' Scotland', 33)
# test_data['native-country'] = test_data['native-country'].replace(' Thailand', 34)
# test_data['native-country'] = test_data['native-country'].replace(' Yugoslavia', 35)
# test_data['native-country'] = test_data['native-country'].replace(' El-Salvador', 36)
# test_data['native-country'] = test_data['native-country'].replace(' Trinadad&Tobago', 37)
# test_data['native-country'] = test_data['native-country'].replace(' Peru', 38)
# test_data['native-country'] = test_data['native-country'].replace(' Hong', 39)
# test_data['native-country'] = test_data['native-country'].replace(' Holand-Netherlands', 40)

# test_data['Income '] = test_data['Income '].replace(' <=50K.', 0)
# test_data['Income '] = test_data['Income '].replace(' >50K.', 1)

test_data.head()

"""# Test Data: Classification Models

**Correlation**
"""

test_data_corr = test_data[selected_features + ['Income ']]

test_data_corr = test_data_corr.drop_duplicates()

"""1-Logistic regression"""

test_X_corr = test_data_corr.drop('Income ', axis=1)
test_y_corr = test_data_corr['Income ']

test_y_corr_pred_logreg = logreg_corr.predict(test_X_corr)
accuracy = accuracy_score(test_y_corr, test_y_corr_pred_logreg)
print("Accuracy:", accuracy)

"""2-svm"""

test_y_corr_pred_svm  = svm_corr.predict(test_X_corr)
accuracy = accuracy_score(test_y_corr, test_y_corr_pred_svm )
print("Accuracy:", accuracy)

"""3- Decision tree"""

test_y_corr_pred_dt = dt_corr.predict(test_X_corr)
accuracy = accuracy_score(test_y_corr, test_y_corr_pred_dt)
print("Accuracy:", accuracy)

test_y_corr_regul_pred_dt = dt_corr_regul.predict(test_X_corr)
accuracy = accuracy_score(test_y_corr, test_y_corr_regul_pred_dt)
print("Accuracy:", accuracy)

"""**Rank**"""

test_data_rank = test_data[top_features + ['Income ']]

test_data_rank = test_data_rank.drop_duplicates()

"""1-Logistic regression"""

test_X_rank = test_data_rank.drop('Income ', axis=1)
test_y_rank = test_data_rank['Income ']

test_y_rank_pred_logreg = logreg_rank.predict(test_X_rank)
accuracy = accuracy_score(test_y_rank, test_y_rank_pred_logreg)
print("Accuracy:", accuracy)

"""2-SVM"""

test_y_rank_pred_svm = svm_rank.predict(test_X_rank)
accuracy = accuracy_score(test_y_rank, test_y_rank_pred_svm)
print("Accuracy:", accuracy)

"""3-Decision Tree"""

test_y_rank_pred_dt = dt_rank.predict(test_X_rank)
accuracy = accuracy_score(test_y_rank, test_y_rank_pred_dt)
print("Accuracy:", accuracy)

test_y_rank_regul_pred_dt = dt_rank_regul.predict(test_X_rank)
accuracy = accuracy_score(test_y_rank, test_y_rank_regul_pred_dt)
print("Accuracy:", accuracy)

"""**IG**"""

test_data_ig = test_data[ig_features + ['Income ']]
test_data_ig = test_data_ig.drop_duplicates()


test_X_ig = test_data_ig.drop('Income ', axis=1)
test_y_ig = test_data_ig['Income ']

"""1-Logistic regression"""

test_y_ig_pred_logreg = logreg_ig.predict(test_X_ig)
accuracy = accuracy_score(test_y_ig, test_y_ig_pred_logreg)
print("Accuracy:", accuracy)

"""2-SVM"""

test_y_ig_pred_svm = svm_ig.predict(test_X_ig)
accuracy = accuracy_score(test_y_ig, test_y_ig_pred_svm)
print("Accuracy:", accuracy)

"""3-Decision Tree"""

test_y_ig_pred_dt = dt_ig.predict(test_X_ig)
accuracy = accuracy_score(test_y_ig, test_y_ig_pred_dt)
print("Accuracy:", accuracy)

test_y_ig_regul_pred_dt = dt_ig_regul.predict(test_X_ig)
accuracy = accuracy_score(test_y_ig, test_y_ig_regul_pred_dt)
print("Accuracy:", accuracy)

"""# Model Evaluation

**Correlation**

1-Logistic regression
"""



"""2-SVM"""



"""3-Decision Tree"""





models = {
    'Logistic Regression': (train_y_corr_pred_logreg, test_y_corr_pred_logreg),
    'Support Vector Machine': (train_y_corr_pred_svm, test_y_corr_pred_svm),
    'Decision Tree': (train_y_corr_pred_dt, test_y_corr_pred_dt),
    'Regularized Decision Tree': (train_y_corr_regul_pred_dt, test_y_corr_regul_pred_dt)
}

for model_name, (train_pred, test_pred) in models.items():
    print(f'{model_name} - Train Data:')
    print(f'Accuracy: {metrics.accuracy_score(train_y_corr, train_pred)}')
    print(f'Precision: {metrics.precision_score(train_y_corr, train_pred)}')
    print(f'Recall: {metrics.recall_score(train_y_corr, train_pred)}')
    print(f'F1-score: {metrics.f1_score(train_y_corr, train_pred)}')
    print(f'Confusion Matrix:\n{metrics.confusion_matrix(train_y_corr, train_pred)}\n')
    print('-' * 25)
    print(f'{model_name} - Test Data:')
    print(f'Accuracy: {metrics.accuracy_score(test_y_corr, test_pred)}')
    print(f'Precision: {metrics.precision_score(test_y_corr, test_pred)}')
    print(f'Recall: {metrics.recall_score(test_y_corr, test_pred)}')
    print(f'F1-score: {metrics.f1_score(test_y_corr, test_pred)}')
    print(f'Confusion Matrix:\n{metrics.confusion_matrix(test_y_corr, test_pred)}\n')
    print('=' * 50)

"""**Rank**

1-Logistic regression
"""



"""2_SVM"""



"""3-Decision Tree"""





models = {
    'Logistic Regression': (train_y_rank_pred_logreg, test_y_rank_pred_logreg),
    'Support Vector Machine': (train_y_rank_pred_svm, test_y_rank_pred_svm),
    'Decision Tree': (train_y_rank_pred_dt, test_y_rank_pred_dt),
    'Regularized Decision Tree': (train_y_rank_regul_pred_dt, test_y_rank_regul_pred_dt)
}

for model_name, (train_pred, test_pred) in models.items():
    print(f'{model_name} - Train Data:')
    print(f'Accuracy: {metrics.accuracy_score(train_y_rank, train_pred)}')
    print(f'Precision: {metrics.precision_score(train_y_rank, train_pred, zero_division=1)}')
    print(f'Recall: {metrics.recall_score(train_y_rank, train_pred)}')
    print(f'F1-score: {metrics.f1_score(train_y_rank, train_pred)}')
    print(f'Confusion Matrix:\n{metrics.confusion_matrix(train_y_rank, train_pred)}\n')
    print('-' * 25)
    print(f'{model_name} - Test Data:')
    print(f'Accuracy: {metrics.accuracy_score(test_y_rank, test_pred)}')
    print(f'Precision: {metrics.precision_score(test_y_rank, test_pred, zero_division=1)}')
    print(f'Recall: {metrics.recall_score(test_y_rank, test_pred)}')
    print(f'F1-score: {metrics.f1_score(test_y_rank, test_pred)}')
    print(f'Confusion Matrix:\n{metrics.confusion_matrix(test_y_rank, test_pred)}\n')
    print('=' * 50)

"""**IG**

1-Logistic regression
"""



"""2_SVM"""



"""3-Decision Tree"""





models = {
    'Logistic Regression': (train_y_ig_pred_logreg, test_y_ig_pred_logreg),
    'Support Vector Machine': (train_y_ig_pred_svm, test_y_ig_pred_svm),
    'Decision Tree': (train_y_ig_pred_dt, test_y_ig_pred_dt),
    'Regularized Decision Tree': (train_y_ig_regul_pred_dt, test_y_ig_regul_pred_dt)
}

for model_name, (train_pred, test_pred) in models.items():
    print(f'{model_name} - Train Data:')
    print(f'Accuracy: {metrics.accuracy_score(train_y_ig, train_pred)}')
    print(f'Precision: {metrics.precision_score(train_y_ig, train_pred, zero_division=1)}')
    print(f'Recall: {metrics.recall_score(train_y_ig, train_pred)}')
    print(f'F1-score: {metrics.f1_score(train_y_ig, train_pred)}')
    print(f'Confusion Matrix:\n{metrics.confusion_matrix(train_y_ig, train_pred)}\n')
    print('-' * 25)
    print(f'{model_name} - Test Data:')
    print(f'Accuracy: {metrics.accuracy_score(test_y_ig, test_pred)}')
    print(f'Precision: {metrics.precision_score(test_y_ig, test_pred, zero_division=1)}')
    print(f'Recall: {metrics.recall_score(test_y_ig, test_pred)}')
    print(f'F1-score: {metrics.f1_score(test_y_ig, test_pred)}')
    print(f'Confusion Matrix:\n{metrics.confusion_matrix(test_y_ig, test_pred)}\n')
    print('=' * 50)

"""so, correlated SVM is the best model.

"""