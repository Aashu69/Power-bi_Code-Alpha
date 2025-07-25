import pandas as pd
import numpy as np # type: ignore
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# 1. Generate synthetic HR data

np.random.seed(42)

# Employees data
num_employees = 500
start_date = datetime(2015, 1, 1)

# Generate employee join and exit dates
join_dates = [start_date + timedelta(days=np.random.randint(0, 2000)) for _ in range(num_employees)]
exit_dates = []
for jd in join_dates:
    # 70% employees still active, others left randomly between join and today
    if np.random.rand() < 0.7:
        exit_dates.append(pd.NaT)
    else:
        exit_dates.append(jd + timedelta(days=np.random.randint(30, 1000)))

# Employee satisfaction (scale 1-10)
satisfaction = np.random.randint(4, 10, num_employees)

# Performance rating (1-5)
performance = np.random.randint(1, 6, num_employees)

# Employee department
departments = ['Sales', 'IT', 'HR', 'Finance', 'Operations']
department = np.random.choice(departments, num_employees)

# Assemble DataFrame
employees = pd.DataFrame({
    'EmployeeID': range(1, num_employees+1),
    'JoinDate': join_dates,
    'ExitDate': exit_dates,
    'Satisfaction': satisfaction,
    'Performance': performance,
    'Department': department
})

# 2. Recruitment metrics: monthly hires and turnover rates

# Extract hire month
employees['HireMonth'] = employees['JoinDate'].dt.to_period('M')

# Extract exit month
employees['ExitMonth'] = employees['ExitDate'].dt.to_period('M')

# Monthly hires count
monthly_hires = employees.groupby('HireMonth').size().rename('Hires').reset_index()

# Monthly exits count
monthly_exits = employees[employees['ExitMonth'].notna()].groupby('ExitMonth').size().rename('Exits').reset_index()

# Combine hires and exits
monthly_stats = pd.merge(monthly_hires, monthly_exits, left_on='HireMonth', right_on='ExitMonth', how='outer').fillna(0)
monthly_stats['Month'] = monthly_stats['HireMonth'].combine_first(monthly_stats['ExitMonth'])
monthly_stats = monthly_stats[['Month', 'Hires', 'Exits']].sort_values('Month').reset_index(drop=True)

# Calculate turnover rate = Exits / (Exits + Current Employees)
# Approximate current employees for the month (simplified)
monthly_stats['TurnoverRate'] = monthly_stats['Exits'] / (monthly_stats['Exits'] + monthly_stats['Hires'])
monthly_stats['TurnoverRate'] = monthly_stats['TurnoverRate'].fillna(0)

# 3. Analyze employee satisfaction & performance - averages by department
dept_stats = employees.groupby('Department').agg({
    'Satisfaction': 'mean',
    'Performance': 'mean',
    'EmployeeID': 'count'
}).rename(columns={'EmployeeID': 'EmployeeCount'}).reset_index()

# 4. Predictive analytics: Forecast hires next 6 months using linear regression on monthly hires

# Prepare data for model
monthly_stats['MonthNum'] = monthly_stats['Month'].apply(lambda x: x.to_timestamp()).map(pd.Timestamp.toordinal)
X = monthly_stats[['MonthNum']]
y = monthly_stats['Hires']

# Train linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict next 6 months
last_month = monthly_stats['Month'].max()
future_months = [last_month + i for i in range(1, 7)]
future_month_nums = [m.to_timestamp().toordinal() for m in future_months]
X_future = pd.DataFrame({'MonthNum': future_month_nums})

predicted_hires = model.predict(X_future)
predicted_hires = np.maximum(predicted_hires, 0).round().astype(int)

forecast_df = pd.DataFrame({
    'Month': future_months,
    'PredictedHires': predicted_hires
})

# 5. Export processed data to CSV files for Power BI import
monthly_stats.to_csv('monthly_hiring_turnover.csv', index=False)
dept_stats.to_csv('department_satisfaction_performance.csv', index=False)
forecast_df.to_csv('hire_forecast.csv', index=False)

print("Data processing complete. CSV files generated:\n- monthly_hiring_turnover.csv\n- department_satisfaction_performance.csv\n- hire_forecast.csv")
