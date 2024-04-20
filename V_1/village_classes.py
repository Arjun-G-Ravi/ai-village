import re
import random
import threading
import ast
# We are using Gemini model by Google

class LLM:
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key='AIzaSyDA6pSGmfSJdpQw0L1Re-y8AEnm4NbCxaw') # API Key

        safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE"}]

        self.model = genai.GenerativeModel('gemini-pro', safety_settings)
        self.generation_config=genai.types.GenerationConfig(candidate_count=1, max_output_tokens=1000, temperature=0.3, top_p=.9)
    
    def generate(self, inp):
        '''Generates output using Google API, given the input.'''
        try:
            response = self.model.generate_content(inp+"Answer in character in two sentences.", generation_config=self.generation_config)
        except:
            return 'Failed to fetch data from API'
        # print(response.text)
        return response.text

class Person:
    def __init__(self, name, position, base_character, energy, villagers):
        self.name = name
        self.position = position
        self.base_character = base_character
        self.schedule = {} # Schedule is a dictionary of time:action
        self.relationship = {v:0.5 for v in villagers} # maybe randomise at the start?
        self.energy = energy
        self.villagers = villagers
        self.memory = {v:'' for v in villagers} 
        
    # def __repr__(self): # Very detailed repr
    #     return f'''Person: {self.name}
    # Base character: {self.base_character}
    # Energy: {self.energy}
    # Schedule: {self.schedule}
    # Relationship: {self.relationship}
    # Memory: {self.memory}'''

    def __repr__(self):
        return f'''Person: {self.name}
    Energy: {self.energy}
    Relationship: {self.relationship}
    Memory: {self.memory}'''
    
  
class ConversationAI:
    def __init__(self):
        self.llm = LLM()

    def create_thread_and_perform_conversation(self, p1, p2, display=False):
        self.p1 = p1
        self.p2 = p2
        thread = threading.Thread(target=self._thread_function, args=(p1, p2, display))
        thread.start()
        thread.join()

    def _thread_function(self, p1, p2, display):
        conv = self._perform_conversation()
        self._update_stats(p1, p2)
        if display: print(conv)

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
                if matches: person1.relationship[person2.name] = matches[0]
                if matches: person2.relationship[person1.name] = matches[0]

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
            self.actions.remove('TALK')
    
    def create_new_schedule(self):
        '''Adds the shedule to shedule method of the Person object'''
        writer = LLM()
        write_out = writer.generate(f'''Using the base character of the AI and memory, write the actions performed by the AI agents in a day.
                        possible actions: {self.actions}
                        base character: {self.person.base_character}
                        relevant memory: {self.person.memory}
                        Write the actions and the time of start of action in a dictionary format. The time for dictionary should start at 6:00 by waking up and end at around 22:00 by going to sleep.''' + 
                        '''
                        Format: {"Start time for activity":"Name of activity"}
                        Example: {"6:00":"WAKE UP", "6:30":"BRUSH", "7:00":"EXCERCISE", "8:00":"DANCE", "9:00":"BATH", "10:00":"COOK", "14:30":"EAT", "15:00":"SLEEP", "17:00":"WAKE UP", "17.30":"READ", "19:00":"BATH", "20:00":"EAT", "21:00":"SLEEP"}.
                        Remember to make the time table of the agent as realistic and reasonable as possible and make sure that it follows the nature of the agent. Also ensure that the actions are the actions given in the prompt.
                        ''')
        
        # data = re.search(r'\{(.*?)\}', write_out).group(1)
        # print(data)
        pattern = r'\{(.*?)\}'
        data = '{' +re.findall(pattern, write_out)[0] + '}'
        final_shedule = ast.literal_eval(data)
        self.person.schedule = final_shedule

    def change_schedule(self, reason):
        '''Changes the schedule of a person, because of another person's intervention(the summary will be given in as reason.)'''
        writer = LLM()
        write_out = writer.generate(f'''Using the base character of the AI, memory and factor that affect schedule, write the actions performed by the AI agents for a day.
                        previous schedule: {self.person.schedule}
                        Factor that affect schedule: {reason}
                        possible action pool: {self.actions}
                        Change the schedule with the help of the above factor. Ensure that all the actions in the schedule comes from the given action pool. If the agent is meeting to somebody at any place, the agent have to first reach that place and then perform the action MEET half an hour later.''' + 
                        '''
                        Format: {"Start time for activity":"Name of activity"}
                        Example: {"6:00":"WAKE UP", "6:30":"BRUSH", "7:00":"EXCERCISE", "8:00":"DANCE", "9:00":"BATH", "10:00":"COOK", "14:30":"EAT", "15:00":"SLEEP", "17:00":"WAKE UP", "17.30":"READ", "19:00":"BATH", "20:00":"EAT", "21:00":"SLEEP"}.
                        Now carefully modify the schedule.''')
        pattern = r'\{(.*?)\}'
        data = '{' +re.findall(pattern, write_out)[0] + '}'
        final_shedule = ast.literal_eval(data)
        
        self.person.schedule = final_shedule


if __name__ == '__main__':

    # # Testing conversation AI
    p1 = Person('Tom', (0,0), 'Tom is an introvert and a shy person who likes to talk about cows.', 1, ['Joy', 'Tim', 'John', 'Terry'])
    # p2 = Person('Joy', (0,0), 'Joy is an extrovert who loves to create conversation and interact with people.', 1, ['Tom', 'Tim', 'John', 'Terry'])
    # print(p1)
    # conv = ConversationAI()
    # conv.create_thread_and_perform_conversation(p1, p2)
    # print(p1)

    # Testing scheduler
    sc = ScheduleMaker(p1)
    sc.change_schedule('Tom and Jane decided to meet in the market at time 15.')
    print(p1.schedule)
    print()
    sc.create_new_schedule() 
    print(p1.schedule)

    # Test llm text generation
    # print(llm.generate('''You are John, a twelve year old boy who thinks that he are a super cool assasin.You always talk in a shady and suspesious manner, even if there isnt one.
    #                    As he was walking home from school, he saw a cow killing the mayor of the town. The cow also gave him a scary look and threatened him that is he tell anybody of the
    #                    incident, then the cow will stomp him to death. Even the slightest clue and John is done. The cow even mooed at him. This scared the life out of John. 
    #                    John doesn't is so scared that he is willing to lie about never seeing the incident. Later, his brother asks if hehas seen anything about the murder of the mayor?
    #                    Will John tell the truth or will he lie to his brother?'''))
