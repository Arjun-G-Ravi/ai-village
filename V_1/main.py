import village_classes
import gui

if __name__ == '__main__':
    person_list = village_classes.CreatePerson().person_list()
    objects = []
    for name in list(person_list.keys()):
        objects.append(village_classes.create_new_person(name,person_list))
    gui.Window(objects)