import pygame
from sprite import Sprite, EnemySprite
from settings import *
from sidebar import Sidebar

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.grid = Grid(ROW, COL, self.display_surface)

        #Contains all the sprites placed in the level
        self.placed_sprites = pygame.sprite.Group()
        # Contains all the sprites which help the enemy to rotate (Direction triangles)
        self.rotation_sprites = pygame.sprite.Group()

        # Single enemy sprite for early testing
        self.enemy_sprite = EnemySprite("assets/enemy/tank_0.png",self.grid.get_pos((0,0),False,False),0)
        self.placed_sprites.add(self.enemy_sprite)
        
        self.selected_sprite = None # Selected sprite which will be placed in the level
        self.mouse_sprite = self.set_mouse_sprite("") # Sprite which will follow the mouse
        self.mouse_spr_img_path = "" # Image path of the mouse sprite (to create and place a new sprite)
        
        self.pause_frames = 0 # Used to stop some actions for a specific amount of frames

        self.test_num = 0

        self.sidebar = Sidebar((WIDTH - (SIDEBAR_SIZE*GRID_SIZE), 0),(self.set_mouse_sprite,IMAGE_BUTTON_COMMAND),(self.set_mouse_sprite,IMAGE_BUTTON_COMMAND),(self.set_enemy_number))

    def set_enemy_number(self,num):
        if num:
            self.test_num = int(num)
        else:
            self.test_num = 0

    def set_mouse_sprite(self,image_path):
        if image_path:
            if image_path == self.mouse_spr_img_path:
                self.mouse_sprite = ""
                self.mouse_spr_img_path = ""
            else:
                self.mouse_sprite = Sprite(image_path,(-100,100))
                self.mouse_spr_img_path = image_path
        else:
            self.mouse_sprite = ""

    def handle_input(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button(event.pos, event.button)
        elif event.type == pygame.KEYDOWN:
            self.handle_key_down(event)

    def handle_mouse_motion(self, pos):
        if self.mouse_sprite:
            if pos[0] < WIDTH - (SIDEBAR_SIZE * GRID_SIZE):
                self.mouse_sprite.rect.center = self.grid.get_pos(pos, True, True)

    def handle_mouse_button(self, pos, button):
        if button == pygame.BUTTON_RIGHT:
            self.handle_right_click(pos)
        elif button == pygame.BUTTON_LEFT:
            self.handle_left_click(pos)

    def check_sprite_type(self,spr_img_path,sprite):
        if spr_img_path in DEFENCE:
            pass
        elif spr_img_path in DIRECTION:
            self.rotation_sprites.add(sprite)
        elif spr_img_path in ENEMY:
            pass

    def handle_right_click(self, pos):
        if self.mouse_sprite:
            try:
                grid_pos = self.grid.get_pos(pos, True, False)
                if not self.grid.grid[grid_pos[0]][grid_pos[1]]:
                    sprite = Sprite(self.mouse_spr_img_path, self.grid.get_pos(pos, True, True))
                    
                    self.placed_sprites.add(sprite)
                    self.check_sprite_type(self.mouse_spr_img_path,sprite)
                    
                    self.grid.grid[grid_pos[0]][grid_pos[1]] = "x"
            
            except IndexError:
                pass

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

        if event.key == pygame.K_x:
            if self.selected_sprite:
                self.selected_sprite.kill()
                selected_grid = self.grid.get_pos(self.selected_sprite.rect.center,True,False)
                self.grid.grid[selected_grid[0]][selected_grid[1]] = ""

        elif event.key == pygame.K_s:
            if self.enemy_sprite.speed == 5:
                self.enemy_sprite.speed = 0
                
            else:
                self.enemy_sprite.speed = 5

    def check_in_between(self,player, enemy):
        return player.collidepoint(enemy.center)

    def set_rotation(self,rotation):
        if rotation == 0: 
            self.enemy_sprite.direction = "up"
        elif rotation == 90: 
            self.enemy_sprite.direction = "left"
        elif rotation == 180: 
            self.enemy_sprite.direction = "down"
        elif rotation == 270: 
            self.enemy_sprite.direction = "right"
        self.enemy_sprite.set_rotation(rotation)
    
    def check_collision(self):
        self.pause_frames += 1
        for sprite in self.rotation_sprites.sprites():
            if self.check_in_between(self.enemy_sprite.rect,sprite.rect):
                #Allign the enemy sprite at the center of the grid and removes the collision
                self.enemy_sprite.rect.center = sprite.rect.center
                sprite.rect.width, sprite.rect.height = 0, 0

                self.set_rotation(sprite.rotation)
                
        if self.pause_frames >= 8: #Removes collision from the triangles for 8 frames
                                #to allign the enemy sprite and move ahead without stucking
            for sprite in self.rotation_sprites.sprites():
                sprite.rect.width, sprite.rect.height = sprite.image.get_width(), sprite.image.get_height()
                self.pause_frames = 0
                
    def draw(self):
        self.grid.draw_grid()
        self.sidebar.draw()
        self.placed_sprites.draw(self.display_surface)
        for sprite in self.placed_sprites.sprites():
            pygame.draw.rect(self.display_surface,(255,0,0),sprite.rect,1)
        if self.mouse_sprite:
            self.display_surface.blit(self.mouse_sprite.image,self.mouse_sprite.rect)
        num_surf = FONT.render(str(self.test_num),True,(255,255,255))
        self.display_surface.blit(num_surf,(0,0))

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
        for i in range(self.row + 1):
            pygame.draw.line(self.display_surf,(WHITE),(i*GRID_SIZE,0),(i*GRID_SIZE,HEIGHT))
        for i in range(self.col + 1):
            pygame.draw.line(self.display_surf,(WHITE),(0,i*GRID_SIZE),((WIDTH - (SIDEBAR_SIZE * GRID_SIZE)),i*GRID_SIZE))

    def get_pos(self,pos,grid_pos,centered): # If grid_pos: window_pos -> grid_pos else: grid_pos -> window_pos
        if grid_pos:
            grid_x = int(pos[0] / GRID_SIZE)
            grid_y = int(pos[1] / GRID_SIZE)
            if centered:
                centered_x = (grid_x * GRID_SIZE + ((grid_x * GRID_SIZE) + GRID_SIZE)) // 2
                centered_y = (grid_y * GRID_SIZE + ((grid_y * GRID_SIZE) + GRID_SIZE)) // 2
                return (centered_x,centered_y)
            return(grid_x,grid_y)
        else:
            main_x = pos[0] * GRID_SIZE
            main_y = pos[1] * GRID_SIZE
            return (self.get_pos((main_x,main_y),True,True))