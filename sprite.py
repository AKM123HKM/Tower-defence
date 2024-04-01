import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self,image_path,pos):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center = pos)
        self.id = id
        self.rotation = 0

    def change_rotation(self,rotation):
        self.rotation += rotation
        if self.rotation < 0 : self.rotation = 270
        elif self.rotation >= 360: self.rotation = 0
        self.image = pygame.transform.rotate(self.image,rotation)

class EnemySprite(Sprite):
    def __init__(self,image_path,pos,speed):
        super().__init__(image_path,pos)
        self.speed = speed
        self.direction = "down"

    def move(self):
        self.prev_pos = self.rect.center
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed