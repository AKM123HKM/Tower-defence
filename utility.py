import pygame
from settings import *
from functools import partial

class Button:
    def __init__(self,display_surf,pos,image_path = "",text = "button",func = lambda:print("clicked"),*args):
        #Main button
        self.display_surface = display_surf
        self.rect = pygame.rect.Rect(pos[0],pos[1],BUTTON_WIDTH,BUTTON_HEIGHT)
        self.color = BUTTON_COLOR
        self.type = "button"

        #Image
        if image_path:
            self.image = pygame.transform.scale((pygame.image.load(image_path)),(BUTTON_IMAGE_SIZE,BUTTON_IMAGE_SIZE))
            self.image_rect = self.image.get_rect(topleft = (pos[0]+BUTTON_IMAGE_OFFSET,pos[1]+BUTTON_IMAGE_OFFSET))
        else:
            self.image = image_path
        #Text
        self.text = text
        self.text_color = WHITE
        self.text_x = (pos[0] + ((BUTTON_WIDTH - (5*BUTTON_IMAGE_OFFSET+BUTTON_IMAGE_SIZE)) - (FONT.size(self.text)[0] / 2)))
        self.text_y = (pos[1] + ((BUTTON_HEIGHT / 2) - (FONT.size(self.text)[1] / 2)))
        
        #Function
        self.function = partial(func,*args)

    def hover_action(self,mouse_collision = True):
        if mouse_collision:
            self.color = BUTTON_HOVER_COLOR
            self.text_color = BUTTON_COLOR
        else:
            self.color = BUTTON_COLOR
            self.text_color = WHITE

    def scroll_action(self,y,speed):
        self.rect.y += y * speed
        if self.image: self.image_rect.y += y * speed
        self.text_y += y * speed

    def func(self):
        try:
            self.function()
        except TypeError:
            print("Clicked")

    def draw(self):
        #Button background
        pygame.draw.rect(self.display_surface,self.color,self.rect)
        
        #Button Image
        if self.image:self.display_surface.blit(self.image,self.image_rect)
        
        #Button Text
        text = FONT.render(self.text,False,self.text_color)
        self.display_surface.blit(text,(self.text_x,self.text_y))

class EntryBox:
    def __init__(self,display_surf,pos,start = 0,end = 100,func = ""):
        self.display_surface = display_surf
        self.color = ENTRY_BOX_COLOR
        self.rect = pygame.rect.Rect(pos[0],pos[1],ENTRY_BOX_WIDTH,ENTRY_BOX_HEIGHT)
        
        self.blink_visible = True
        self.blink_frame = 0
        
        self.start = start
        self.value = ""
        self.end = end
        self.max_len = 5

        if func:
            self.function = func
        else: self.function = func
        self.type = "entry_box"

    def scroll_action(self,y,speed):
        self.rect.y += y * speed

    def func(self):
        if self.function:
            entry_func = partial(self.function,self.value)
            entry_func()
        else:
            print(self.value)

    def left_click_action(self,mouse_collide = True):
        if mouse_collide:
            self.color = SELECTED_ENTRY_BOX_COLOR
        else:
            self.color = ENTRY_BOX_COLOR

    def key_input_action(self,event):
        if self.color == SELECTED_ENTRY_BOX_COLOR:
            if event.key >= pygame.K_0 and event.key <= pygame.K_9 and not len(self.value) >= self.max_len:
                key = int(event.unicode) #This ensures that the key presses are only in numbers; easy for me :)
                self.value += str(key)
            elif event.key == pygame.K_RETURN:
                if self.value:
                    if int(self.value) < self.start: self.value = ""
                    elif int(self.value) > self.end: self.value = str(self.end)
                self.color = ENTRY_BOX_COLOR
                self.func()
            elif event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]

    def blink(self):
        self.blink_frame += 1
        if self.blink_frame >= BLINK_SPEED:
            if self.blink_visible : self.blink_visible = False
            else: self.blink_visible = True
            self.blink_frame = 0
        if self.blink_visible:
            blink_surf = FONT.render("|",True,(255,0,0))
            y = (self.rect.y + self.rect.height / 2) - (blink_surf.get_size()[1] / 2)
            self.display_surface.blit(blink_surf,(self.rect.x,y))

    def draw(self):
        pygame.draw.rect(self.display_surface,self.color,self.rect)
        self.blink()
        text = FONT.render(str(self.value),True,(0,0,0))
        self.display_surface.blit(text,(self.rect.x,self.rect.y))