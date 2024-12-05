import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

## loading data
ms_data = pd.read_csv('ms_data_clean.csv')
ms_data['visit_date'] = pd.to_datetime(ms_data['visit_date'])


# 1. Analyze walking speed
## building multiple regression model
model = smf.ols(
    "walking_speed ~ education_level + age",  
    data=ms_data,
    groups=ms_data["patient_id"]  
)
result = model.fit()

## printing summary
print(result.summary())


# 2. Analyze costs
## simple analysis of insurance type effect
### basic statistics
mean_costs = ms_data.groupby('insurance_type')['visit_cost'].agg(['min', 'mean', 'median', 'max', 'std'])
print("Mean costs by insurance type:")
print(mean_costs)

### ANOVA on insurance type
insurance_anova = sm.stats.anova_lm(sm.OLS.from_formula("visit_cost ~ C(insurance_type)", ms_data).fit(), typ=2)
print(insurance_anova)


## box plot for costs by insurance type
#sns.boxplot(x='insurance_type', y='visit_cost', data=ms_data)
#plt.title('Visit Costs by Insurance Type')
#plt.xlabel('Insurance Type')
#plt.ylabel('Visit Cost')
#plt.show()


## calculating effect sizes
sum_sq_model = insurance_anova['sum_sq']['C(insurance_type)']
sum_sq_total = insurance_anova['sum_sq'].sum()
eta_squared = sum_sq_model / sum_sq_total
print(f"Effect size (eta squared): {eta_squared:.3f}")


# 3. Advanced analysis
## education age interaction model to look at effects on walking speed; controlling for confounders (insurance_type)
interaction_model = smf.mixedlm(
    "walking_speed ~ C(education_level) * age + insurance_type",  
    data=ms_data,
    groups=ms_data["patient_id"]
)
interaction_result = interaction_model.fit()

## printing summary
print(interaction_result.summary())
