class Person:
    def __init__(self, name, base_character, villagers,energy = 1, position = (0,0)):
        self.name = name
        self.position = position
        self.base_character = base_character
        self.schedule = {} # Schedule is a dictionary of time:action
        self.relationship = {v:0.5 for v in villagers} 
        self.energy = energy
        self.villagers = villagers
        self.memory = {v:'' for v in villagers} 
        self.is_in_conversation = False

    def __repr__(self):
        return f'''Person: {self.name}
    Energy: {self.energy}
    Relationship: {self.relationship}
    Memory: {self.memory}'''