import pandas as pd

df = pd.DataFrame({
    "name": ["Shiva", "Arnav"],
    "age": [21, 23]
})

# From CSV:--

# df = pd.read_csv("data.csv")

# Inspecting - Data:--
'''
df.head()    # first 5 rows
df.tail()    # last 5 rows
df.info()    # column types, non-null count
df.describe() # summary statistics
df.shape     # (rows, columns)
df.columns   # list of column names
df.index     # row indices

'''
# Missing - Values:--

'''
df.isnull().sum()            # count nulls
df.dropna()                  # remove rows with nulls
df.fillna(0)                 # replace with 0
df["age"].fillna(df["age"].mean())

'''