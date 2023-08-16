import pandas as pd

data = pd.DataFrame({
    'A': [True, True, False, True],
    'B': [False, True, True, True],
    'C': [True, False, False, True]
})

# Check if all elements in each column are True
result = data.apply(lambda column: column.all(), axis=0)
print(result)