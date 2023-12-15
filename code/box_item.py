import os
import pygame
import random
from animation import Animation

'''
module box_item gồm 3 class ItemBox , Bomb và item
ItemBox dùng để tạo các dổi tượng item cứu trợ cho nhân vật như Hp và Mp
Bomb là class dùng để tạo đối tượng bomb đây là vật phầm mất tiền người chơi phải sưu tầm đủ tiền để mua
Coin là class tạo các đổi tượng coin . Coin sẽ rơi ra khi ta tiêu diệt zombie
'''

image_hp = pygame.image.load('../graphics/hp.png')
image_hp = pygame.transform.scale(image_hp, (image_hp.get_width() // 10, image_hp.get_height() // 10))
image_mp = pygame.image.load('../graphics/mp.png')
image_mp = pygame.transform.scale(image_mp, (image_mp.get_width() // 10, image_mp.get_height() // 10))
image_bom = pygame.image.load('../graphics/bom.png')
image_bom = pygame.transform.scale(image_bom, (image_bom.get_width() // 5, image_bom.get_height() // 5))

G = 0.25  # gia tôc rơi

# Lưu các khung ảnh của animation vào coin_list
coin_list = []
for i in os.listdir('../Elements/Coin'):
    image = pygame.image.load(f"../Elements/Coin/{i}")
    image = pygame.transform.scale(image, (image.get_width() // 5, image.get_height() // 5))
    coin_list.append(image)


class ItemBox(pygame.sprite.Sprite):
    # từ điển item_boxes chứa các hình ảnh cuả các  item
    item_boxes = {'hp': image_hp, 'mp': image_mp}

    def __init__(self, pos, top):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = random.choice([str(i) for i in self.item_boxes.keys()])  
        self.image = self.item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.speed = 0
        self.rect.midtop = pos  
        self.top = top  


    def update(self, player):
        """
        Cập nhật trạng thái ,vị trí của hộp item từ lúc đc thả cho đến khai va chạm với nhân vật
        :param player: group chứa đối tượng player
        :return:
        """
        
        dy = 0
        self.speed += G
        dy += self.speed
        if self.rect.bottom + dy > self.top:
            dy = self.top - self.rect.bottom
        self.rect.y += dy
        '''
          kiểm tra xem nhân vật có chạm vào item ko nếu chạm vào hộp hp thì hồi hp còn nếu chạm vào hộp mp thì hồi mp 
          và sau đó xoá bỏ item đang hiển thị còn nếu không chạm thì vẫn hiển thị hộp item
         '''
        if pygame.sprite.collide_mask(self, player):
            if self.item_type == 'hp':
                player.hp += 20
                if player.hp > player.hp_max:
                    player.hp = player.hp_max
            if self.item_type == 'mp':
                player.mp += 10
                if player.mp > player.mp_max:
                    player.mp = player.mp_max
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, top):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_bom
        self.rect = self.image.get_rect()
        self.speed = 0
        self.rect.midtop = pos  
        self.top = top  
    def update(self, screen, zombies):
        """

        :param screen: đối tượng mành hình hiển thị
        :param zombies: group chứa các đói tượng zomie
        :return:
        """
        
        dy = 0
        self.speed += G
        dy += self.speed
        
        if self.rect.bottom + dy > self.top:
            dy = self.top - self.rect.bottom
        self.rect.y += dy
        '''
         Kiểm tra va chạm của bom với mật đất
         Nếu va chạm sẽ tạo vụ nổ và nếu có zombie va chạm với bom thì sẽ bị trừ hp về 0
         '''
        if self.rect.bottom == self.top:
            zombie = pygame.sprite.spritecollide(self, zombies, False)
            if zombie:
                for i in zombie:
                    i.hp = 0

    
    def explosion_bomb(self):
        if self.rect.bottom == self.top:
            return True
        return False


# kế thừa class animation
class Coin(Animation):
    def __init__(self, pos, coin):
        Animation.__init__(self, coin_list, 90, False)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 0
        self.coin = coin
        self.fly = False
        self.time_fly = 40

    def update(self):
        """
              hiệu ứng bay lên của coin
              Tính từ lúc tạo ra nếu time_fly > 0 thì coin sẽ không bay lên và time_fly giảm 1
              khi time_fly < 0 thì coin bắt đầu bay lên và trạng thái fly = True
        """
        self.update_animation()

        if self.time_fly < 0:
            self.speed -= G
            self.rect.y += self.speed - G
        else:
            self.time_fly -= 1
            if self.time_fly < 0:
                self.fly = True
        
        if self.rect.bottom <= 0:
            self.kill()
