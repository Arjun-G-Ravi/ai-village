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
        self.generation_config=genai.types.GenerationConfig(candidate_count=1, max_output_tokens=700, temperature=0.9, top_p=.9)
    
    def generate(self, inp):
        try:
            response = self.model.generate_content(inp+"Answer in character in two sentences.", generation_config=self.generation_config)
        except:
            return 'Try Again'
        return response.text

class Person:
    def __init__(self, name, position, base_character, memory, relationship, energy):
        self.name = name
        self.position = position
        self.base_character = base_character
        self.memory = memory
        self.relationship = relationship
        self.energy = energy
        self.schedule = [] # queue
        
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

class ScheduleMaker:
    def __init__(self, person_object):
        self.person = person_object
        with open('./actions.txt','r') as f:
            self.actions = f.read().split('\n')
        # print(self.actions)
    
    def write_schedule(self):
        writer = LLM()
        write_out = writer.generate(f'''Using the base character of the AI, memory and energy level, write the continuation of the actions.
                        possible actions: {self.actions}
                        base character: {self.person.base_character}
                        ''')
        
        print(write_out)


        # choices = 



if __name__ == '__main__':
    p1 = Person('Tom', (0,0), 'Shy', 'Forgot to shower today', [0], 1)
    sc = ScheduleMaker(p1)
    sc.write_schedule()

    # print(llm.generate('''You are John, a twelve year old boy who thinks that he are a super cool assasin.You always talk in a shady and suspesious manner, even if there isnt one.
    #                    As he was walking home from school, he saw a cow killing the mayor of the town. The cow also gave him a scary look and threatened him that is he tell anybody of the
    #                    incident, then the cow will stomp him to death. Even the slightest clue and John is done. The cow even mooed at him. This scared the life out of John. 
    #                    John doesn't is so scared that he is willing to lie about never seeing the incident. Later, his brother asks if hehas seen anything about the murder of the mayor?
    #                    Will John tell the truth or will he lie to his brother?'''))