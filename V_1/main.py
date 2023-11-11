import os
from time import sleep
from random import random, randint
from classes import Village
def main():
    day = 1
    v = Village()
    while True:
        os.system('clear')
        for t in range(24):
            print(f"   DAY {day} |",f'Time = {t}:00\n','-'*10,'\n','-'*10)
            v.display()        
            sleep(1)
        
        day += 1
    


if __name__ == '__main__':
    main()