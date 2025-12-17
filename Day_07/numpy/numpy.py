my_list=[1,2,3,4,5]
result = [x + 10 for x in my_list]

# In Numpy:-
import numpy as np
arr=np.array(my_list)
result=arr + 10

# arr = np.array([1, 2, 3, 4])

#  OR:---

#arr = np.array([1, 2, 3, 4],[3,4,5,6])

arr = np.array([1,2,3])
arr * 10      # output: [10 20 30]


# Mathematical - Operations:--
'''
arr + 5
arr - 3
arr * 2
arr / 2
np.sqrt(arr)
np.exp(arr)
np.log(arr)

'''


# Aggregations:--

'''
arr.sum()
arr.mean()
arr.std()
arr.min()
arr.max()
arr.sum(axis=0)    # column-wise sum
arr.sum(axis=1)    # row-wise sum

'''

# Boolean - Masking:--

'''
arr = np.array([10, 20, 30, 40])
mask = arr > 25
# mask = [False False True True]

arr[mask]   # [30 40]

'''

# Remove invalid negative values:---

data = np.array([12, 15, -5, 18, 20, -3])
cleaned_data = data[data>=0]

