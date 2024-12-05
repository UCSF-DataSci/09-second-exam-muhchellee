import pandas as pd
import numpy as np
import random

# 1. Load and structure the data
## reading processed CSV file
ms_data = pd.read_csv('ms_data.csv')

## converting visit_date to datetime and sorting by patient_id and visit_date
ms_data['visit_date'] = pd.to_datetime(ms_data['visit_date'])
ms_data = ms_data.sort_values(by=['patient_id', 'visit_date'])

## handling missing data
ms_data = ms_data.dropna(subset=['patient_id', 'visit_date']) # removing rows with missing patient_id or visit_date

if ms_data['walking_speed'].isnull().any(): # imputing missing walking_speed values with the mean
        ms_data['walking_speed'] = ms_data['walking_speed'].fillna(ms_data['walking_speed'].mean()) 


# 2. Add insurance information
## reading insurance types from `insurance.lst`
with open('insurance.lst', 'r') as file:
    insurance_types = file.read().splitlines()[1:] # ignore header

## randomly assign insurance type to each patient_id
np.random.seed(88)  
patient_ids = ms_data['patient_id'].unique()
patient_insurance = {
    patient_id: np.random.choice(insurance_types) for patient_id in patient_ids
}
ms_data['insurance_type'] = ms_data['patient_id'].map(patient_insurance)

## generate visit costs based on insurance type and add random variation
insurance_cost_base = {'Bronze': 100, 'Silver': 200, 'Gold': 300}
ms_data['visit_cost'] = ms_data['insurance_type'].map(insurance_cost_base)
ms_data['visit_cost'] += np.random.normal(loc=0, scale=20, size=len(ms_data))


# 3. Calculate summary statistics
## mean walking speed by education level
walking_speed_by_education = ms_data.groupby('education_level')['walking_speed'].mean()

## mean costs by insurance type
mean_costs_by_insurance = ms_data.groupby('insurance_type')['visit_cost'].mean()

## corr coeff of age effect on walking speed
age_walking_corr = ms_data['age'].corr(ms_data['walking_speed'])

## outputting results
print("Mean walking speed by education level:")
print(walking_speed_by_education)

print("\nMean costs by insurance type:")
print(mean_costs_by_insurance)

print("\nCorrelation between age and walking speed:")
print(f"{age_walking_corr:.2f}")
