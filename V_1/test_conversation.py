from village_classes import Person, ConversationAI
from base_characters import base_character_dict
import random

p1 = Person('Tom',  (0,0), base_character_dict['Tom'],  1, ['Joy', 'Jane', 'John', 'Terry'])
p2 = Person('John', (0,0), base_character_dict['John'], 1, ['Tom', 'Jane', 'John', 'Terry'])
p3 = Person('Jane', (0,0), base_character_dict['Jane'], 1, ['Tom', 'Jane', 'John', 'Terry'])


print(p1)
print(p2)
print(p3)

conv = ConversationAI()
l = [p1, p2, p3]
for _ in range(3):
    p1,p2 = random.sample(l,2)

    conv.create_thread_and_perform_conversation(p1,p2)
    print()

    print(p1)
    print(p2)
    # print(p3)