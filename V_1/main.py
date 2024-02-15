class Person:
    def __init__(self, name, position, base_character, memory, relationship, energy):
        self.name = name
        self.position = position
        self.base_character = base_character
        self.memory = memory
        self.relationship = relationship
        self.energy = energy
        
    def add_memory(self, mem, importance):
        import heapq
        # if importance>1: importance=1
        # if importance<0: importance=0
        
        heapq.heappush(self.memory.data, [-importance, mem]) # minus changes default min heap to max heap
        # should do something to give more importance to recent information
    
    def read_memory(self, n=3):
        # should write a function to fetch relevant information, given a situation (grep should work?????????)
        ''' reads top 'n' important memories'''
        out = []
        for i in range(n):
            out.append(self.memory.data[i])
        return out
        
class Memory:
    def __init__(self):
        self.data = []
    
        




if __name__ == '__main__':
    tom_character = 'Tom is always angry at everyone. He works at the mart.'
    tom_memory = Memory()
    p1 = Person('Tom', (0,0), tom_character, tom_memory, [i for i in range(10)])
    
        
