def WALK(entity, loc, invalid):
    path = pathfinder((entity.X,entity.Y),loc, invalid)

def SLEEP():
    #get location of bed and go to that location
    #sleep in bed
    pass

def EAT():
    #go to dining table
    #eat food
    pass
    
def TALK():
    #need to discuss
    pass
    
def GO_TO_WORK():
    #get location of work place and go to that location
    #do work
    pass
    
def COME_HOME_FROM_WORK():
    #get location of home and go to that location
    pass
    
def GO_TO_MARKET():
    #get location of market and go to that location
    pass
    
def DO_SHOPPING():
    #get location of stall and go to that location
    #shop items
    pass
    
def COME_BACK_HOME():
    #get location of home and go to that location
    pass
    
def READ():
    #get location of bookshelf and go to that location
    #read book
    pass
    
def FARM():
    #get location of farmland and go to that location
    #do farming
    pass
    
def COOK():
    #get location of kitchen and go to that location
    #do cooking
    pass
    
def SING():
    #start singing
    pass
    
def DANCE():
    #start dancing
    pass
    
def PLAY():
    #need to discuss
    pass
    
def EXCERCISE():
    #get location of park and go to that location
    #do excercise
    pass
    
def PRAY():
    #get location of pray area and go to that location
    #pray
    pass
    
def BRUSH():
    #get location of bathroom and go to that location
    #brush teeth
    pass
    
def BATH():
    #get location of bathroom and go to that location
    #bathe
    pass
    
def WAKE_UP():
    #wake up from sleep
    pass
    
def PLAY_VIDEO_GAMES():
    #get location of tv and go to that location
    #play games
    pass
    
def WATCH_TV():
    #get location of tv and go to that location
    #watch tv
    pass

TRANSITION = {
    "WALK" : WALK,
    "EAT" : EAT,
}