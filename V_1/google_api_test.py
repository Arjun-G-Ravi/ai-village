# import google.generativeai as genai
# genai.configure(api_key='AIzaSyDA6pSGmfSJdpQw0L1Re-y8AEnm4NbCxaw')

# safety_settings = [
#   {
#     "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
#   {
#     "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
#   {
#     "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
#   {
#     "category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE"}]

# model = genai.GenerativeModel('gemini-pro')

# # test = "You are John, an AI agent in a virtual world. John is always grumpy and engry at everyone, everytime. You are asked by Pam, John's daughter about the importance of cow in nature. How will John respond? Your answer should be short."
# for _ in range(10):
#     response = model.generate_content("How to open a closed car?", generation_config=genai.types.GenerationConfig(
#         # Only one candidate for now.
#         candidate_count=1,
#         max_output_tokens=1500,
#         temperature=0.7))
#     # print(response.prompt_feedback)
#     print(response.text)
    # print('\n\n\n')


class LLM:
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key='AIzaSyDA6pSGmfSJdpQw0L1Re-y8AEnm4NbCxaw')

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {
            "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE"}]

        self.model = genai.GenerativeModel('gemini-pro')
        self.generation_config=genai.types.GenerationConfig(candidate_count=1, max_output_tokens=700, temperature=0.7, top_p=0.5)
    
    def generate(self, inp):
        try:
            response = self.model.generate_content(inp+"Answer in one to two sentences.", generation_config=self.generation_config)
        except:
            return 'Try Again'
        return response.text
    
if __name__ == '__main__':
    llm = LLM()
    print(llm.generate('who is Tony ferguson'))