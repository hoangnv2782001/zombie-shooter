import pygame

"""
module animation chuuắ 1 class animation
Class animation dùng để xây dưng class cha tạo các animation và đc kế thừa bởi 1 số class như coin ...
"""


class Animation(pygame.sprite.Sprite):
    def __init__(self, animation, cooldown, flip=False):
        pygame.sprite.Sprite.__init__(self)
        self.animation = animation
        self.index = 0
        self.cooldown = cooldown
        self.flip = flip 
        self.time = pygame.time.get_ticks()
        self.image = pygame.transform.flip(self.animation[self.index], flip, False)

    def update_animation(self):
        """
        Thuật toán quan trọng
        Cập nhật khung ảnh của 1 animation
        :return:
        """
        
        self.image = pygame.transform.flip(self.animation[self.index], self.flip, False)

        
        if pygame.time.get_ticks() - self.time > self.cooldown:
            self.index += 1
            self.time = pygame.time.get_ticks()  

        
        if self.index >= len(self.animation):
            self.index = 0
