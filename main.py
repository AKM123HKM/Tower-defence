import pygame
from settings import *
from level import Level

#Initializing pygame
pygame.init()

# Main Game
class Game:
    def __init__(self,width,height,title,fps):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        self.fps = fps
        self.level = Level()
        self.loop = True
    
    def run(self):
        while self.loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loop = False
                self.level.handle_input(event) # Handles all the input in the level
                self.level.sidebar.handle_input(event) # Handles all the input in the sidebar 

            self.screen.fill((50,50,50)) # My preffered color for background
            self.level.draw()
            self.level.update()
            pygame.display.update()

            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT, TITLE, FPS)
    game.run()