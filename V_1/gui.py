import pygame

pygame.init()
class Window:

    DRAGGING = False
    
    def __init__(self):
        self.SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        
        self.WINDOW_WIDTH,self.WINDOW_HEIGHT = pygame.display.get_window_size()

        self.WORLD = World()
        self.WORLD.set_texture(pygame.image.load("World_Texture_placeholder.png").convert())

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
                    self.DRAGGING = True
                    mouse_pos = event.pos
                    x_offset = self.WORLD.X - mouse_pos[0]
                    y_offset = self.WORLD.Y - mouse_pos[1]
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.DRAGGING = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.DRAGGING and (self.WORLD.WIDTH*self.WORLD.SCALE) > self.WINDOW_WIDTH:
                        pos = event.pos
                        x = pos[0] + x_offset
                        y = pos[1] + y_offset
                        self.WORLD.set_x(max(min(0,x),-self.WORLD.WIDTH * self.WORLD.SCALE + self.WINDOW_WIDTH))
                        self.WORLD.set_y(max(min(0,y),-self.WORLD.HEIGHT * self.WORLD.SCALE + self.WINDOW_HEIGHT))
                elif event.type == pygame.MOUSEWHEEL:
                    scale = min(max(1,self.WORLD.SCALE + event.precise_y),4)
                    x,y = pygame.mouse.get_pos()
                    
                    #under development
                    posx = (x - self.WORLD.X)*scale - x
                    posy = (y - self.WORLD.Y)*scale - y
                    
                    self.WORLD.set_x(-posx/scale)
                    self.WORLD.set_y(-posy/scale)
                    
                    self.WORLD.set_scale(scale)


            self.update()

            self.render()


    def update(self):
        #update events
        pass
    
    def render(self):
        self.SCREEN.fill("gray")

        self.WORLD.draw(self.SCREEN)

        pygame.display.update()

class World:
    SCALE = 1
    MAX_SCALE = 4
    X = 0
    Y = 0
    WIDTH = 3200
    HEIGHT = 1600
    TEXTURE = None
    SCALED_TEXTURE = None

    def set_scale(self,scale):
        self.SCALE = scale
        self.scale()
    
    def set_x(self,x):
        self.X = x
    
    def set_y(self,y):
        self.Y = y
    
    def draw(self, surface):
        surface.blit(self.SCALED_TEXTURE, (self.X, self.Y))
    
    def set_texture(self, texture):
        self.TEXTURE = texture
        self.scale()
        
    def scale(self):
        self.SCALED_TEXTURE = pygame.transform.scale(self.TEXTURE, (self.WIDTH*self.SCALE, self.HEIGHT*self.SCALE))


if __name__ == "__main__":
    win = Window()