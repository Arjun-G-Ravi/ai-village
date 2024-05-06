import re
import random
import threading
import ast
from groq import Groq
from Person import Person

class AI_agents():
    '''This class is a abstraction of all other classes. This is the only class to be used on other parts. '''
    def __init__(self):
        pass

    def conversation(self, p1, p2, display=False):
        conv = ConversationAI()
        if not display: conv.create_thread_and_perform_conversation(p1, p2)
        else: conv.create_thread_and_perform_conversation(p1, p2, display=True)

    def create_schedule(self, p):
        sc = ScheduleMaker(p)
        sc.create_new_schedule()

    def change_schedule(self, p, reason):
        sc = ScheduleMaker(p)
        sc.change_schedule(reason)



class CreatePerson:
    '''Uses AI to create the character and behaviour of a person.'''
    def __init__(self, ):
        self.llm = LLM(temperature=0.5)

    def write_new_character(self, name, character = False):
        if character: out = self.llm.generate(f'''Write 5 character of a person called {name} as words or phrases separated by comma. 
The character should follow these behaviours {character}. Also ensure that the text should be output in the following format:
<Name>: < 5 characters>. 
Dont answer anything else.''')
            
        else: out = self.llm.generate(f'''Write 5 character of a person called {name} as words or phrases separated by comma. 
Also ensure that the text should be output in the following format:
<Name>: < 5 characters>. 
Dont answer anything else.''')
        
        with open('generated_base_characters.txt', 'a') as f:
            f.write(out + '|\n')

    def clear(self):
        with open('generated_base_characters.txt', 'w') as f:
            f.write('')

    def person_list(self):
        with open('generated_base_characters.txt', 'r') as f:
            person_list = f.read().split('|\n')
        persons = {}
        for person in person_list:
            if person:
                new = person.split(':')
                persons[new[0]] = new[1]
        return persons

# Global functions

def create_new_person(name, char_dict):
    return Person(name, char_dict[name], {k:'' for k,v in char_dict.items()})


# ---------------------

class LLM:
    def __init__(self, temperature = 0.2, top_p=0.3):
        self.temperature = temperature
        self.top_p = top_p
        self.client = Groq(api_key='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')

    def generate(self, inp):
        '''Generates output using Google API, given the input.'''
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user","content": f"{inp}"}],
            model="llama3-8b-8192",
            # All models: llama3-8b-8192 llama3-70b-8192 gemma-7b-it mixtral-8x7b-32768
            temperature = self.temperature,
            top_p=self.top_p)

        return chat_completion.choices[0].message.content


  
class ConversationAI:
    def __init__(self):
        self.llm = LLM(temperature = 0.3)

    def create_thread_and_perform_conversation(self, p1, p2, display=False):
        self.p1 = p1
        self.p2 = p2
        thread = threading.Thread(target=self._thread_function, args=(p1, p2, display))
        thread.start()
        thread.join()

    def _thread_function(self, p1, p2, display):
        self.p1.is_in_conversation = True
        self.p2.is_in_conversation = True
        conv = self._perform_conversation()
        self._update_stats(p1, p2)
        if display: print(conv)
        self.p1.is_in_conversation = False
        self.p2.is_in_conversation = False

    def _perform_conversation(self):
        self.conv = self.llm.generate(f'''Generate a relevant conversation between {self.p1.name} and {self.p2.name} using the following details.
{self.p1.name} has the base character: {self.p1.base_character}.
Relevant memory of {self.p1.name}: {self.p1.memory}.

{self.p2.name} has the base character: {self.p2.base_character}.
Relevant memory of {self.p2.name}: {self.p2.memory}.

Relationship between  {self.p2.name} and {self.p2.name}: {self.p2.relationship[self.p1.name]}. Here closer to 0 indicates bad relation and hatred. 1 means really good friends.
Example Format:
<CONV BEGINS>
{self.p1.name}: Conversation relevent to memory, base charater and relationship with {self.p2.name}
{self.p2.name}: Conversation relevent to memory, base charater and relationship with {self.p1.name}
{self.p1.name}: Conversation relevent to memory, base charater and relationship with {self.p2.name}
{self.p2.name}: Conversation relevent to memory, base charater and relationship with {self.p1.name}
<CONV ENDS>
Now, generate the conversation in the above format only. Use the memory to create a flow of conversations. 

After the conversation, create a small summary of the conversation that happened between them as SUMMARY: relevant summary
Also generate a number between 0 and 1 that expresses the current relationship between both of them in the format: 
RELATIONSHIP:number.(Write only the number. Don't add any text here)''')
        return self.conv
    
    def _update_stats(self, person1, person2):
        # update the energy, memory and relationship of the agents.
        conv_list = self.conv.split('\n')
        for conversation in conv_list:
            if 'SUMMARY:' in conversation or 'SUMMARY :' in conversation:
                person1.memory[person2.name] += conversation[9: ]
                person2.memory[person1.name] += conversation[9: ]
            if 'RELATIONSHIP:' or 'RELATIONSHIP :' in conversation:
                matches = re.findall(r'\b0\.\d+\b', conversation)
                if matches: person1.relationship[person2.name] = float(matches[0])
                if matches: person2.relationship[person1.name] = float(matches[0])

        person1.energy -= random.randint(1,3)*0.1
        person1.energy = round(person1.energy, 1)
        if person1.energy < 0: person1.energy = 0

        person2.energy -= round(random.randint(1,3)*0.1, 1)
        person2.energy = round(person2.energy, 1)
        if person2.energy < 0: person2.energy = 0

        

class ScheduleMaker:
    def __init__(self, person_object):
        self.person = person_object
        with open('./actions.txt','r') as f:
            self.actions = f.read().split('\n')
    
    def clean_wrong_schedule(self, schedule):
        to_remove = []
        for t,a in schedule.items():
                if a not in self.actions:
                        print('WRONG ACTIONS:', a)
                        if 'LUNCH' in a or 'FOOD' in a or 'EAT' in a or 'BREAKFAST' in a or 'DINNER' in a: schedule[t] = 'EAT'
                        elif 'SHOWER' in a: schedule[t] = 'BATH'
                        else: to_remove.append(t)
        for i in to_remove: schedule.pop(i)
        return schedule
    
    def create_new_schedule(self):
        '''Adds the shedule to shedule method of the Person object'''
        writer = LLM(temperature=0, top_p=.1)
        write_out = writer.generate(f'''You are modified to act as a LLM that creates the schedule for AI agents to work in a simluated environment.
                        Using following details, craft the schedule to be followed by the agent during a day.
                        Available actions: {self.actions}
                        Base character: {self.person.base_character}
                        Relevant memory: {self.person.memory}
                        Write the actions and the time of start of action in a dictionary format. The time for dictionary can start at anywhere between 5:00 and 9:00 by the action "WAKE UP" and end between 20:00 and 22:00 by the action "SLEEP".''' + 
                        '''
                        Format: {"Start time for activity":"Name of activity"}
                        Example: {"6:00":"WAKE UP", "7:00":"EXCERCISE", "9:00":"BATH", "10:00":"COOK", "14:00":"EAT", "15:00":"WATCH TV", "17:00":"GO TO MARKET", "19:30":"COME BACK HOME", "20:00":"EAT", "21:00":"SLEEP"}.
                        The time block should ideally be a integer time or integer-and half time. MAKE SURE THAT ALL THE ACTIONS ARE GENERATED FROM THE AVAILABLE ACTIONS. Now generate schedule: 
                        ''')
        pattern = r'\{(.*?)\}'
        data = '{' +re.findall(pattern, write_out)[0] + '}'
        final_schedule = ast.literal_eval(data) # returns the string as a python expression
        final_schedule = self.clean_wrong_schedule(final_schedule)
        self.person.schedule = final_schedule

    def change_schedule(self, reason):
        '''Changes the schedule of a person, because of another person's intervention(the summary will be given in as reason.)'''
        writer = LLM(temperature=0.1, top_p=.1)
        write_out = writer.generate(f'''You are modified to act as a LLM that creates the schedule for AI agents to work in a simluated environment.
                        Using following details, craft the schedule to be followed by the agent during a day.
                        Possible actions: {self.actions}
                        previous schedule: {self.person.schedule}
                        Factor that affect schedule: {reason}
                        Modify the previous schedule for the AI agent by consider the reason. The time for dictionary can start at anywhere between 5:00 and 9:00 by the action "WAKE UP" and end between 20:00 and 22:00 by the action "SLEEP".''' + 
                        '''
                        Format: {"Start time for activity":"Name of activity"}
                        Example: {"5:00":"WAKE UP", "5:30":"BATH", "6:00":"WATCH TV", "9:00":"GO TO MARKET", "17:00":"COME BACK HOME", "17:30":"PLAY VIDEO GAMES", "20:00":"EAT", "21:00":"SLEEP"}.
                        If the agent is meeting to somebody at any place, the agent have to first reach that place using action like "GO TO MARKET" (takes an hour) and then perform the action MEET for atleast an hour. 
                        The time block should ideally be a integer time or integer-and half time. MAKE SURE THAT ALL THE ACTIONS ARE GENERATED FROM THE AVAILABLE ACTIONS. Do not return anything else to destroy the format of the new schedule.
                        Now generate the modified schdule:
                        ''')



        # write_out = writer.generate(f'''Using the base character of the AI, memory and factor that affect schedule, write the actions performed by the AI agents for a day.
        #                 previous schedule: {self.person.schedule}
        #                 Factor that affect schedule: {reason}
        #                 possible action pool: {self.actions}
        #                 Change the schedule with the help of the above factor. Ensure that all the actions in the schedule comes from the given action pool. The time block should ideally be a integer time or integer-and half time.
        #                 If the agent is meeting to somebody at any place, the agent have to first reach that place(takes an hour) and then perform the action MEET for atleast an hour. Dont put any other actions there.''' + 
        #                 '''
        #                 Format: {"Start time for activity":"Name of activity"}
        #                 Example: {"6:00":"WAKE UP", "6:30":"BRUSH", "7:00":"EXCERCISE", "8:00":"DANCE", "9:00":"BATH", "10:00":"COOK", "14:30":"EAT", "15:00":"SLEEP", "17:00":"WAKE UP", "17.30":"READ", "19:00":"BATH", "20:00":"EAT", "21:00":"SLEEP"}.
        #                 Do not add any unnecessary data or ACTIONS to the schedule and carefully modify the schedule.''')
        pattern = r'\{(.*?)\}'
        data = '{' +re.findall(pattern, write_out)[0] + '}'
        final_schedule = ast.literal_eval(data) # returns the string as a python expression
        final_schedule = self.clean_wrong_schedule(final_schedule)
        self.person.schedule = final_schedule

 

if __name__ == '__main__':

    # Test creating character behaviour by AI
    P =CreatePerson()
    P.clear()
    P.write_new_character('John', 'super funny and extrovert')
    P.write_new_character('Terry', 'introvert who loves marvel movies')
    # P.write_new_character('Tom', 'lazy')
    # P.write_new_character('Lynn', 'super strong and atlethic')
    # P.write_new_character('Tim', 'loves cows')
    char_dict = P.person_list()

    p1 = create_new_person('John', char_dict)
    p2 = create_new_person('Terry', char_dict)

    ai = AI_agents()

    # Testing conversation
    print('-'*20)
    print(p1)
    ai.conversation(p1,p2, display=True)
    print(p1)

    # Testing create_schedule
    print('-'*20)
    ai.create_schedule(p1)
    print(p1.schedule)

    # Testing update_schedule
    print('-'*20)
    ai.change_schedule(p1, 'Tom decided to meet with Janet at 15:00 in the market.')
    print(p1.schedule)











    #################### OLD TESTS ############################

    # Testing conversation AI
    # print(p1)
    # conv = ConversationAI()
    # conv.create_thread_and_perform_conversation(p1, p2, display=True)
    # print(p1)

    # Testing scheduler and schedule changer AI
    # sc = ScheduleMaker(p1)
    # sc.create_new_schedule() 
    # print(p1.schedule)
    # print()
    # sc.change_schedule('Tom is low on energy and want to sleep at 16:00.')
    # print(p1.schedule)


    # # Test llm text generation
    # llm = LLM(temperature=1)
    # print(llm.generate('''You are John, a twelve year old boy who thinks that he are a super cool assasin.You always talk in a shady and suspesious manner, even if there isnt one.
    #                    As he was walking home from school, he saw a cow killing the mayor of the town. The cow also gave him a scary look and threatened him that is he tell anybody of the
    #                    incident, then the cow will stomp him to death. Even the slightest clue and John is done. The cow even mooed at him. This scared the life out of John. 
    #                    John doesn't is so scared that he is willing to lie about never seeing the incident. Later, his brother asks if hehas seen anything about the murder of the mayor?
    #                    Will John tell the truth or will he lie to his brother?'''))
    # print()
    # llm = LLM(temperature=0)
    # print(llm.generate('''You are John, a twelve year old boy who thinks that he are a super cool assasin.You always talk in a shady and suspesious manner, even if there isnt one.
    #                    As he was walking home from school, he saw a cow killing the mayor of the town. The cow also gave him a scary look and threatened him that is he tell anybody of the
    #                    incident, then the cow will stomp him to death. Even the slightest clue and John is done. The cow even mooed at him. This scared the life out of John. 
    #                    John doesn't is so scared that he is willing to lie about never seeing the incident. Later, his brother asks if hehas seen anything about the murder of the mayor?
    #                    Will John tell the truth or will he lie to his brother?'''))
    print('Completed.')