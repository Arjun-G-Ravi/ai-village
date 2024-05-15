import random
import village_classes
import gui


person_list = village_classes.CreatePerson().person_list()
objects = []
print(person_list)

for name in list(person_list.keys()):
    print(name)

    objects.append(village_classes.create_new_person(name,person_list))
print(objects)
print('-' *40)

conv = village_classes.ConversationAI()
for _ in range(10):
    p1,p2 = random.sample(objects,2)

    conv.create_thread_and_perform_conversation(p1,p2, display=False)

    print()

    print(p1)
    print(p2)
    print('-' *40)
    # print(p3)