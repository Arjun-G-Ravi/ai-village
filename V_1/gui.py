import pygame
import random

pygame.init()

class Window:
    #game attributes
    DRAGGING = False
    DT = 1
    
    def __init__(self):
        #create window with fullscreen
        self.SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #create pygame clock
        self.CLOCK = pygame.time.Clock()
        #take window width and height
        self.WINDOW_WIDTH,self.WINDOW_HEIGHT = pygame.display.get_window_size()
        #instantiate the world
        self.WORLD = World()
        self.WORLD.set_texture(pygame.image.load(r".\Sprites\Sample_World.png").convert())
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


    def update(self):
        #update events
        pass
    
    def render(self):
        #render events
        self.SCREEN.fill("gray")
        self.WORLD.draw(self.SCREEN)
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
    #Time attributes
    TIME = 0
    MAX_TIME = 48         # 24 * 2 (30 minute intervals)
    #important locations
    LOCATIONS = {
        "House1" : ((25,29),(26,29)),
        "House2" : ((26,83),(27,83)),
        "House3" : ((145,34),(146,34)),
        "House4" : ((158,90),(159,90)),
        "Market" : ((93,69),(94,69),(93,39),(94,39),(113,54),(113,55),(73,54),(73,55))
    }
    
    def __init__(self):
        #setting locations that cannot be walked on
        self.set_invalid([i for j in self.LOCATIONS for i in self.LOCATIONS[j]])
        
        #create list of entities in the environment
        self.init_entities()
    
    def init_entities(self):
        #create the entities in the world
        self.ENTITIES.append(Entity("John", r".\Sprites\Sprite-0002.png",self.SCALE))
        self.ENTITIES.append(Cow("Cow",r".\Sprites\Cow_Sprite.png", self.SCALE))
    
    def set_invalid(self, exceptions):
        self.INVALID = [(i,0) for i in range(self.WIDTH)] + [(0,i) for i in range(self.HEIGHT)]                                 #top and left
        self.INVALID += [(i,self.HEIGHT-1) for i in range(self.WIDTH)] + [(self.WIDTH-1,i) for i in range(self.HEIGHT)]         #bottom and right
        self.INVALID += [(i,1) for i in range(1,self.WIDTH-1)] + [(1,i) for i in range(1,self.HEIGHT-1)]                        #top and left(2nd layer)
        self.INVALID += [(i,self.HEIGHT-2) for i in range(1,self.WIDTH-1)] + [(self.WIDTH-2,i) for i in range(1,self.HEIGHT-1)] #bottom and right(2nd layer)
        self.INVALID += [(i,10) for i in range(13,39)] + [(i,29) for i in range(13,39) if (i,29) not in exceptions]     #top and bottom(house1)
        self.INVALID += [(13,i) for i in range(10,30)] + [(38,i) for i in range(10,30)]                                 #left and right(house1)
        self.INVALID += [(i,59) for i in range(13,42)] + [(i,83) for i in range(13,42) if (i,83) not in exceptions]     #top and bottom(house2)
        self.INVALID += [(13,i) for i in range(59,84)] + [(41,i) for i in range(59,84)]                                 #left and right(house2)
        self.INVALID += [(i,19) for i in range(140,173)] + [(i,34) for i in range(140,173) if (i,34) not in exceptions] #top and bottom(house3)
        self.INVALID += [(140,i) for i in range(19,35)] + [(172,i) for i in range(19,35)]                               #left and right(house3)
        self.INVALID += [(i,68) for i in range(145,174)] + [(i,90) for i in range(145,174) if (i,90) not in exceptions] #top and bottom(house4)
        self.INVALID += [(145,i) for i in range(68,91)] + [(173,i) for i in range(68,91)]                               #left and right(house4)
        self.INVALID += [(i,39) for i in range(73,114) if (i,39) not in exceptions]                                    #top(market)
        self.INVALID += [(i,69) for i in range(73,114) if (i,69) not in exceptions]                                    #bottom(market)
        self.INVALID += [(73,i) for i in range(39,70) if (113,i) not in exceptions]                                    #left(market)
        self.INVALID += [(113,i) for i in range(39,70) if (113,i) not in exceptions]                                   #right(market)
    
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
    
    def draw_entities(self,surface):
        #draws all the entities in the world
        for entity in self.ENTITIES:
            entity.render(surface, self.X, self.Y, self.SCALE)
    
    def set_texture(self, texture):
        #set the texture for the world
        self.TEXTURE = texture
        self.scale()
        

class Entity:
    #entity attributes
    NAME = ""
    OBJECT = None
    X,Y = 32,32
    #entity sprite attributes
    FACING = "NORTH"
    SPRITE = {}
    CURRENT_SPRITE = None
    #entity actions
    with open('./actions.txt','r') as file:
            ACTIONS = file.read().split('\n')
    STATE = "IDLE"
    
    def __init__(self, name, path, scale):
        self.NAME = name
        self.set_texture(path, scale)
    
    def set_texture(self, path, scale):
        #splits the spritesheet of the entities
        dirs = ["SOUTH", "NORTH", "EAST", "WEST"]
        spritesheet = pygame.image.load(path).convert_alpha()
        for i in range(4):
            image = pygame.Surface([16,16])
            image.set_colorkey(spritesheet.get_at((0,0)))
            image.blit(spritesheet,(0,0),(i*16,0,16,16), pygame.BLEND_ALPHA_SDL2)
            self.SPRITE[dirs[i]] = image
        self.CURRENT_SPRITE = pygame.transform.scale_by(self.SPRITE[self.FACING], scale)
     
    def scale_sprite(self, scale):
        #saves the scaled sprite
        self.CURRENT_SPRITE = pygame.transform.scale_by(self.SPRITE[self.FACING], scale)
    
    def render(self, surface, x_offset, y_offset, scale):
        #renders the sprite to the screen
        surface.blit(self.CURRENT_SPRITE, ((self.X * scale) + x_offset, (self.Y * scale) + y_offset))

class Cow(Entity):
    REGION = ((61,5), (117,24))
    ACTIONS = [ "IDLE", "EATING", "WALKING" ]
    SPRITE = []
    
    def __init__(self, name, path, scale):
        self.X = random.randint(self.REGION[0][0], self.REGION[1][0])*scale*16
        self.Y = random.randint(self.REGION[0][1], self.REGION[1][1])*scale*16
        
        self.set_texture(path, scale)
        
    def set_texture(self, path, scale):
        spritesheet = pygame.image.load(path).convert_alpha()
        image = pygame.Surface([16,32])
        image.blit(spritesheet,(0,0),(0,0,16,32))
        image.set_colorkey(spritesheet.get_colorkey())
        self.SPRITE.append(image)
        image = pygame.Surface([16,32])
        image.blit(spritesheet,(0,0),(16,0,16,32))
        image.set_colorkey(spritesheet.get_colorkey())
        self.SPRITE.append(image)
        image = pygame.Surface([32,16])
        image.blit(spritesheet,(0,0),(0,32,32,16))
        image.set_colorkey(spritesheet.get_colorkey())
        self.SPRITE.append(image)
        image = pygame.Surface([32,16])
        image.blit(spritesheet,(0,0),(0,48,32,16))
        image.set_colorkey(spritesheet.get_colorkey())
        self.SPRITE.append(image)
        self.CURRENT_SPRITE = pygame.transform.scale_by(self.SPRITE[1], scale)
    
    def scale_sprite(self, scale):
        self.CURRENT_SPRITE = pygame.transform.scale_by(self.SPRITE[1], scale)