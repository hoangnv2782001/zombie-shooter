import os

import pygame
'''
module explosion chứa 1 class duy nhất là class explosion
class explosion dùng để tạo các hoạt ảnh nổ tung trong game
'''
explosion = {}

#Đọc các khung ảnh của 1 animation vào trong một list xong lưu các list đó vào trong từ điển explosion
for i in os.listdir('../explosion'):
    list = []
    for j in os.listdir(f'../explosion/{i}'):
        image = pygame.image.load(f'../explosion/{i}/{j}')
        if str(i) == 'bullet': 
            list.append(pygame.transform.scale(image,(image.get_width()//10,image.get_height()//10)))
        elif str(i)=='rocket': 
            list.append(pygame.transform.scale(image,(image.get_width()//3,image.get_height()//3)))
        else:                  
            list.append(pygame.image.load(f'../explosion/{i}/{j}'))
    explosion[str(i)]=list

class Explosion(pygame.sprite.Sprite):
    def __init__(self,pos,type):
        """

        :param pos: vị trí cuất hiện của vụ nổ
        :param type: loại vụ nổ do cái gì gây rra
        """
        super().__init__()
        self.animation = []
        self.animation = explosion[type]
        self.index = 0
        self.image = self.animation[self.index]
        self.rect = self.image.get_rect()
        # xác điịnh vị trí vụ nổ
        if type == 'bom':
            self.rect.midbottom = pos
        else:
            self.rect.center = pos
        self.time = pygame.time.get_ticks()
        self.cooldown = 100


    def update(self):
        """
        hàm update dùng để cập nhật các khung ảnh của 1 animation
        :return:
        """
       # Sau 1 Khoảng thời gian = cooldown thì cập nhật khung ảnh mới bằng cách tăng chỉ số index của list chúa hoạt ảnh
        if pygame.time.get_ticks() - self.time >= self.cooldown:
            self.time = pygame.time.get_ticks()
            self.index += 1
            '''    
            Nếu index chỉ đến chỉ số cuối của list animation thì sẽ xoá đôi tượng explosion này khỏi tất cả các group chứa nó
            Nếu không phải chí số cuối thì cập nhật hoạt ảnh hiện tại của animation
            '''
            if self.index == len(self.animation):
                self.kill()
            else:
                self.image = self.animation[self.index]