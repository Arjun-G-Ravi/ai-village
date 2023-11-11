from names import choose_name
from random import choice, randint, random
from time import time, sleep
import os

class Village:
    def __init__(self):
        self.energy = 0
        self.num_houses = 3
        self.houses = [House(i+1) for i in range(self.num_houses)]
        self.people = [h.people for h in self.houses]
        self.tot_people = []
        for p in self.people:
            self.tot_people.extend(p)
        self.village_pop = len(self.tot_people)

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
            
    def update_time(self, t):  # Updates the general energy level of the village
        if t<7:  # early morning
            self.energy = 0.1
        elif t<17:
            self.energy = 1
        elif t<20:
            self.energy = 0.5
        else:
            self.energy = 0.2
            
            
        
class Person:
    def __init__(self, gender=None):
        # self.energy = 1  # Reduces as the day go by
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
        self.people = self.children + self.parents + self.grand_parents
        # print(self.people)
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
