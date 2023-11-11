from random import choice

def choose_name():
    names = ["Ethan", "Olivia", "Liam", "Emma", "Noah", "Ava", "Sophia", "Jackson", "Aiden", "Isabella",
    "Lucas", "Mia", "Harper", "Benjamin", "Amelia", "Henry", "Evelyn", "Samuel", "Abigail", "Alexander",
    "Ella", "James", "Scarlett", "Daniel", "Grace", "Matthew", "Lily", "Jackson", "Chloe", "Sebastian",
    "Aria", "David", "Zoe", "Carter", "Penelope", "Wyatt", "Riley", "Gabriel", "Layla", "Owen", "Lillian",
    "Caleb", "Addison", "Luke", "Natalie", "Jack", "Hannah", "Ryan", "Mila", "Andrew", "Leah", "Nathan",
    "Brooklyn", "Isaac", "Zoey", "Evan", "Victoria", "Joshua", "Nora", "Nicholas", "Hazel", "Oliver", "Aurora",
    "Caleb", "Savannah", "Matthew", "Audrey", "Julian", "Bella", "Joseph", "Claire", "Dylan", "Eleanor", "Christopher",
    "Stella", "Brandon", "Lucy", "Logan", "Aaliyah", "Isaiah", "Anna", "Eli", "Peyton", "Levi", "Skylar", "Dominic",
    "Samantha", "Hunter", "Caroline", "Aaron", "Maya", "Charles", "Piper", "Adam", "Ariana", "Zachary", "Gabriella",
    "Jose", "Eliana", "Xavier", "Mason", "Emily", "Elijah", "Madison", "Logan", "Avery", "Oliver", "Sofia", "Avery", "Lucas",
    "Grace", "Evan", "Lily", "Avery", "Zachary", "Aurora", "Hudson", "Haley", "Ezra", "Nevaeh",
    "Jayden", "Paisley", "Michael", "Hannah", "William", "Natalie", "Matthew", "Ellie", "Nicholas",
    "Brooke", "Joseph", "Samantha", "Leo", "Kylie", "Isaiah", "Kaylee", "Connor", "Lyla", "Sawyer",
    "Aubrey", "Isaiah", "Claire", "Julian", "Brianna", "Levi", "Alexa", "Isaac", "Kinsley", "Anthony",
    "Alice", "Cameron", "Avery", "Gabriel", "Gabriel", "Gavin", "Sarah", "Eli", "Katherine", "Landon",
    "Alexandra", "Jaxon", "Ashley", "John", "Leilani", "Jonathan", "Eva", "Aaron", "Taylor", "Hunter",
    "Aaliyah", "Miles", "Melanie", "Cooper", "Lydia", "Jeremiah", "Peyton", "Julius", "Gianna", "Colton",
    "Luna", "Justin", "Isabel", "Dylan", "Nora", "Jordan", "Mackenzie", "Brayden", "Hailey", "Dominick",
    "Ruby", "Austin", "Kennedy", "Brody", "Jade", "Axel", "Alexis", "Easton", "Elise", "Xander"]
    return choice(names)


if __name__ == '__main__':
    print(choose_name())
