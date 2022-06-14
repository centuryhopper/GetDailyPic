import os

print(os.getcwd())
print(os.path.basename(__file__))
print(os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))
print(os.getcwd())

if __name__ == '__main__':
    print('in main')
