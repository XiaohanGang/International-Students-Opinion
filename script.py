#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 23:56:32 2024

@author: gangxiaohan
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
pip install factor-analyzer
from factor_analyzer import FactorAnalyzer

# Clean the data

# Open the file 

data = pd.read_csv('int_results.csv', encoding='latin1')

# Select the columns for analysis

L = ['Q2','Q3','Q4','Q5','Q22','Q39_1','Q39_2','Q39_3','Q39_4','Q39_5','Q39_6','Q39_7']
variables = data[L]

# Change column name

fix_name = {'Q2': 'age', 'Q3': 'gender', 'Q4': 'degree', 'Q5': 'discipline', 'Q22': 'region', 'Q39_1': 'att_1','Q39_2': 'att_2','Q39_3': 'att_3','Q39_4': 'att_4','Q39_5': 'att_5','Q39_6': 'att_6','Q39_7': 'att_7'}
variables = variables.rename(columns=fix_name)

# Group countries into regions

asia = [44,91,161,190,4,16,19,53,88,92,96,99,100,105,106,109,121,132,139,150,157,168,172,180,193,213]
variables['region'] = variables['region'].replace(asia, 'Asian')

africa = [24,60,65,77,102,146,177,202,221]
variables['region'] = variables['region'].replace(africa, 'African')

white = [38,76,14,143,5,15,22,51,55,69,70,79,89,90,95,97,140,158,159,163,164,173,179,205]
variables['region'] = variables['region'].replace(white, 'White')

variables['region'] = variables['region'].apply(lambda x: 'Other' if isinstance(x, (int, float)) else x)

# Change age into meaningful categories

age_mapping = {
    2: '<18',
    3: '18-25',
    5: '26-30',
    6: '31-35',
    7: '36-40',
    8: '41-45'
}

for value, label in age_mapping.items():
    variables['age'] = variables['age'].replace(value, label)

# Change gender into meaningful categories

gender_mapping = {
    1: 'male',
    2: 'female',
    4: 'na'
}

for value, label in gender_mapping.items():
    variables['gender'] = variables['gender'].replace(value, label)

# Change degree into meaningful categories

degree_mapping = {
    1: 'master',
    2: 'phd',
}

for value, label in degree_mapping.items():
    variables['degree'] = variables['degree'].replace(value, label)


# Change degree into meaningful categories

discipline_mapping = {
    1: 'Life Sciences',
    2: 'Physical Sciences',
    3: 'Engineering',
    4: 'Mathematics',
    5: 'Computer Science',
    6: 'Other'
}

for value, label in discipline_mapping.items():
    variables['discipline'] = variables['discipline'].replace(value, label)
    
# Calculate the score of attitude rates

variables['att_rates'] = variables['att_1'] + variables['att_2'] + variables['att_3'] + variables['att_4'] + variables['att_5'] + variables['att_6'] + variables['att_7']

#%%

# Produce distribution of the dependent variable - attitudes

fig, ax1 = plt.subplots()
sns.histplot(data=variables, x=variables['att_rates'], hue=variables["region"], kde=True, ax=ax1)
fig.tight_layout()
fig.savefig("attitudes.png")

#%%

# Produce a quick overview of the primary independent variable (country) and the control variables

ctr_vars = ['age', 'gender', 'degree', 'discipline', 'region']

for var in ctr_vars:
    print(var)
    print(variables[var].value_counts())
    fig = sns.catplot(y=var, data=variables, kind="count")

#%%

# Factor Analysis of the dependent variable

df_dep_var = variables[['att_1', 'att_2', 'att_3', 'att_4', 'att_5', 'att_6', 'att_7']]

fa = FactorAnalyzer()
fa.fit(df_dep_var)

# Use Kaiser criterion (eigenvalues greater than 1)
print("Eigenvalues:")
print(fa.get_eigenvalues())

# Get factor loadings
loadings = fa.loadings_
print("Factor Loadings:")
print(loadings)


#%%

# Set up for OLS regression model

# Set up the primary independent variable - regions

regions = {
    'Asian': {'Asian': 1, 'White': 0, 'African': 0, 'Other': 0},
    'White': {'Asian': 0, 'White': 1, 'African': 1, 'Other': 1},
    'African': {'Asian': 0, 'White': 0, 'African': 1, 'Other': 0},
    'Other': {'Asian': 0, 'White': 0, 'African': 0, 'Other': 1}
}

for region, values in regions.items():
    variables[region] = variables['region'].replace(values)
    
# Set up the control variables

ages = {
    '<30': {'<18': 1, '18-25': 1, '26-30': 1, '31-35': 0, '36-40': 0, '41-45': 0},
    '31-35': {'<18': 0, '18-25': 0, '26-30': 0, '31-35': 1, '36-40': 0, '41-45': 0},
    '36-40': {'<18': 0, '18-25': 0, '26-30': 0, '31-35': 0, '36-40': 1, '41-45': 0},
    '41-45': {'<18': 0, '18-25': 0, '26-30': 0, '31-35': 0, '36-40': 0, '41-45': 1},
}

for age, values in ages.items():
    variables[age] = variables['age'].replace(values)
    
genders = {
    'male': {'male': 1, 'female': 0, 'na': 0},
    'female': {'male': 0, 'female': 1, 'na': 0},
    'na': {'male': 0, 'female': 0, 'na': 1},
}

for gender, values in genders.items():
    variables[gender] = variables['gender'].replace(values)

degrees = {
    'master': {'master': 1, 'phd': 0},
    'phd': {'master': 0, 'phd': 1}
}

for degree, values in degrees.items():
    variables[degree] = variables['degree'].replace(values)
    
disciplines = {
    'Life Sciences': {'Life Sciences': 1, 'Physical Sciences': 0, 'Engineering': 0, 'Mathematics': 0, 'Computer Science': 0, 'Other': 0},
    'Physical Sciences': {'Life Sciences': 0, 'Physical Sciences': 1, 'Engineering': 0, 'Mathematics': 0, 'Computer Science': 0, 'Other': 0},
    'Engineering':{'Life Sciences': 0, 'Physical Sciences': 0, 'Engineering': 1, 'Mathematics': 0, 'Computer Science': 0, 'Other': 0},
    'Mathematics':{'Life Sciences': 0, 'Physical Sciences': 0, 'Engineering': 0, 'Mathematics': 1, 'Computer Science': 0, 'Other': 0},
    'Computer Science':{'Life Sciences': 0, 'Physical Sciences': 0, 'Engineering': 0, 'Mathematics': 0, 'Computer Science': 1, 'Other': 0},
    'Other':{'Life Sciences': 0, 'Physical Sciences': 0, 'Engineering': 0, 'Mathematics': 0, 'Computer Science': 0, 'Other': 1}
}

for discipline, values in disciplines.items():
    variables[discipline] = variables['discipline'].replace(values)
    

#%%

# Run an OLS regression model for attitudes international students towards of graduate stem US education

# Model 1 (reference: white)

dep_var  = 'att_rates'
ind_vars = ['Asian', 'African', 'Other']

Y = variables[dep_var]

X = variables[ind_vars]
X = sm.add_constant(X)

model = sm.OLS(Y,X)

results = model.fit()

print( results.summary() )

#%%

# Model 2 (reference: <30)

dep_var  = 'att_rates'
ind_vars = ['Asian', 'African', 'Other', '31-35', '36-40', '41-45']

Y = variables[dep_var]

X = variables[ind_vars]
X = sm.add_constant(X)

model = sm.OLS(Y,X)

results = model.fit()

print( results.summary() )

## Get the coefficients (betas) of the model

betas = results.params
print("Coefficients (Betas):")
print(betas)

#%%

# Model 3 (reference: male)

dep_var  = 'att_rates'
ind_vars = ['Asian', 'African', 'Other', '31-35', '36-40', '41-45', 'female', 'na']

Y = variables[dep_var]

X = variables[ind_vars]
X = sm.add_constant(X)

model = sm.OLS(Y,X)

results = model.fit()

print( results.summary() )

## Get the coefficients (betas) of the model

betas = results.params
print("Coefficients (Betas):")
print(betas)

#%%

# Model 4 (reference: Computer Science)

dep_var  = 'att_rates'
ind_vars = ['Asian', 'African', 'Other', '31-35', '36-40', '41-45', 'female', 'na', 'Life Sciences', 'Physical Sciences', 'Engineering', 'Mathematics', 'Other']

Y = variables[dep_var]

X = variables[ind_vars]
X = sm.add_constant(X)

model = sm.OLS(Y,X)

results = model.fit()

print( results.summary() )

## Get the coefficients (betas) of the model

betas = results.params
print("Coefficients (Betas):")
print(betas)



















