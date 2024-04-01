import pygame
from sprite import Sprite, EnemySprite
from settings import *

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.grid = Grid(ROW, COL, self.display_surface)

        self.placed_sprites = pygame.sprite.Group()
        self.rotation_sprites = pygame.sprite.Group()
        self.test_sprite = Sprite("dir_triangle.png",(-100,-100))
        self.enemy_sprite = EnemySprite("assets/enemy/tank_0.png",self.grid.get_pos((17,0),False,False),0)
        self.placed_sprites.add(self.enemy_sprite)
        self.selected_sprite = None

    def handle_input(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button(event.pos, event.button)
        elif event.type == pygame.KEYDOWN:
            self.handle_key_down(event)

    def handle_mouse_motion(self, pos):
        self.test_sprite.rect.center = self.grid.get_pos(pos, True, True)

    def handle_mouse_button(self, pos, button):
        if button == pygame.BUTTON_RIGHT:
            self.handle_right_click(pos)
        elif button == pygame.BUTTON_LEFT:
            self.handle_left_click(pos)

    def handle_right_click(self, pos):
        grid_pos = self.grid.get_pos(pos, True, False)
        if not self.grid.grid[grid_pos[0]][grid_pos[1]]:
            sprite = Sprite("dir_triangle.png", self.grid.get_pos(pos, True, True))
            self.placed_sprites.add(sprite)
            self.rotation_sprites.add(sprite)

    def handle_left_click(self, pos):
        for sprite in self.placed_sprites.sprites():
            if sprite.rect.collidepoint(pos):
                self.selected_sprite = sprite
                break
        else:
            self.selected_sprite = None

    def handle_key_down(self, event):
        if self.selected_sprite in self.rotation_sprites.sprites():
            if event.key == pygame.K_LEFT:
                self.selected_sprite.change_rotation(90)
            elif event.key == pygame.K_RIGHT:
                self.selected_sprite.change_rotation(-90)
            elif event.key == pygame.K_x:
                self.selected_sprite.kill()
        if event.key == pygame.K_s:
            self.enemy_sprite.speed = 5

    def check_in_between(self,left,between,right):
        x, y = False, False
        left_x, left_y = left[0] , left[1]
        between_x, between_y = between[0], between[1]
        right_x, right_y = right[0], right[1]
        if right_x > left_x:
            if left_x <= between_x and right_x >= between_x:
                x = True
        else:
            if right_x <= between_x and left_x >= between_x:
                x = True
        if right_y > left_y:
            if left_y <= between_y and right_y >= between_y:
                y = True
        else:
            if right_y <= between_y and left_y >= between_y:
                y = True
        
        return x and y
        
    def friend_collision(self):
        offset = (0,0)
        for sprite in self.placed_sprites.sprites():
            offset = pygame.Vector2(offset).elementwise() * self.enemy_sprite.rect.size
            if pygame.Rect(self.enemy_sprite.rect.topleft + offset, self.enemy_sprite.rect.size).colliderect(sprite.rect):
                if self.enemy_sprite.direction == "up":
                    offset = 0, -1
                elif self.enemy_sprite.direction == "left":
                    offset = 1, 0
                elif self.enemy_sprite.direction == "down":
                    offset = 0, 1
                elif self.enemy_sprite.direction == "right":
                    offset = -1, 0

    def check_collision(self):
        for sprite in self.rotation_sprites.sprites():
            if self.check_in_between(self.enemy_sprite.prev_pos,sprite.rect.center,self.enemy_sprite.rect.center):
                print('COLLIDES')
                if sprite.rotation == 0: 
                    self.enemy_sprite.direction = "up"
                elif sprite.rotation == 90: 
                    self.enemy_sprite.direction = "left"
                elif sprite.rotation == 180: 
                    self.enemy_sprite.direction = "down"
                elif sprite.rotation == 270: 
                    self.enemy_sprite.direction = "right"

    def draw(self):
        self.grid.draw_grid()
        self.placed_sprites.draw(self.display_surface)
        for sprite in self.placed_sprites.sprites():
            pygame.draw.rect(self.display_surface,(255,0,0),sprite.rect,1)
        self.display_surface.blit(self.test_sprite.image,self.test_sprite.rect)

    def update(self):
        self.enemy_sprite.move()
        self.check_collision()

class Grid:
    def __init__(self,row,col,display_surf):
        self.row, self.col = row, col
        self.display_surf = display_surf
        self.grid = []
        self.initialize_grid()

    def initialize_grid(self):
        for i in range(self.row):
            self.grid.append([])
            for j in range(self.col):
                self.grid[i].append("")

    def draw_grid(self):
        for i in range(self.row):
            pygame.draw.line(self.display_surf,(WHITE),(i*GRID_SIZE,0),(i*GRID_SIZE,HEIGHT))
        for i in range(self.col):
            pygame.draw.line(self.display_surf,(WHITE),(0,i*GRID_SIZE),(WIDTH,i*GRID_SIZE))

    def get_pos(self,pos,grid_pos,centered): # If grid_pos: window_pos -> grid_pos else: grid_pos -> window_pos
        if grid_pos:
            grid_x = int(pos[0] / GRID_SIZE)
            grid_y = int(pos[1] / GRID_SIZE)
            if centered:
                centered_x = (grid_x * GRID_SIZE + ((grid_x * GRID_SIZE) + GRID_SIZE)) // 2
                centered_y = (grid_y * GRID_SIZE + ((grid_y * GRID_SIZE) + GRID_SIZE)) // 2
                return (centered_x,centered_y)
            return (grid_x,grid_y)
        else:
            main_x = pos[0] * GRID_SIZE
            main_y = pos[1] * GRID_SIZE
            return (self.get_pos((main_x,main_y),True,True))
