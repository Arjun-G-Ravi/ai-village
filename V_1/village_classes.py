import heapq
import re
import json

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
        self.generation_config=genai.types.GenerationConfig(candidate_count=1, max_output_tokens=700, temperature=0.7, top_p=.9)
    
    def generate(self, inp):
        '''Generates output using Google API, given the input.'''
        try:
            response = self.model.generate_content(inp+"Answer in character in two sentences.", generation_config=self.generation_config)
        except:
            return 'Failed to fetch data from API'
        return response.text

class Person:
    def __init__(self, name, position, base_character, energy, villagers):
        self.name = name
        self.position = position
        self.base_character = base_character
        self.schedule = {} # Schedule is a dictionary of time:action
        self.relationship = {v:0.5 for v in villagers} # maybe randomise?
        self.energy = energy
        self.villagers = villagers
        self.memory = {v:'' for v in villagers} 
        
    def add_memory(self, data, person_name):
        '''This function exists so that we can readily change the data structure of self.memory in the future.'''
        self.memory[person_name] = data
    
  
class ConversationAI:
    def __init__(self):
        self.llm = LLM()

    def _perform_conversation(self):
        # Create AI that takes into accoutn of memory and character of both agents and then talk. Also call update_stats funciion().
        conv = self.llm.generate(f'''Generate a relevant conversation between {self.p1.name} and {self.p2.name} using the following details.
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
Now, generate the conversation. 

After the conversation, create a small summary of the conversation that happened between them as SUMMARY: relevant summary
Also generate a number between 0 and 1 that expresses the current relationship between both of them in the format: 
RELATIONSHIP:number''')

        return conv
    
    def _update_stats(self, person):
        # update the energy, memory and relationship of the agents.
        pass

    def _fetch_relevant_memory(self,person):
        all_memory = person.memory
        

    def create_thread_and_perform_conversation(self, p1, p2):
        # Create a thread here to do the conversation
        self.p1 = p1
        self.p2 = p2
        print(self._perform_conversation())

    
class ScheduleMaker:
    def __init__(self, person_object):
        self.person = person_object
        with open('./actions.txt','r') as f:
            self.actions = f.read().split('\n')
    
    def write_schedule(self):
        '''Adds the shedule to shedule method of the Person object'''
        writer = LLM()
        write_out = writer.generate(f'''Using the base character of the AI, memory and energy level, write the actions performed by the AI agents in a day.
                        possible actions: {self.actions}
                        base character: {self.person.base_character}
                        relevant memory: {self.person.memory}
                        Write the actions and the time of start of action in a dictionary format. The time for dictionary should start at 6 by waking up and end at around 22 by going to sleep.''' + 
                        '''
                        Format: {"Start time for activity":"Name of activity"}
                        Example: {6:"WAKE UP", 6.30: "BRUSH", 7:"EXCERCISE", 8:"DANCE", 9:"BATH", 10:"COOK", 14:"EAT", 15:"SLEEP", 17:"WAKE UP", 17.30:"READ", 19:"BATH", 20:"EAT", 21:"SLEEP"}.
                        Remember to make the time table of the agent as realistic and reasonable as possible and make sure that it follows the nature of the agent.
                        ''')
        
        data = re.search(r'\{(.*?)\}', write_out).group(1)
        final_shedule = {}
        for i in data.split(','):
            l = i.split(':')
            final_shedule[l[0].strip()] = l[1].strip()[1:-1]
        self.person.schedule = final_shedule

if __name__ == '__main__':


    # Testing conversation AI




    # Testing scheduler
    p1 = Person('Tom', (0,0), 'Tom is an introvert and a shy person who likes to talk about cows.', 1, ['Joy', 'Tim', 'John', 'Terry'])
    p2 = Person('Joy', (0,0), 'Joy is an extrovert who loves to create conversation and interact with people.', 1, ['Tom', 'Tim', 'John', 'Terry'])
    # print(p1.memory)
    conv = ConversationAI()
    conv.create_thread_and_perform_conversation(p1, p2)



    # sc = ScheduleMaker(p1)
    # sc.write_schedule()
    # print(p1.schedule)

    # Test llm text generation
    # print(llm.generate('''You are John, a twelve year old boy who thinks that he are a super cool assasin.You always talk in a shady and suspesious manner, even if there isnt one.
    #                    As he was walking home from school, he saw a cow killing the mayor of the town. The cow also gave him a scary look and threatened him that is he tell anybody of the
    #                    incident, then the cow will stomp him to death. Even the slightest clue and John is done. The cow even mooed at him. This scared the life out of John. 
    #                    John doesn't is so scared that he is willing to lie about never seeing the incident. Later, his brother asks if hehas seen anything about the murder of the mayor?
    #                    Will John tell the truth or will he lie to his brother?'''))