# AI Village
A study of relationship between different AI agents in a adverserial and collaborative environment.

This is a project where the LLMs control the actions of the villagers in a village. The villagers will follow a time-table set by the LLM based on the characteristics and memory of each agent. When the agents meet, they start up a conversation. This conversation will affect the memory and behaviour of both agents. 

[![AI Village!](https://img.youtube.com/vi/aHd0qiFE9gI/maxresdefault.jpg)](https://www.youtube.com/watch?v=aHd0qiFE9gI)


## How to run
1. Create a `.env` file and add your groq api key there as:
   `api_key = 'your_api_key'`
2. If you want to add custom sprites, replace the sprites in the Sprites directory with that one. 
3. Install all requirements using `pip install requirements.txt`
4. Go to the `generated_base_characters.txt` file and change the base characters of the villages in the way you want. This will drastically affect the villager's life.
5. Now, run `python main.py`

## Contributors
This was submitted as the mini project for the college.
The team members are:
  - Advaid Arvind
  - Govind S Sarath
  - Arjun G Ravi