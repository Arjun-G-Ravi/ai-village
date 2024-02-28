import pygame

pygame.init()
class Window:
    #game attributes
    DRAGGING = False
    
    def __init__(self):
        #create window with fullscreen
        self.SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #take window width and height
        self.WINDOW_WIDTH,self.WINDOW_HEIGHT = pygame.display.get_window_size()
        #instantiate the world
        self.WORLD = World()
        self.WORLD.set_texture(pygame.image.load("Sample_world.png").convert())
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
            #game updates
            self.update()
            #game rendering
            self.render()


    def update(self):
        #update events
        pass
    
    def render(self):
        #render events
        self.SCREEN.fill("gray")
        self.WORLD.draw(self.SCREEN)
        pygame.display.update()

class World:
    #world attributes
    SCALE = 1
    MAX_SCALE = 4
    X = 0
    Y = 0
    WIDTH = 200
    HEIGHT = 100
    CELL_SIZE = 16
    TEXTURE = None
    SCALED_TEXTURE = None
    #important locations
    LOCATIONS = {
        "House1" : ((26,29),(27,29)),
        "House2" : ((26,83),(27,83)),
        "House3" : ((145,34),(146,34)),
        "House4" : ((158,90),(159,90)),
        "Market" : ((93,69),(94,69),(93,39),(94,39),(113,54),(113,55),(73,54),(73,55))
    }
    
    def __init__(self):
        #setting locations that cannot be walked on
        self.set_invalid([i for j in self.LOCATIONS for i in self.LOCATIONS[j]])
    
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
    
    def set_x(self,x):
        #update x coordinate of world
        self.X = x
    
    def set_y(self,y):
        #update y coordinate of world
        self.Y = y
    
    def draw(self, surface):
        #render the world texture
        surface.blit(self.SCALED_TEXTURE, (self.X, self.Y))
    
    def set_texture(self, texture):
        #set the texture for the world
        self.TEXTURE = texture
        self.scale()
        
    def scale(self):
        #scale the texture for rendering
        self.SCALED_TEXTURE = pygame.transform.scale_by(self.TEXTURE, self.SCALE)

class Cow:
    pass

if __name__ == "__main__":
    win = Window()