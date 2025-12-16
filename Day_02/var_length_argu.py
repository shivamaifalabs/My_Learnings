
# 01 *args :-

def add(*args):
    return sum(args)
print(add(1,2,3,4,5))

# 02. **kwargs :-

def fun(**kwargs):
    for key,value in kwargs.items():
        print(f'{key} : {value}')
fun(a=10,b=20,c=30)