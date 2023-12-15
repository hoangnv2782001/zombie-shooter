import os

import pygame
from animation import Animation

'''
module gồm duy nhất 1 class là Bullet
Class Bullet dùng để tạo các đối tượng đạn khi nhân vật bắn
'''

# từ điển cartridge_box chứa các list trong các list lại chứa các thông tin về loại đạn bao gồm :
# [tốc độ , sát thương , khoảng thời gian cooldown giữa hai lần cập nhật khung ảnh của đạn]
cartridge_box = {'bullet1': [-10, 2, 100], 'bullet2': [-10, 3, 100], 'Rockets': [-5, 7, 150], 'sword': [-10, 1, 100]}

# Đọc các hình ảnh của loại đạn và lưu vào trong list thông tin loại đạn trong từ điển cartridge_box
for i in os.listdir('../Elements/bullet'):
    list = []
    for j in os.listdir(f'../Elements/bullet/{i}'):
        image = pygame.image.load(f'../Elements/bullet/{i}/{j}')  
        image = pygame.transform.scale(image, (image.get_width() // 5, image.get_height() // 5))  
        list.append(image)  
    cartridge_box[str(i)].append(list)  


class Bullet(Animation):
    def __init__(self, pos, bullet, flip, screen_width):
        """

        :param pos: vị trí xuát hiện của đạn
        :param bullet: tên đạn
        :param flip: thuộc tính bool Nếu = true ảnh đc lật theo chiều ngang nêu = False ảnh giữ nguyên
        :param screen_width: chiều rộng của màn hình
        """
        Animation.__init__(self, cartridge_box[bullet][3], cartridge_box[bullet][2], flip)
        self.speed, self.dame = cartridge_box[bullet][0], cartridge_box[bullet][1]
        self.rect = self.image.get_rect()
        self.time = pygame.time.get_ticks()
        
        if not self.flip:
            self.rect.midleft = pos
        else:
            self.rect.midright = pos
        self.rect.y += 15
        self.width_x_constraint = screen_width

    # Đối tượng đạn sẽ bị xoá khỏi các group chứa nó nếu bay ra khỏi phạm vi màn hình
    def destroy(self):
        if self.rect.left <= 0 or self.rect.right >= self.width_x_constraint:
            self.kill()

    def update(self):
        """
        Cập nhạta trạng thái của bullet
        :return:
        """
        self.update_animation()

        
        if self.flip:
            self.direction = -1
        else:
            self.direction = 1

       
        self.rect.x -= self.speed * self.direction
        self.destroy()
