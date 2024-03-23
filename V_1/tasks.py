from queue import PriorityQueue

def h(start, end):
    return abs(end[0]-start[0]) + abs(end[1]-start[1])

def path(node, parent):
    l = [node]
    p = parent[node]
    while p is not None:
        l.append(p)
        p = parent[p]
    return tuple(l)

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
            if (child not in closed or child not in open_set) and child not in invalid:
                cost[child] = cost[node] + 1 
                open_queue.put((cost[child] + est, child))
                open_set.add(child)
                parent[child] = node
            elif child in open_set and cost[child] > cost[node] + 1:
                pass
    

def WALK(entity, loc):
    pass

def SLEEP(entity, loc):
    pass

def EAT:
    pass
    
def TALK:
    pass
    
def GO_TO_WORK:
    pass
    
def COME_HOME_FROM_WORK:
    pass
    
def GO_TO_MARKET:
    pass
    
def DO_SHOPPING:
    pass
    
def COME_BACK_HOME:
    pass
    
def READ:
    pass
    
def FARM:
    pass
    
def COOK:
    pass
    
def SING:
    pass
    
def DANCE:
    pass
    
def PLAY:
    pass
    
def EXCERCISE:
    pass
    
def PRAY:
    pass
    
def BRUSH:
    pass
    
def BATH:
    pass
    
def WAKE_UP:
    pass
    
def PLAY_VIDEO_GAMES:
    pass
    
def WATCH_TV:
    pass