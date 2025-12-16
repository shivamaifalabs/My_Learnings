# Scope:-

x="global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print("Inner:", x)
    
    inner()
    print("Outer:", x)

outer()
print("Global:", x)


# 02 Closures:-

def outer():
    message = "Hello"   # Enclosing variable

    def inner():
        print(message)  # Inner function uses outer variable
    
    return inner  # Return the inner function (without calling it)

my_func = outer()
my_func()

# Closures with arguments:-

def multiplier(n):
    def inner(x):
        return x * n
    return inner

times3 = multiplier(3)
times5 = multiplier(5)

print(times3(10))  # 30
print(times5(10))  # 50

