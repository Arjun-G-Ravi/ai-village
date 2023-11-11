from names import choose_name
from random import choice, randint, random
from time import time, sleep
import os

class Village:
    def __init__(self):
        self.num_houses = 3
        self.houses = [House(i+1) for i in range(self.num_houses)]
        self.village_pop = sum([h.tot_pop for h in self.houses ])

    def display(self):
        for house in self.houses:
            print(house,)
            print(f'Grandparents:')
            for i in house.grand_parents:
                print(i)
            print(f'Parents:')
            for i in house.parents:
                print(i)
            print(f'Children:')
            for i in house.children:
                print(i)
            print('---\n')
        
class Person:
    def __init__(self, gender=None):
        self.energy = 1  # Reduces as the day go by
        self.mood = random()  # Random for each day
        self.name = choose_name()  # Just for fun
        self.age = 0
        self.gender = None
        self.extrovertiness = random()  # How probable are they to meet others
    
    def __repr__(self):
        return f'Name: {self.name} | Age: {self.age}'
        
class House:
    def __init__(self, house_num):
        self.house_num = house_num
        self.grand_parents = [Person(), Person()]
        self.parents = [Person(), Person()]
        self.children = [Person(), Person()]
        self.tot_pop = 6
        for pers in self.grand_parents:
            pers.age = randint(60, 100)
        for pers in self.parents:
            pers.age = randint(25, 60)
        for pers in self.children:
            pers.age = randint(1, 25)
    def __repr__(self):
        return f'House {self.house_num}'
            
            
if __name__ == '__main__':
    v = Village()
    v.display()
