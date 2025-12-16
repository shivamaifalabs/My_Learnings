
import time

def slow():
    time.sleep(1)

def compute():
    for _ in range(1000000):
        pass

def run():
    slow()
    compute()

if __name__ == "__main__":
    run()
