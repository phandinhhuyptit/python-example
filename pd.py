import pandas as pd
import matplotlib.pyplot as plt

# Create a sample DataFrame
data = {
    'Year': [2015, 2016, 2017, 2018, 2019],
    'Revenue': [100000, 120000, 150000, 180000, 200000],
    'Expenses': [80000, 90000, 110000, 140000, 160000]
}

df = pd.DataFrame(data)

# Plotting using pandas built-in functions
df.plot(x='Year', y=['Revenue', 'Expenses'], kind='line', marker='o')
plt.title('Revenue and Expenses Over Years')
plt.xlabel('Year')
plt.ylabel('Amount')
plt.grid(True)
plt.show()
