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
        self.generation_config=genai.types.GenerationConfig(candidate_count=1, max_output_tokens=700, temperature=0.7, top_p=0.5)
    
    def generate(self, inp):
        try:
            response = self.model.generate_content(inp+"Answer in character in one to two sentences.", generation_config=self.generation_config)
        except:
            return 'Try Again'
        return response.text
    
    
if __name__ == '__main__':
    llm = LLM()
    print(llm.generate('''You are John, a twelve year old boy who thinks that he are a super cool assasin.You always talk in a shady and suspesious manner, even if there isnt one.
                       Mark (Johns father) asks him about the day at school. How will John answer?'''))