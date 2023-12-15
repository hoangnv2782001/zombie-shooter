import pygame
import os
from heath import HP

'''
module zombie có duy nhất 1 class là Zombie
Class zombie dùng để tạo các zombie trong game
Từ điển info_zombie chứa thông tin về các loại zombie các thôn tin đó là
[hp của zombie, tốc độ ,sát thương, tỉ lệ hình ảnh khi scale, coin nhận dc khi tiê diệt zombie, animatiom của zombie(sẽ đc thêm ở dưới)]
'''

info_zombie = {'zombie1': [10, 5, 1, 1, 5], 'zombie2': [7, 3, 3, 5, 4], 'zombie3': [7, 4, 4, 1, 3],
               'zombie4': [6, 5, 2, 1, 2], 'zombie5': [9, 4, 2, 1, 1]}

# Đọc các hoạt ảnh của zombie và lưu vào trong từ điển info_zombie
for i in os.listdir('../zombie'):
    animation = {}
    for j in os.listdir(f'../zombie/{i}'):
        arr = []
        scale = info_zombie[str(i)][3]
        for action in os.listdir(f'../zombie/{i}/{j}'):
            image = pygame.image.load(f'../zombie/{i}/{j}/{action}')
            image = pygame.transform.scale(image,
                                           (image.get_width() // scale, image.get_height() // scale))
            image = pygame.transform.flip(image, True, False)
            arr.append(image)
        animation[str(j)] = arr
    info_zombie[str(i)].append(animation)


class Zombie(pygame.sprite.Sprite):
    def __init__(self, zombie_type, x, y):
        """
        :param zombie_type: tên loại zombie
        :param x: toạ độ x
        :param y: toạ độ y
        """
        super().__init__()
        # Khởi tạo các thuộc tính cơ bản của zombie
        self.animation = {}  
        self.index = 0
        self.zombie_type = f'zombie{zombie_type}'
        self.action = 'run' 
        self.hp, self.speed, self.dame, scale, self.coin, self.animation = info_zombie[self.zombie_type]
        self.image = self.animation[self.action][self.index]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.alive = True
        self.max_hp = self.hp

        # Khởi tạo 1 số thuộc tính thời gian để tạo hiệu ứng cho zombie
        self.attack_cooldown = 1000
        self.cooldown = 100
        self.delay = 150
        self.time_attack = pygame.time.get_ticks()
        self.time = pygame.time.get_ticks()
        # Hiển thị thanh hp của zombie
        self.hp_bar = HP(self.rect.x, self.rect.y - 2, self.max_hp, self.rect.width, 2)

    def update(self, screen, player):
        """
         Kiểm tra va chạm giữa zombie và nhân vật :
		 nêú zombie va chạm với người và trang thái của zombie ko phải chết thì cập nhật trạng thái của zombie thành 'attack'
	     đồng thời cập nhật lại thuộc tính moving_collision của người chơi thành false để nhân vật ko thể di chuyển về bên phải
		 nếu không va chạm thì cập nhật trạng thái của zombie thành 'run'
		 Th còn lại thì cập nhật  moving_collision của người chơi thanh true để có thể di chuyển về bên phải

        :param screen:
        :param player:
        :return:
        """

        if pygame.sprite.spritecollide(self, player, False) and self.action != 'dead':
            self.update_action('attack')
            player.sprite.moving_collision = False
        elif self.action != 'dead' :
            self.update_action('run')


        self.image = self.animation[self.action][self.index]
        now = pygame.time.get_ticks()
        if now - self.time > self.cooldown:
            self.index += 1
            self.time = now
            if self.action == 'run':
                self.rect.x -= self.speed

            self.hp_bar.update(self.rect.x, self.rect.y - 2)

        
        if self.index >= len(self.animation[self.action]):
            if self.action == 'dead':
                self.index = len(self.animation[self.action]) - 1
            else:
                self.index = 0

        
        if self.hp > 0:
            self.hp_bar.draw(screen, self.hp)

        
        if self.hp <= 0 and self.action != 'dead':
            self.hp = 0
            self.update_action('dead')

        
        if self.action == 'dead':
            if self.delay < 0:
                self.kill()
            else:
                self.delay -= 1

        
        if self.action == 'attack':
            if pygame.time.get_ticks() - self.time_attack > self.attack_cooldown:
                player.sprite.hp -= self.dame
                if player.sprite.hp < 0:
                    player.sprite.hp = 0
                self.time_attack = pygame.time.get_ticks()


    def update_action(self, newaction):
        """
         Phương thức cạp nhật lại trạng thái của zombie
        :param newaction: hành dônng mới của zombie
        :return:
        """
        if self.action != newaction:
            self.action = newaction
            self.index = 0
            self.time = pygame.time.get_ticks()
