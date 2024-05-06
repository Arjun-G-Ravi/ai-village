import pygame
import random
from village_classes import AI_agents
from queue import PriorityQueue

pygame.init()

class SchedulePlaceholder:
    name = ""
    schedule = {}

def h(start, end, occupied):
    l = []
    for i in end:
        #print(i,occupied)
        if i not in occupied:
            l.append(abs(i[0]-start[0]) + abs(i[1]-start[1]))
    return min(l)

def path(node, parent):
    l = [node]
    p = parent[node]
    while p is not None:
        l.append(p)
        p = parent[p]
    l.pop()
    return l

def pathfinder(start,end,world):
    open_queue = PriorityQueue()
    cost = {start : 0}
    open_queue.put((cost[start] + h(start,end,tuple(world.OCCUPIED)), start))
    closed = set()
    open_set = {start}
    parent = {start : None}
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.Surface((16,16))
    sprite.image.fill("black")
    while not open_queue.empty():
        node = open_queue.get()[1]
        open_set.remove(node)
        if node in end:
            world.OCCUPIED.append(node)
            return path(node, parent)
        closed.add(node)
        for i in ((0,1), (0,-1), (1,0), (-1,0)):
            child = (node[0]+i[0], node[1]+i[1])
            est = h(child, end, tuple(world.OCCUPIED))
            sprite.rect = sprite.image.get_rect(topleft = (child[0]*16,child[1]*16))
            sprite.mask = pygame.mask.from_surface(sprite.image)
            if child not in closed and child not in open_set and child not in world.OCCUPIED and not world.check_collision(sprite):
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

class Window:
    #game attributes
    DRAGGING = False
    #time attributes
    DT = 1
    TIMER = 150
    global AI
    #initialise AI
    AI = AI_agents()
    
    def __init__(self,person_list):
        #display info
        self.DISPLAY_INFO = pygame.display.Info()
        #create window with fullscreen
        self.SCREEN = pygame.display.set_mode((self.DISPLAY_INFO.current_w,self.DISPLAY_INFO.current_h),pygame.NOFRAME)
        pygame.display.set_caption("AI VILLAGE")
        #create pygame clock
        self.CLOCK = pygame.time.Clock()
        #take window width and height
        self.WINDOW_WIDTH,self.WINDOW_HEIGHT = pygame.display.get_window_size()
        #instantiate the world
        self.WORLD = World(person_list)
        self.FONT = pygame.font.SysFont("calibri", 16)
        #start the event loop
        self.event_loop()

    def event_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                #click and drag
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #currently dragging the screen
                    self.DRAGGING = True
                    #calculate the offset of coordinates moved by the mouse when dragging
                    mouse_pos = event.pos
                    x_offset = self.WORLD.X - mouse_pos[0]
                    y_offset = self.WORLD.Y - mouse_pos[1]
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    #currently not dragging the screen
                    self.DRAGGING = False
                #zoom the world
                elif event.type == pygame.MOUSEMOTION:
                    if self.DRAGGING:
                        #calculation of world coordinates after dragging
                        pos = event.pos
                        x = pos[0] + x_offset
                        y = pos[1] + y_offset
                        #updating world coordinates
                        self.WORLD.set_x(max(min(0,x),-self.WORLD.WIDTH * self.WORLD.CELL_SIZE * self.WORLD.SCALE + self.WINDOW_WIDTH))
                        self.WORLD.set_y(max(min(0,y),-self.WORLD.HEIGHT * self.WORLD.CELL_SIZE * self.WORLD.SCALE + self.WINDOW_HEIGHT))
                elif event.type == pygame.MOUSEWHEEL:
                    #calculation of new world scale
                    scale = min(max(1,self.WORLD.SCALE + event.precise_y),4)
                    #calculation for new world coordinates
                    x,y = pygame.mouse.get_pos()
                    posx = ((x - self.WORLD.X)//self.WORLD.SCALE)*scale - x
                    posy = ((y - self.WORLD.Y)//self.WORLD.SCALE)*scale - y
                    #updating world coordinates and world scale
                    self.WORLD.set_x(max(min(-posx,0),-self.WORLD.WIDTH * self.WORLD.CELL_SIZE * scale + self.WINDOW_WIDTH))
                    self.WORLD.set_y(max(min(-posy,0),-self.WORLD.HEIGHT * self.WORLD.CELL_SIZE * scale + self.WINDOW_HEIGHT))
                    self.WORLD.set_scale(scale)
                    self.WORLD.scale_entities(scale)
            
            #game updates
            self.update()
            #game rendering
            self.render()
            #clock tick
            self.DT = self.CLOCK.tick(30)/1000
            self.TIMER += self.DT

    def update(self):
        if self.WORLD.TIME != (self.TIMER//15)%self.WORLD.MAX_TIME:
            self.WORLD.TIME = (self.TIMER//15)%self.WORLD.MAX_TIME
        self.WORLD.update(self.DT)
    
    def render(self):
        #render events
        self.SCREEN.fill("gray")
        self.WORLD.draw(self.SCREEN)
        
        time = self.WORLD.get_time()
        text = self.FONT.render(time, True, (255,255,255))
        text_surf = text.copy()
        text_surf.fill((0,0,0))
        self.SCREEN.blit(text_surf, (0,0))
        self.SCREEN.blit(text, (0,0))
        
        pygame.display.flip()

class World:
    #world attributes
    SCALE = 1
    MAX_SCALE = 4
    X = 0
    Y = 0
    WIDTH = 200
    HEIGHT = 100
    CELL_SIZE = 16
    #texture for the world
    TEXTURE = None
    SCALED_TEXTURE = None
    #entities in the world
    ENTITIES = []
    OCCUPIED = []
    TASK_PRIORITY = {
        "SLEEP" : 1,
        "WAKE UP" : 1,
        "EAT" : 0.8,
        "EXCERCISE" : 0.4,
        "GO TO WORK" : 0.6,
        "GO TO MARKET" : 0.4,
        "COME BACK HOME" : 0.6,
        "READ" : 0.4,
        "COOK" : 0.4,
        "WATCH TV" : 0.4,
        "PLAY VIDEO GAMES" : 0.4,
        "BATH" : 0.6,
        "WAIT" : 0.2,
        "IDLE" : 0,
        "MEET" : 1
        }
    #Time attributes
    TIME = 10
    MAX_TIME = 48         # 24 * 2 (30 minute intervals)
    DARKNESS = 150
    #important locations
    LOCATIONS = {
        "House1" : {
            "Kitchen" : ((31, 11),(30,11),(36,11),(33,11),(34,11)),
            "Kitchen_Seat" : ((34,12),(34,13)),
            "Bath" : ((25,11),),
            "Toilet" : ((27, 11),),
            "Bed" : ((17, 11),(17,18)),
            "TV" : ((36, 20),(35, 20)),
            "Bookshelf" : ((28, 19),),
            "Seat" : ((34, 24),(31,24)),
            "Seat_Dir" : {(34, 24):"S",(31,24):"S",(34,12):"E",(34,13):"E",(36, 20):"N",(35, 20):"N"},
            "Corner" : ((39,30),(39,8),(12,8),(12,30))
        },
        "House2" : {
            "Kitchen" : ((34, 61),(33,61),(39,61),(36,61),(37,61)),
            "Kitchen_Seat" : ((37,62),(37,63)),
            "Bath" : ((28,61),),
            "Toilet" : ((30, 61),),
            "Bed" : ((20, 61),(20,68)),
            "TV" : ((38, 70),(39, 70)),
            "Bookshelf" : ((31, 69),),
            "Seat" : ((34, 74),(39,70)),
            "Seat_Dir" : {(34, 74):"S",(39,70):"S",(37,62):"E",(37,63):"E",(38, 70):"N",(39, 70):"N"},
            "Corner" : ((42,80),(42,58),(15,58),(15,80))
        },
        "House3" : {
            "Kitchen" : ((165, 17),(164,17),(170,17),(167,17),(168,17)),
            "Kitchen_Seat" : ((168,18),(168,19)),
            "Bath" : ((159,17),),
            "Toilet" : ((161, 17),),
            "Bed" : ((151, 17),(151,24)),
            "TV" : ((169, 26),(170, 26)),
            "Bookshelf" : ((162, 25),),
            "Seat" : ((165,30),(168,30)),
            "Seat_Dir" : {(165, 30):"S",(168,30):"S",(168,18):"E",(168,19):"E",(169, 26):"N",(170, 26):"N"},
            "Corner" : ((173,36),(173,16),(146,16),(146,36))
        },
        "House4" : {
            "Kitchen" : ((162, 68),(161,68),(167,68),(164,68),(165,65)),
            "Kitchen_Seat" : ((165,69),(165,70)),
            "Bath" : ((156,68),),
            "Toilet" : ((158, 68),),
            "Bed" : ((148, 68),(148,75)),
            "TV" : ((166, 77),(167, 77)),
            "Bookshelf" : ((159, 76),),
            "Seat" : ((162,81),(165,81)),
            "Seat_Dir" : {(162, 81):"S",(165,81):"S",(165,69):"E",(165,70):"E",(166, 77):"N",(167, 77):"N"}
        },
        "Market" : {
            "Cart" : ((79,63),(105,63)),
            "Items" : ((84,58),(87,54),(85,53),(85,55),(87,51),(89,51),(91,51),(93,51),
                (96,51),(98,51),(92,54),(90,53),(95,53),(95,54),(100,55),(101,51)),
            "Seat" : ((97,57),(101,57)),
            "Counter" : ((95,57),(99,57))
        }
    }
    
    def __init__(self,person_list):
        self.set_texture()
        self.TIME = 10
        
        #sprite mask
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load(r'./Sprites/World_Mask.png').convert_alpha()
        sprite.rect = sprite.image.get_rect(topleft = (self.X,self.Y))
        sprite.mask = pygame.mask.from_surface(sprite.image)
        self.SPRITE_GROUP = pygame.sprite.GroupSingle(sprite)
        self.SKY = pygame.Surface((2000,1500),pygame.SRCALPHA)
        self.SKY.fill((0,0,0,self.DARKNESS))
        
        #create list of entities in the environment
        self.init_entities(person_list)
    
    def init_entities(self, person_list):
        #create the entities in the world
        '''
        schedule = {
            "1:00" : "WAKE UP",
            "1:30" : "GO TO MARKET",
            "6:30" : "COOK",
            "7:30" : "EAT",
            "8:00" : "PLAY VIDEO GAMES",
            "11:00" : "GO TO WORK",
            "15:00" : "COME BACK HOME",
            "16:00" : "READ",
            "18:00" : "COOK",
            "19:00" : "EAT",
            "21:00" : "SLEEP",
        }
        obj = SchedulePlaceholder()
        obj.name = "John"
        obj.schedule = schedule
        entity = Entity(obj.name, r"./Sprites/Sample_Character.png",self.SCALE,obj,self.LOCATIONS["House1"],self)
        self.ENTITIES.append(entity) 
        '''
        for i,obj in enumerate(person_list):
            AI.create_schedule(obj)
            print("\n"+"-"*20+"\nSchedule for",obj.name)
            print(obj.schedule)
            entity = Entity(obj.name, r"./Sprites/Sample_Character.png",self.SCALE,obj,self.LOCATIONS["House"+str((i+1)%4)],self)
            self.ENTITIES.append(entity)
    
    def set_scale(self,scale):
        #update scale of world
        self.SCALE = scale
        self.scale()
    
    def scale(self):
        #scale the texture for rendering
        self.SCALED_TEXTURE = pygame.transform.scale_by(self.TEXTURE, self.SCALE)
    
    def scale_entities(self, scale):
        #scale all the entities in the world
        for entity in self.ENTITIES:
            entity.scale_sprite(scale)
    
    def set_x(self,x):
        #update x coordinate of world
        self.X = x
    
    def set_y(self,y):
        #update y coordinate of world
        self.Y = y
    
    def draw(self, surface):
        #render the world texture
        surface.blit(self.SCALED_TEXTURE, (self.X, self.Y))
        self.draw_entities(surface)
        #surface.blit(self.SKY, (0,0))
    
    def draw_entities(self,surface):
        #draws all the entities in the world
        for entity in self.ENTITIES:
            entity.render(surface, self.X, self.Y, self.SCALE)
    
    def set_texture(self):
        texture = pygame.image.load(r"./Sprites/World.png").convert()
        #set the texture for the world
        self.TEXTURE = texture
        self.scale()
    
    def update(self, dt):
        if self.DARKNESS > 0 and self.TIME > 11 and self.TIME < 35:
            self.DARKNESS -= 0.5
            self.SKY.fill((0,0,0,int(self.DARKNESS)))
        if self.DARKNESS < 150 and self.TIME > 35:
            self.DARKNESS += 0.5
            self.SKY.fill((0,0,0,int(self.DARKNESS)))
        for entity in self.ENTITIES:
            entity.update(dt,self)
    
    def check_collision(self, sprite):
        if pygame.sprite.spritecollide(sprite,self.SPRITE_GROUP,False,pygame.sprite.collide_mask):
            return True
        return False
    
    def get_time(self):
        time = int(self.TIME//2)
        if self.TIME%2==0:
            time = str(time)+":00"
        else:
            time = str(time)+":30"
        return time
    
def get_cell(x,y):
    x = (x - x%16)//16

class Entity:
    #entity attributes
    NAME = ""
    OBJECT = None
    X,Y = 32, 32
    SPEED = 64
    #entity sprite attributes
    FACING = "S"
    SPRITE = {}
    STATE = "SLEEP"
    FRAME = 0
    #entity actions
    with open('./actions.txt','r') as file:
            ACTIONS = file.read().split('\n')
    ACTION_DONE = False
    ACTION_TIMER = 0
    START_TIME = 0
    TASK = "SLEEP"
    TASK_INDEX = 0
    INTERACTABLE = {}
    NEXT_TASK = ""
    OTHER = None
    MEET = False
    
    def __init__(self, name, path, scale, person, house, world):
        self.NAME = name
        self.PERSON = person
        self.PATH = list()
        self.INTERACTABLE = house
        print(self.NAME+"'s attributes initialised")
        #set current location to bed

        self.X,self.Y = self.INTERACTABLE["Bed"][0]
        self.X *= 16
        self.Y *= 16
        print(self.NAME+"'s location initialised")
        #for mask
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface((16*scale,16*scale))
        sprite.image.fill("black")
        sprite.rect = sprite.image.get_rect(topleft = (self.X,self.Y))
        sprite.mask = pygame.mask.from_surface(sprite.image)
        self.SPRITE_GROUP = pygame.sprite.GroupSingle(sprite)
        print(self.NAME+"'s sprite mask initialised")
        #texture of character
        self.set_texture(path)
        print(self.NAME+"'s sprite texture initialised")
        self.scale_sprite(scale)
        print(self.NAME+"'s sprite textures scaled")
        #initialise tasks
        self.init_task(world)
        print(self.NAME+"'s task initialised\n")
    
    def set_texture(self, path):
        spritesheet = pygame.image.load(path).convert_alpha()
        #idle and walking sprites
        key = ["IDLE","WALK"]
        for i in range(2):
            self.SPRITE[key[i]] = {"N":[],"S":[],"E":[],"W":[]}
            dirs = ["E","N","W","S"]
            for j in range(24):
                image = pygame.Surface([16,32])
                image.set_colorkey(spritesheet.get_at((0,0)))
                image.blit(spritesheet,(0,0),(j*16,i*32,16,32), pygame.BLEND_ALPHA_SDL2)
                self.SPRITE[key[i]][dirs[j//6]].append(image)
        #sitting sprites
        self.SPRITE["SIT"] = {"E":[],"W":[]}
        dirs = ["E","W"]
        for i in range(12):
            image = pygame.Surface([16,32])
            image.set_colorkey(spritesheet.get_at((0,0)))
            image.blit(spritesheet,(0,0),(i*16,64,16,32), pygame.BLEND_ALPHA_SDL2)
            self.SPRITE["SIT"][dirs[i//6]].append(image)
        #reading sprites
        self.SPRITE["READ"] = []
        for i in range(12):
            image = pygame.Surface([16,32])
            image.set_colorkey(spritesheet.get_at((0,0)))
            image.blit(spritesheet,(0,0),((i+12)*16,64,16,32), pygame.BLEND_ALPHA_SDL2)
            self.SPRITE["READ"].append(image)
        #sleeping sprites
        self.SPRITE["SLEEP"] = []
        for i in range(6):
            image = pygame.Surface([16,32])
            image.set_colorkey(spritesheet.get_at((0,0)))
            image.blit(spritesheet,(0,0),((i)*16,96,16,32), pygame.BLEND_ALPHA_SDL2)
            self.SPRITE["SLEEP"].append(image)
    
    def scale_sprite(self, scale):
        #saves the scaled sprite
        self.CURRENT_SPRITE = []
        if self.STATE in ["IDLE","WALK","SIT"]:
            for frame in self.SPRITE[self.STATE][self.FACING]:
                frame = pygame.transform.scale_by(frame,scale)
                self.CURRENT_SPRITE.append(frame)
        else:
            for frame in self.SPRITE[self.STATE]:
                frame = pygame.transform.scale_by(frame,scale)
                self.CURRENT_SPRITE.append(frame)
    
    def update_distance(self,distance,next_cell):
        cell_pass = False
        if self.FACING in ["N","S"]:
            if distance >= abs((next_cell[1]*16)-self.Y):
                distance -= abs((next_cell[1]*16)-self.Y)
                self.Y = next_cell[1]*16
                if self.PATH!=[]:
                    self.set_dir()
                else:
                    distance = 0
                cell_pass = True
            else:
                if self.FACING == "N":
                    self.Y -= distance
                else:
                    self.Y += distance
                distance = 0
        else:
            if distance >= abs((next_cell[0]*16)-self.X):
                distance -= abs((next_cell[0]*16)-self.X)
                self.X = next_cell[0]*16
                if self.PATH!=[]:
                    self.set_dir()
                else:
                    distance = 0
                cell_pass = True
            else:
                if self.FACING == "W":
                    self.X -= distance
                else:
                    self.X += distance
                distance = 0
        return distance, cell_pass
    
    def check_surround(self, world):
        if self.TASK!="MEET":
            for ent in world.ENTITIES:
                if ent.NAME != self.NAME and abs(self.X-ent.X) < 160 and abs(self.Y-ent.Y) < 80:
                    #calculate probability of meeting
                    prob = self.PERSON.relationship[ent.NAME]*self.PERSON.energy
                    if random.random() < prob:
                        #release currently occupied spaces
                        if (self.X//16,self.Y//16) in world.OCCUPIED:
                            world.OCCUPIED.remove((self.X//16,self.Y//16))
                        if (ent.X//16,ent.Y//16) in world.OCCUPIED:
                            world.OCCUPIED.remove((ent.X//16,ent.Y//16))
                        #setting aside the current task
                        if self.NEXT_TASK == "" or world.TASK_PRIORITY[self.NEXT_TASK] <= world.TASK_PRIORITY[self.TASK]:
                            self.NEXT_TASK = self.TASK
                        if ent.NEXT_TASK == "" or world.TASK_PRIORITY[ent.NEXT_TASK] <= world.TASK_PRIORITY[ent.TASK]:
                            ent.NEXT_TASK = ent.TASK
                        #initialising the meeting
                        self.PERSON.energy -= 0.05
                        ent.PERSON.energy -= 0.05
                        self.MEET = True
                        self.TASK = "MEET"
                        self.STATE = "WALK"
                        self.FRAME = 0
                        ent.TASK = "MEET"
                        ent.STATE = "WALK"
                        ent.FRAME = 0
                        path = pathfinder((self.X//16,self.Y//16),((ent.X//16,ent.Y//16),),world)
                        mid = len(path)//2
                        self.PATH = path[:mid]
                        print(self.PATH)
                        ent.PATH = path[:mid-1:-1]
                        print(ent.PATH)
                        self.set_dir()
                        self.scale_sprite(world.SCALE)
                        ent.set_dir()
                        ent.scale_sprite(world.SCALE)
                        self.OTHER = ent
                        ent.OTHER = self
    
    def meet(self):
        print(True)
        self.PATH = []
        AI.conversation(self.PERSON,self.OTHER.PERSON,display = True)
    
    def update(self, dt, world):
        #print(self.PATH)
        #check for change in schedule
        time = world.get_time()
        if time in self.PERSON.schedule.keys() and self.PERSON.schedule[time] != self.TASK:
            self.change_task(time,world)
        if self.TASK == "SLEEP":
            if self.PATH != []:
                next_cell = self.PATH.pop()
                self.PATH.append(next_cell)
                distance = self.SPEED*dt
                while distance>0:
                    distance, passed = self.update_distance(distance,next_cell)
                    if passed and self.PATH!=[]:
                        next_cell = self.PATH.pop()
                        self.scale_sprite(world.SCALE)
                    elif not passed:
                        self.PATH.append(next_cell)
                    elif self.PATH == [] and (self.X//16,self.Y//16) in self.INTERACTABLE["Bed"]:
                        self.STATE = "SLEEP"
                        self.FRAME = 0
                        self.TASK = "IDLE"
                        self.scale_sprite(world.SCALE)
                if self.TASK == "SLEEP":
                    self.PATH.append(next_cell)
        elif self.TASK == "WAKE UP":
            if self.PATH != []:
                next_cell = self.PATH.pop()
                self.PATH.append(next_cell)
                distance = self.SPEED*dt
                while distance>0:
                    distance, passed = self.update_distance(distance,next_cell)
                    if passed and self.PATH!=[]:
                        next_cell = self.PATH.pop()
                        self.scale_sprite(world.SCALE)
                    elif not passed:
                        self.PATH.append(next_cell)
                    elif self.PATH == [] and (self.X//16,self.Y//16) in self.INTERACTABLE["Toilet"]:
                        self.STATE = "IDLE"
                        self.FRAME = 0
                        self.TASK = "IDLE"
                        self.scale_sprite(world.SCALE)
                if self.TASK == "WAKE UP":
                    self.PATH.append(next_cell)
            elif world.TIME - self.START_TIME > 0:
                self.update_task(world)
        elif self.TASK == "COOK":
            if self.STATE == "IDLE":
                self.ACTION_TIMER -= 1
                if self.ACTION_TIMER == 0:
                    self.TASK_INDEX = (self.TASK_INDEX+1)%5
                    self.init_task(world)
            else:
                if self.PATH != []:
                    next_cell = self.PATH.pop()
                    self.PATH.append(next_cell)
                    distance = self.SPEED*dt
                    while distance>0:
                        distance, passed = self.update_distance(distance,next_cell)
                        if passed and self.PATH!=[]:
                            next_cell = self.PATH.pop()
                            self.scale_sprite(world.SCALE)
                        elif not passed:
                            self.PATH.append(next_cell)
                        elif self.PATH == [] and (self.X//16,self.Y//16) in self.INTERACTABLE["Kitchen"]:
                            self.STATE = "IDLE"
                            self.FRAME = 0
                            if self.TASK_INDEX == 1:
                                self.FACING = "W"
                            self.scale_sprite(world.SCALE)
        elif self.TASK == "EAT":
            if self.PATH != []:
                next_cell = self.PATH.pop()
                self.PATH.append(next_cell)
                distance = self.SPEED*dt
                while distance>0:
                    distance, passed = self.update_distance(distance,next_cell)
                    if passed and self.PATH!=[]:
                        next_cell = self.PATH.pop()
                        self.scale_sprite(world.SCALE)
                    elif not passed:
                        self.PATH.append(next_cell)
                    elif self.PATH == [] and (self.X//16,self.Y//16) in self.INTERACTABLE["Kitchen_Seat"]:
                        self.STATE = "SIT"
                        self.FRAME = 0
                        self.TASK = "IDLE"
                        self.FACING = self.INTERACTABLE["Seat_Dir"][(self.X//16,self.Y//16)]
                        self.scale_sprite(world.SCALE)
                if self.TASK == "EAT":
                    self.PATH.append(next_cell)
            elif world.TIME - self.START_TIME > 0:
                self.update_task(world)
        elif self.TASK == "READ":
            if self.STATE == "IDLE":
                self.ACTION_TIMER -= 1
                if self.ACTION_TIMER == 0:
                    self.STATE = "READ"
                    self.START_TIME = world.TIME
                    self.scale_sprite(world.SCALE)
                    self.FRAME = 0
                    self.TASK = "IDLE"
            elif self.STATE == "READ" and world.TIME - self.START_TIME > 2:
                self.update_task(world)
            else:
                if self.PATH != []:
                    next_cell = self.PATH.pop()
                    self.PATH.append(next_cell)
                    distance = self.SPEED*dt
                    while distance>0:
                        distance, passed = self.update_distance(distance,next_cell)
                        if passed and self.PATH!=[]:
                            next_cell = self.PATH.pop()
                            self.scale_sprite(world.SCALE)
                        elif not passed:
                            self.PATH.append(next_cell)
                        elif self.PATH == [] and (self.X//16,self.Y//16) in self.INTERACTABLE["Bookshelf"]:
                            self.STATE = "IDLE"
                            self.FRAME = 0
                            self.scale_sprite(world.SCALE)
        elif self.TASK in ["WATCH TV","PLAY VIDEO GAMES"]:
            if self.PATH != []:
                next_cell = self.PATH.pop()
                self.PATH.append(next_cell)
                distance = self.SPEED*dt
                while distance>0:
                    distance, passed = self.update_distance(distance,next_cell)
                    if passed and self.PATH!=[]:
                        next_cell = self.PATH.pop()
                        self.scale_sprite(world.SCALE)
                    elif not passed:
                        self.PATH.append(next_cell)
                    elif self.PATH == [] and (self.X//16,self.Y//16) in self.INTERACTABLE["TV"]:
                        self.STATE = "IDLE"
                        self.FRAME = 0
                        self.TASK = "IDLE"
                        self.FACING = self.INTERACTABLE["Seat_Dir"][(self.X//16,self.Y//16)]
                        self.scale_sprite(world.SCALE)
                if self.TASK in ["WATCH TV","PLAY VIDEO GAMES"]:
                    self.PATH.append(next_cell)
        elif self.TASK == "EXCERCISE":
            if self.STATE == "IDLE":
                self.TASK_INDEX = (self.TASK_INDEX+1)%4
                self.init_task(world)
            else:
                if self.PATH != []:
                    next_cell = self.PATH.pop()
                    self.PATH.append(next_cell)
                    distance = self.SPEED*dt
                    while distance>0:
                        distance, passed = self.update_distance(distance,next_cell)
                        if passed and self.PATH!=[]:
                            next_cell = self.PATH.pop()
                            self.scale_sprite(world.SCALE)
                        elif not passed:
                            self.PATH.append(next_cell)
                        elif self.PATH == [] and (self.X//16,self.Y//16) in self.INTERACTABLE["Corner"]:
                            self.STATE = "IDLE"
                            self.FRAME = 0
                            self.scale_sprite(world.SCALE)
        elif self.TASK == "BATH":
            if self.PATH != []:
                next_cell = self.PATH.pop()
                self.PATH.append(next_cell)
                distance = self.SPEED*dt
                while distance>0:
                    distance, passed = self.update_distance(distance,next_cell)
                    if passed and self.PATH!=[]:
                        next_cell = self.PATH.pop()
                        self.scale_sprite(world.SCALE)
                    elif not passed:
                        self.PATH.append(next_cell)
                    elif self.PATH == [] and (self.X//16,self.Y//16) in self.INTERACTABLE["Bath"]:
                        self.STATE = "IDLE"
                        self.FRAME = 0
                        self.TASK = "IDLE"
                        self.scale_sprite(world.SCALE)
                if self.TASK == "BATH":
                    self.PATH.append(next_cell)
        elif self.TASK == "WAIT":
            if self.PATH != []:
                next_cell = self.PATH.pop()
                self.PATH.append(next_cell)
                distance = self.SPEED*dt
                while distance>0:
                    distance, passed = self.update_distance(distance,next_cell)
                    if passed and self.PATH!=[]:
                        next_cell = self.PATH.pop()
                        self.scale_sprite(world.SCALE)
                    elif not passed:
                        self.PATH.append(next_cell)
                    elif self.PATH == [] and (self.X//16,self.Y//16) in self.INTERACTABLE["Seat"]:
                        self.STATE = "IDLE"
                        self.FRAME = 0
                        self.TASK = "IDLE"
                        self.FACING = self.INTERACTABLE["Seat_Dir"][(self.X//16,self.Y//16)]
                        self.scale_sprite(world.SCALE)
                if self.TASK == "WAIT":
                    self.PATH.append(next_cell)
        elif self.TASK == "GO TO MARKET":
            if self.STATE == "IDLE":
                self.ACTION_TIMER -= 1
                if self.ACTION_TIMER == 0:
                    self.init_task(world)
            else:
                if self.PATH != []:
                    next_cell = self.PATH.pop()
                    self.PATH.append(next_cell)
                    distance = self.SPEED*dt
                    while distance>0:
                        distance, passed = self.update_distance(distance,next_cell)
                        if passed and self.PATH!=[]:
                            next_cell = self.PATH.pop()
                            self.scale_sprite(world.SCALE)
                        elif not passed:
                            self.PATH.append(next_cell)
                        elif self.PATH == [] and (self.X//16,self.Y//16) in world.LOCATIONS["Market"]["Items"]:
                            self.STATE = "IDLE"
                            self.FRAME = 0
                            self.scale_sprite(world.SCALE)
                    self.check_surround(world)
        elif self.TASK == "MEET":
            if self.PATH != []:
                next_cell = self.PATH.pop()
                self.PATH.append(next_cell)
                distance = self.SPEED*dt
                while distance>0:
                    distance, passed = self.update_distance(distance,next_cell)
                    if passed and self.PATH!=[]:
                        next_cell = self.PATH.pop()
                        self.scale_sprite(world.SCALE)
                    elif not passed:
                        self.PATH.append(next_cell)
                    elif self.PATH == []:
                        self.STATE = "IDLE"
                        self.FRAME = 0
                        self.ACTION_DONE = True
                        xdiff = (self.OTHER.X)-self.X
                        ydiff = (self.OTHER.Y)-self.Y
                        if xdiff > 0:
                            self.FACING = "E"
                        elif xdiff < 0:
                            self.FACING = "W"
                        elif ydiff > 0:
                            self.FACING = "S"
                        else:
                            self.FACING = "N"
                        self.scale_sprite(world.SCALE)
                        if self.MEET:
                            self.MEET = False
                            self.meet()
                if not self.ACTION_DONE:
                    self.PATH.append(next_cell)
            elif self.PERSON.is_in_conversation == False:
                self.update_task(world)
        elif self.TASK == "COME BACK HOME":
            if self.PATH != []:
                next_cell = self.PATH.pop()
                self.PATH.append(next_cell)
                distance = self.SPEED*dt
                while distance>0:
                    distance, passed = self.update_distance(distance,next_cell)
                    if passed and self.PATH!=[]:
                        next_cell = self.PATH.pop()
                        self.scale_sprite(world.SCALE)
                    elif not passed:
                        self.PATH.append(next_cell)
                    elif self.PATH == [] and (self.X//16,self.Y//16) in self.INTERACTABLE["Seat"]:
                        self.STATE = "IDLE"
                        self.FRAME = 0
                        self.TASK = "IDLE"
                        self.FACING = self.INTERACTABLE["Seat_Dir"][(self.X//16,self.Y//16)]
                        self.scale_sprite(world.SCALE)
                if self.TASK == "COME BACK HOME":
                    self.PATH.append(next_cell)
        if self.STATE == "WALK" and self.TASK != "MEET":
            self.check_surround(world)
    
    def render(self, surface, x_offset, y_offset, scale):
        #renders the sprite to the screen
        if self.STATE == "READ":
            surface.blit(self.CURRENT_SPRITE[self.FRAME//3], ((self.X * scale) + x_offset, (self.Y * scale) + y_offset - 16*scale))
            self.FRAME = (self.FRAME+1)%36
        else:
            surface.blit(self.CURRENT_SPRITE[self.FRAME//3], ((self.X * scale) + x_offset, (self.Y * scale) + y_offset - 16*scale))
            self.FRAME = (self.FRAME+1)%18
    
    def set_path(self,path):
        self.PATH = path.copy()
    
    def change_task(self, time, world):
        if self.PERSON.schedule[time] in world.TASK_PRIORITY.keys():
            if self.NEXT_TASK == "":
                if world.TASK_PRIORITY[self.TASK] <= world.TASK_PRIORITY[self.PERSON.schedule[time]]:
                    self.PERSON.energy -= 0.05
                    print(self.NAME,self.PERSON.energy)
                    self.TASK = self.PERSON.schedule[time]
                    if self.TASK in ["COOK","EXCERCISE"]:
                        self.TASK_INDEX = 0
                    self.init_task(world)
            else:
                if world.TASK_PRIORITY[self.NEXT_TASK] < world.TASK_PRIORITY[self.PERSON.schedule[time]]:
                    self.NEXT_TASK = self.PERSON.schedule[time]
    
    def update_task(self,world):
        if self.NEXT_TASK == "":
            self.TASK = "WAIT"
            self.init_task(world)
        else:
            self.TASK = self.NEXT_TASK
            self.NEXT_TASK = ""
            self.init_task(world)
    
    def init_task(self,world):
        print(world.OCCUPIED)
        if (self.X//16,self.Y//16) in world.OCCUPIED:
            world.OCCUPIED.remove((self.X//16,self.Y//16))
        if self.PATH != [] and self.PATH[0] in world.OCCUPIED:
            world.OCCUPIED.remove(self.PATH[0])
        if self.TASK == "SLEEP" and (self.X//16,self.Y//16) not in self.INTERACTABLE["Bed"]:
            #getting ready for walking to bed
            self.STATE = "WALK"
            self.FRAME = 0
            self.PATH = pathfinder((self.X//16,self.Y//16),self.INTERACTABLE["Bed"],world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
        elif self.TASK == "WAKE UP" and (self.X//16,self.Y//16) not in self.INTERACTABLE["Toilet"]:
            #get path to a tiolet sink
            self.STATE = "WALK"
            self.FRAME = 0
            self.START_TIME = world.TIME
            self.PATH = pathfinder((self.X//16,self.Y//16),self.INTERACTABLE["Toilet"],world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
        elif self.TASK == "COOK":
            #get path to a kitchen 
            self.STATE = "WALK"
            self.FRAME = 0
            self.ACTION_TIMER = 60
            self.PATH = pathfinder((self.X//16,self.Y//16),(self.INTERACTABLE["Kitchen"][self.TASK_INDEX],),world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
        elif self.TASK == "EAT" and (self.X//16,self.Y//16) not in self.INTERACTABLE["Kitchen_Seat"]:
            #get path to chair
            self.STATE = "WALK"
            self.FRAME = 0
            self.START_TIME = world.TIME
            self.PATH = pathfinder((self.X//16,self.Y//16),self.INTERACTABLE["Kitchen_Seat"],world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
        elif self.TASK == "READ" and (self.X//16,self.Y//16) not in self.INTERACTABLE["Bookshelf"]:
            #get path to bookshelf
            self.STATE = "WALK"
            self.FRAME = 0
            self.ACTION_TIMER = 60
            self.PATH = pathfinder((self.X//16,self.Y//16),self.INTERACTABLE["Bookshelf"],world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
        elif self.TASK in ["WATCH TV","PLAY VIDEO GAMES"] and (self.X//16,self.Y//16) not in self.INTERACTABLE["TV"]:
            #get path to chair
            self.STATE = "WALK"
            self.FRAME = 0
            self.PATH = pathfinder((self.X//16,self.Y//16),self.INTERACTABLE["TV"],world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
        elif self.TASK == "EXCERCISE":
            #get path to a house corner (walks around the house) 
            self.STATE = "WALK"
            self.FRAME = 0
            self.PATH = pathfinder((self.X//16,self.Y//16),(self.INTERACTABLE["Corner"][self.TASK_INDEX],),world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
        elif self.TASK == "BATH" and (self.X//16,self.Y//16) not in self.INTERACTABLE["Bath"]:
            #get path to shower
            self.STATE = "WALK"
            self.FRAME = 0
            self.PATH = pathfinder((self.X//16,self.Y//16),self.INTERACTABLE["Bath"],world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
        elif self.TASK == "WAIT" and (self.X//16,self.Y//16) not in self.INTERACTABLE["Seat"]:
            #get path to seat
            self.STATE = "WALK"
            self.FRAME = 0
            self.PATH = pathfinder((self.X//16,self.Y//16),self.INTERACTABLE["Seat"],world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
        elif self.TASK == "GO TO MARKET":
            #get path to market
            self.STATE = "WALK"
            self.FRAME = 0
            self.ACTION_TIMER = 60
            loc = (self.X//16,self.Y//16)
            while(loc == (self.X//16,self.Y//16) or loc in world.OCCUPIED):
                loc = random.choice(world.LOCATIONS["Market"]["Items"])
            self.PATH = pathfinder((self.X//16,self.Y//16),(loc,),world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
        elif self.TASK == "COME BACK HOME" and (self.X//16,self.Y//16) not in self.INTERACTABLE["Seat"]:
            #get path to seat
            self.STATE = "WALK"
            self.FRAME = 0
            self.PATH = pathfinder((self.X//16,self.Y//16),self.INTERACTABLE["Seat"],world)
            #setting facing direction
            self.set_dir()
            self.scale_sprite(world.SCALE)
    
    def set_dir(self):
        loc = self.PATH.pop()
        xdiff = (loc[0]*16)-self.X
        ydiff = (loc[1]*16)-self.Y
        self.PATH.append(loc)
        if xdiff > 0:
            self.FACING = "E"
        elif xdiff < 0:
            self.FACING = "W"
        elif ydiff > 0:
            self.FACING = "S"
        else:
            self.FACING = "N"
