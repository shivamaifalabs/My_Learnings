# 01. List:-

num=[1,2,3,4,5,6,7,8]

result=[x**2 for x in num if x%2==0]
print(result)

# 02. Sets:-

data=[1,2,2,3,4,2,1,34,34,5,7,8,10,21,4]
r={x for x in data if x>20}
print(r)

# 03. Dicts:-

number=[1,2,3,4,5,6,7,8]
output={x:x**2 for x in number if x%2==0}
print(output)
