import heapq
import re
import json

# We are using Gemini model by Google

class LLM:
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key='AIzaSyDA6pSGmfSJdpQw0L1Re-y8AEnm4NbCxaw')

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
    def __init__(self, name, position, base_character, memory, relationship, energy):
        self.name = name
        self.position = position
        self.base_character = base_character
        self.memory = memory
        self.relationship = relationship
        self.energy = energy
        self.schedule = {}
        
    def add_memory(self, data, importance):
        if importance>1: importance=1
        if importance<0: importance=0
        heapq.heappush(self.memory.data, [-importance, data]) # minus changes default min heap to max heap
        # should do something to give more importance to recent information
    
    def read_memory(self, n=3):
        # should write a function to fetch relevant information, given a situation (cosine similarity kinda stuff)
        ''' reads top 'n' important memories'''
        out = []
        for i in range(n):
            out.append(self.memory.data[i])
        return out
  
class ConversationAI:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def _perform_conversation():
        # Create AI that takes into accoutn of memory and character of both agents and then talk. Also call update_stats funciion().
        pass

    def _update_stats(person):
        # update the energy, memory and relationship of the agents.
        pass

    def create_thread_and_perform_conversation():
        pass

    
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
    pass
    # Testing conversation AI




    # Testing scheduler
    # p1 = Person('Tom', (0,0), 'loves singing and dancing', 'have to go to work at 9 ', [1], 1)
    # sc = ScheduleMaker(p1)
    # sc.write_schedule()
    # print(p1.schedule)

    # Test llm text generation
    # print(llm.generate('''You are John, a twelve year old boy who thinks that he are a super cool assasin.You always talk in a shady and suspesious manner, even if there isnt one.
    #                    As he was walking home from school, he saw a cow killing the mayor of the town. The cow also gave him a scary look and threatened him that is he tell anybody of the
    #                    incident, then the cow will stomp him to death. Even the slightest clue and John is done. The cow even mooed at him. This scared the life out of John. 
    #                    John doesn't is so scared that he is willing to lie about never seeing the incident. Later, his brother asks if hehas seen anything about the murder of the mayor?
    #                    Will John tell the truth or will he lie to his brother?'''))