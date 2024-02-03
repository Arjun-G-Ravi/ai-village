import pygame

pygame.init()

class World:
    SCALE = 2
    X = 0
    Y = 0
    WIDTH = 1600
    HEIGHT = 1600

    def set_scale(self,scale):
        self.SCALE = scale
    
    def set_x(self,x):
        self.X = x
    
    def set_y(self,y):
        self.Y = y

class Window:

    DRAGGING = False
    
    def __init__(self):
        self.SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = pygame.display.get_window_size()

        self.WORLD = World()

        self.event_loop()

    def event_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
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
                    if self.DRAGGING:
                        pos = event.pos
                        x = pos[0] + x_offset
                        y = pos[1] + y_offset
                        self.WORLD.set_x(max(min(0,x),-self.WORLD.WIDTH * self.WORLD.SCALE + self.WINDOW_WIDTH))
                        self.WORLD.set_y(max(min(0,y),-self.WORLD.HEIGHT * self.WORLD.SCALE + self.WINDOW_HEIGHT))

            self.update()

            self.render()


    def update(self):
        #update events
        pass
    
    def render(self):
        self.SCREEN.fill("gray")

        color = [0,0,0]
        index = 0
        for i in range(100):
            for j in range(100):
                pygame.draw.rect(self.SCREEN, color, (self.WORLD.X + j*32,self.WORLD.Y + i*32,32,32))
                color[0] = (color[0] + 1)%256
                color[1] = (color[1] + 1)%256
                color[2] = (color[2] + 1)%256
            

        #pygame.draw.rect(self.SCREEN, (0,0,0), (16,16,32,32))

        pygame.display.flip()

if __name__ == "__main__":
    win = Window()