#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 11:42:59 2024

@author: gangxiaohan
"""

import pandas as pd

# Clean the data

# Open the file 

data = pd.read_csv('int_results.csv', encoding='latin1')
country_list = pd.read_csv('country_list.csv', encoding='latin1')

# Select the columns for analysis

L = ['Q2','Q3','Q4','Q5','Q22','Q39_1','Q39_2','Q39_3','Q39_4','Q39_5','Q39_6','Q39_7']
variables = data[L]

# Change column name

fix_name = {'Q2': 'age', 'Q3': 'gender', 'Q4': 'degree', 'Q5': 'discipline', 'Q22': 'country', 'Q39_1': 'att_1','Q39_2': 'att_2','Q39_3': 'att_3','Q39_4': 'att_4','Q39_5': 'att_5','Q39_6': 'att_6','Q39_7': 'att_7'}
variables = variables.rename(columns=fix_name)

# Create a column of regions in the country list 

country_list['region'] = country_list['Country Code']

# Recategorize the countries into regions

east_asia = [44,161,190,88,92,99,121,132,172,193,213]
country_list['region'] = country_list['region'].replace(east_asia, 'East Asia')

south_asia = [91,19,139,157,180]
country_list['region'] = country_list['region'].replace(south_asia, 'South Asia')

middle_east = [4,16,53,96,100,105,106,109,150,168]
country_list['region'] = country_list['region'].replace(middle_east, 'Middle East')

africa = [24,60,65,77,102,146,177,202,221]
country_list['region'] = country_list['region'].replace(africa, 'Africa')

white = [38,76,14,143,5,15,22,51,55,69,70,79,89,90,95,97,140,158,159,163,164,173,179,205]
country_list['region'] = country_list['region'].replace(white, 'White')

country_list['region'] = country_list['region'].apply(lambda x: 'Other' if isinstance(x, (int, float)) else x)

# Merge the dataframes

variables = variables.merge(country_list, left_on = ['country'], right_on = ['Country Code'], how="left", indicator=True)

print(variables["_merge"].value_counts())
variables = variables.drop(columns='_merge')

#%%

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

# Save the cleaned data

variables.to_csv('data_clean.csv')