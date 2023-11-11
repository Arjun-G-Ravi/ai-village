import os
from time import sleep
from random import random, randint
from classes import Village
def main():
    day = 1
    v = Village()
    while True:
        os.system('clear')
        print(f"   DAY {day}\n",'-'*10,'\n','-'*10)
        v.display()        
        sleep(3)
        
        day += 1
    


if __name__ == '__main__':
    main()