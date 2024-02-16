import pygame
import sys
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
        if sys.platform == 'linux':
            self.WORLD.set_texture(pygame.image.load("V_1/World_Texture_placeholder.png").convert()) # Dont know if this repr works with windows. So created a split
        else:
            self.WORLD.set_texture(pygame.image.load("World_Texture_placeholder.png").convert())
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
                    if self.DRAGGING and (self.WORLD.WIDTH*self.WORLD.SCALE) > self.WINDOW_WIDTH:
                        #calculation of world coordinates after dragging
                        pos = event.pos
                        x = pos[0] + x_offset
                        y = pos[1] + y_offset
                        #updating world coordinates
                        self.WORLD.set_x(max(min(0,x),-self.WORLD.WIDTH * self.WORLD.SCALE + self.WINDOW_WIDTH))
                        self.WORLD.set_y(max(min(0,y),-self.WORLD.HEIGHT * self.WORLD.SCALE + self.WINDOW_HEIGHT))
                elif event.type == pygame.MOUSEWHEEL:
                    #calculation of new world scale
                    scale = min(max(1,self.WORLD.SCALE + event.precise_y),4)
                    #calculation for new world coordinates
                    x,y = pygame.mouse.get_pos()
                    posx = ((x - self.WORLD.X)//self.WORLD.SCALE)*scale - x
                    posy = ((y - self.WORLD.Y)//self.WORLD.SCALE)*scale - y
                    #updating world coordinates and world scale
                    self.WORLD.set_x(max(min(-posx,0),-self.WORLD.WIDTH * scale + self.WINDOW_WIDTH))
                    self.WORLD.set_y(max(min(-posy,0),-self.WORLD.HEIGHT * scale + self.WINDOW_HEIGHT))
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
    WIDTH = 3200
    HEIGHT = 1600
    TEXTURE = None
    SCALED_TEXTURE = None

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


if __name__ == "__main__":
    win = Window()