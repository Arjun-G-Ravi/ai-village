from queue import PriorityQueue

def h(start, end):
    return abs(end[0]-start[0]) + abs(end[1]-start[1])

def path(node, parent):
    l = [node]
    p = parent[node]
    while p is not None:
        l.append(p)
        p = parent[p]
    return tuple(l[::-1])

def pathfinder(start,end,invalid):
    open_queue = PriorityQueue()
    cost = {start : 0}
    open_queue.put((cost[start] + h(start,end), start))
    closed = set()
    open_set = {start}
    parent = {start : None}
    while not open_queue.empty():
        node = open_queue.get()[1]
        open_set.remove(node)
        if node == end:
            return path(node, parent)
        closed.add(node)
        for i in ((0,1), (0,-1), (1,0), (-1,0)):
            child = (node[0]+i[0], node[1]+i[1])
            est = h(child, end)
            if child not in closed and child not in open_set and child not in invalid:
                cost[child] = cost[node] + 1 
                open_queue.put((cost[child] + est, child))
                open_set.add(child)
                parent[child] = node
            elif child in open_set and cost[child] > cost[node] + 1:
                open_queue.queue.remove((cost[child]+est, child))
                cost[child] = cost[node] + 1
                open_queue.put((cost[child]+est, child))
                parent[child] = node
    return []

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