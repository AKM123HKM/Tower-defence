import pygame
from settings import *
from utility import Button, EntryBox

class Sidebar:
    def __init__(self,pos,*funcs):
        self.display_surface = pygame.display.get_surface()
        self.funcs = funcs
        self.sidebar_height = 0
        self.sidebar_y = 0
        self.prev_utility_height = 0
        self.rect = pygame.rect.Rect(pos[0],pos[1],SIDEBAR_SIZE*GRID_SIZE,HEIGHT)
        self.buttons = []
        self.entry_boxes = []
        self.initialize_buttons()

    def initialize_buttons(self):
        y_offset = 0
        
        for i,data in enumerate(SIDEBAR_DATA.keys()):
            utility = SIDEBAR_DATA[data]
            
            if utility["type"] == "button":
                y_offset += BUTTON_OFFSET
                button_pos = ((WIDTH - (SIDEBAR_SIZE * GRID_SIZE)) + BUTTON_OFFSET,self.prev_utility_height + y_offset)
                try:
                    if self.funcs[i][1] == IMAGE_BUTTON_COMMAND:
                        # Button with function and image
                        button = Button(self.display_surface,button_pos,utility["image_path"],utility["text"],self.funcs[i][0],utility["image_path"])
                except IndexError:
                    button = Button(self.display_surface,button_pos)

                self.buttons.append(button)
                self.prev_utility_height += BUTTON_HEIGHT
                self.sidebar_height += BUTTON_HEIGHT + y_offset
            
            elif utility["type"] == "entry":
                y_offset += ENTRY_BOX_OFFSET
                entry_pos = ((WIDTH - (SIDEBAR_SIZE * GRID_SIZE)) + ENTRY_BOX_OFFSET,self.prev_utility_height + y_offset)
                try:
                    entry_box = EntryBox(self.display_surface,entry_pos,func = self.funcs[i])
                except IndexError:
                    entry_box = EntryBox(self.display_surface,entry_pos)
                
                self.entry_boxes.append(entry_box)
                self.prev_utility_height += ENTRY_BOX_HEIGHT
                self.sidebar_height += ENTRY_BOX_HEIGHT + y_offset
        
        self.sidebar_height = (self.sidebar_height / SCROLL_SPEED) + 20
    
    def handle_mouse_motion(self,pos):
        entry_box_collision = False
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                button.hover_action()
            else:
                button.hover_action(False)

        for entry_box in self.entry_boxes:
            if entry_box.rect.collidepoint(pos):
                entry_box_collision = True
                break
            else:
                entry_box_collision = False
            
        if entry_box_collision:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_left_click(self,pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                button.func()

        for entry_box in self.entry_boxes:
            if entry_box.rect.collidepoint(pos):
                entry_box.left_click_action(True)
            else:
                entry_box.left_click_action(False)

    def handle_mouse_wheel(self,y):
        self.sidebar_y += -y * SCROLL_SPEED
        if self.sidebar_y >= 0 and self.sidebar_y <= self.sidebar_height:
            for button in self.buttons:
                button.scroll_action(y,SCROLL_SPEED)
            for entry_box in self.entry_boxes:
                entry_box.scroll_action(y,SCROLL_SPEED)
        elif self.sidebar_y < 0: self.sidebar_y = 0
        elif self.sidebar_y > self.sidebar_height: self.sidebar_y = self.sidebar_height
    
    def handle_input(self,event):
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self.handle_mouse_motion(pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = event.pos
                self.handle_left_click(pos)
        elif event.type == pygame.MOUSEWHEEL:
            self.handle_mouse_wheel(event.y)
        elif event.type == pygame.KEYDOWN:
            for entry_box in self.entry_boxes:
                entry_box.key_input_action(event)

    def draw(self):
        pygame.draw.rect(self.display_surface,WHITE,self.rect)
        for button in self.buttons:
            button.draw()

        for entry_box in self.entry_boxes:
            entry_box.draw()

    def update(self,event):
        pass