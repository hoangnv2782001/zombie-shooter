import os

import pygame
from bullet import Bullet
from animation import Animation

'''
module player gồm 2 class là Player,Weapon_icon, và Helicopter
Player dùng để tạo nhân vật game
Weapon_icon dùng để cập nhật và hiển thị hình ảnh vũ khí đang sủ dụng
Helicopter dùng để tạo đối tượng trực thăng cứu trợ
--------------------------------------
Từ điển weapom lưu chũ các list chưa  thông tin về vũ khí gồm
[ thời gian cooldown  giữa 2 lần bắn, animation tấn công của mỗi loại vũ khí(đc thêm vào sau)]
'''

weapon = {'sword': [20], 'gun': [30]}
# Đọc các khung ảnh của animation tấn công và lưu vào weapon
for i in os.listdir('../Character Sprites/attack'):
    list = []
    for j in os.listdir(f'../Character Sprites/attack/{i}'):
        file = f'../Character Sprites/attack/{i}/{j}'
        list.append(pygame.transform.scale(pygame.image.load(file), (110, 110)))
    weapon[str(i)].append(list)


class Player(pygame.sprite.Sprite):
    DELAY = 100  
    G = 0.5  
    COOLDOWN_MP = 3000  

    '''
    từ điển bullet chứa 1 số thôn tin về loại đạn như
    [tên loại đạn , mp mà loại đạn đó tiêu tốn]
    có 3 loại đạn chính đc sử dụng bởi vũ khí súng
    bullet_gun là chi số của các loại đạn đó trong từ điển bullet
    '''
    bullet = {1: ['bullet1', 1], 2: ['bullet2', 2], 3: ['Rockets', 10]}

    def __init__(self, pos, constraint, speed):
        '''
         khởi tạo đối tượng
        :param pos: vị trí của nhân vật sẽ xuất hiện khi khơi tạo
        :param constraint: giới hạn độ rộng màn hình theo trục x
        :param speed: tốc độ di chuyển của nhân vật
        '''
        super().__init__()
        self.animation_dic = {'idle': [], 'walk': [], 'attack': [], 'death': []}
        #  thuoc tinh cơ bản của nhan vật
        self.moving_right = False
        self.moving_left = False
        self.moving_collision = True
        self.attack = False
        self.flip = False
        self.alive = True
        self.shooting = False
        self.hp_max = 100
        self.hp = 100
        self.mp_max = 100
        self.mp = 100
        self.weapon = 'sword'
        self.bullet_gun = 1
        self.index = 0
        self.direction = 1
        self.action = 'idle'
        #  khoi tao mot so thuoc tinh khac
        self.time_last = pygame.time.get_ticks()
        self.time_move = pygame.time.get_ticks()
        self.time_mp = pygame.time.get_ticks()
        self.cooldown = 0
        self.posY = 0

        # khoi tao cac animation chinh

        self.set_animation()
        self.cooldown, self.animation_dic['attack'] = weapon[self.weapon]
        self.image = self.animation_dic[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.width = 70
        self.rect.midbottom = pos
        self.weapon_icon = pygame.sprite.Group(Weapon_icon(self.weapon))

        #  cai dat cac animation quan trong
        self.rect_y = pos[1]
        self.speed = speed
        self.max_x_constraint = constraint
        self.rocket = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.rocket = pygame.sprite.GroupSingle()
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.05)
        self.font = pygame.font.Font('../font/gamecuben.ttf', 20)

    def set_active(self):
        """
         reset lại các thuộc tính cơ bản của nhân vật khi chuyển màn
        :return:
        """
        self.moving_right = False
        self.moving_left = False
        self.attack = False
        self.flip = False
        self.alive = True
        self.shooting = False
        self.index = 0
        self.direction = 1
        self.moving_collision = True

    def update_animation(self):
        """
          Cập nhât các khung ảnh của animation sau 1 khoang tg= Delay
          nếu inđex = len(animation) thì reset index= 0 với các trang thái khác  còn index = len(annimation)-1 vs trạng thái chết,
          đồng thời cập nhật lại shooting nế action = 'attack' và

        """
        self.image = pygame.transform.flip(self.animation_dic[self.action][self.index], self.flip, False)
        if pygame.time.get_ticks() - self.time_last > self.DELAY:
            self.time_last = pygame.time.get_ticks()
            self.index += 1
        
        if self.index >= len(self.animation_dic[self.action]):  
            if self.action == 'death':
                self.index = len(self.animation_dic[self.action]) - 1
            else:
                self.index = 0
            
            if self.action == 'attack':
                if not self.shooting:
                    self.attack = False

    def move(self):
        """
         Phương thức dùng để Di chuyển nhân vật
        :return:
        """
        # Độ dich chuyển của vị trí nhân vật theo x ,y
        dx = 0
        dy = 0
        # di chuyen sang trái
        if self.moving_left and self.rect.left >= -20:
            dx = -self.speed
            # Cập nhật flip khi shooting = false
            if not self.attack:  
                self.flip = True
            self.direction = -1

        # di chuyển sang phải nếu không va chạm với zombie còn sống
        if self.moving_right and self.rect.right <= self.max_x_constraint:
            if self.moving_collision:
                dx = self.speed
            if not self.attack:  
                self.flip = False
            self.direction = 1

        # giới hạn di chuyên của nhân vật trong phạm vi màn hình
        if self.rect.left + dx < -20:
            dx = -20 - self.rect.left
        # tính lại độ dịch dx nếu toạ độ của vật vượt quá giới hạn
        if self.rect.right + dx > self.max_x_constraint:
            dx = self.max_x_constraint - self.rect.right

        # cập nhật vị trí của nhân vạt sau 20 mili giây
        if pygame.time.get_ticks() - self.time_move > 20:
            self.rect.x += dx
            self.rect.y += dy
            self.time_move = pygame.time.get_ticks()

    def update_action(self, newaction):
        """
         Cập nhật hành động của nhân vật
        :param newaction: hành động mới
        :return:
        """
        if self.action != newaction:
            self.action = newaction
            self.index = 0
            self.time_last = pygame.time.get_ticks()

    def update(self, screen):
        """
        Cập nhật các trạng thái của nhân vật
        :param screen: đối tượng màn hình để hiển thị game
        :return:
        """

        self.update_animation()
        self.bullets.update()
        self.check_alive()
        self.rehabilitate_mp()
        if self.alive:
            if self.attack:  
                self.update_action('attack')

                if self.weapon == 'gun':
                    if self.shooting:  
                        self.shoot()
                        if self.bullet_gun == 3:  
                            self.shooting = False

                else:
                    if self.index == 3:  
                        self.shoot()
            elif self.moving_left or self.moving_right:  
                self.update_action('walk')
            else:
                self.update_action('idle')  
            self.move()

        
        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self):
        """
         Phương thức dùng để bắn đạn:
         Sau 1 khoang tg = cooldown thì viên đạn tiếp theo sẽ đc bắn trừ th là rocket
         rocket chỉ đc bắn khi trong group rocket ko có rocket nào
         Sau khi bắn thì mp sẽ bị giảm phụ thuộc vào lượng mp cần tiêu tốn của loại đạn đó
         Nếu lg hp ko đủ sẽ ko thể bắn sword ko tiêu tốn mp còn đạn của gun tiêu tốn mp

        """
        if self.cooldown == 0:
            shooted = False
            self.cooldown = weapon[self.weapon][0]  # cập nhật cooldown
            
            if self.weapon == 'gun' and self.mp >= Player.bullet[self.bullet_gun][1]:
                self.add_bullet(Player.bullet[self.bullet_gun][0])
                shooted = True
                self.laser_sound.play()  # âm thanh bắn đạn
            
            elif self.weapon == 'sword':
                self.add_bullet('sword')
                self.laser_sound.play()
            # mp tieu hao khi bắn đạn của súng
            if shooted:
                self.mp -= Player.bullet[self.bullet_gun][1]

    def add_bullet(self, bullet):
        """
        thêm đối tg đạn vào group
        :param bullet: tên loại đạn cần thêm
        :return:
        """
        if self.bullet_gun != 3:  
            if not self.flip:  
                self.bullets.add(Bullet(self.rect.midright, bullet, self.flip, self.max_x_constraint))
            else:
                self.bullets.add(Bullet(self.rect.midleft, bullet, self.flip, self.max_x_constraint))
        else:  
            if not self.flip:
                self.rocket.add(Bullet(self.rect.midright, bullet, self.flip, self.max_x_constraint))
            else:
                self.rocket.add(Bullet(self.rect.midleft, bullet, self.flip, self.max_x_constraint))

    def check_alive(self):
        """
        kiểm tra nhân vật còn sống hay ko nếu hp<0 thì cập nhật trạng thái chết va alive = False
        :return:
        """
        if self.hp <= 0:
            self.hp = 0
            self.speed = 0
            self.alive = False
            self.update_action('death')

    def rehabilitate_mp(self):
        """
        phuc hoi mp sau 1 khoang thời gian COOLDOWN_MP
        :return:
        """
        if pygame.time.get_ticks() - self.time_mp > self.COOLDOWN_MP:
            self.mp += 3
            self.time_mp = pygame.time.get_ticks()

        # Giới hạn mp
        if self.mp > self.mp_max:
            self.mp = self.mp_max

    def change_weapon(self):
        """
        Phương thức đổi vũ khí của nhân vật
        :return:
        """
        if self.weapon == 'sword':
            self.weapon = 'gun'
        else:
            self.weapon = 'sword'
        self.bullet_gun = 1  
        self.update_action('idle')

        
        self.cooldown, self.animation_dic['attack'] = weapon[self.weapon]
        self.weapon_icon.update(self.weapon)

    def change_bullet_gun(self):
        """
        Nếu vũ khí đang sử dụng là súng thì có thể thay đổi loại đạn của súng
        :return:
        """
        if self.weapon == 'gun':
            self.bullet_gun += 1  
            if self.bullet_gun > len(Player.bullet):
                self.bullet_gun = 1  

    def set_animation(self):
        """
        lưu các khng ảnh của các animation vào từ điển animation
        :return:
        """
        for f in os.listdir('../Character Sprites/animation'):
            list = []
            for i in os.listdir(f'../Character Sprites/animation/{f}'):
                file = f'../Character Sprites/animation/{f}/{i}'
                list.append(pygame.transform.scale(pygame.image.load(file).convert_alpha(), (110, 110)))
            self.animation_dic[str(f)] = list


class Weapon_icon(pygame.sprite.Sprite):
    def __init__(self, weapon):
        """

        :param weapon: tên loại vũ khí hiện đang sử dụng
        """
        pygame.sprite.Sprite.__init__(self)
        # Đọc hình ảnh của gun và sword
        gun = pygame.transform.scale(pygame.image.load('../Elements/weapon/image-01.png'), (125, 60))
        sword = pygame.transform.scale(pygame.image.load('../Elements/weapon/sword.png'), (147, 40))
        self.weapons = {'gun': gun, 'sword': sword}  
        self.weapon = weapon
        self.image = self.weapons[self.weapon]
        self.rect = pygame.Rect(160, 0, 150, 60)

    def update(self, weapon):
        """
        cập nhật hình
         :param weapon: tên loại vũ khí hiện đang sử dụng
        """
        self.image = self.weapons[weapon]


'''
Đọc các khung ảnh của animation Helicopter lưu vào trong list animation
'''
animation = []
for i in os.listdir('../maybay'):
    image = pygame.image.load(f"../maybay/{i}")
    image = pygame.transform.scale(image, (image.get_width() // 3, image.get_height() // 3))
    animation.append(image)


class Helicopter(Animation):
    def __init__(self, side, screen_width):
        """
        :param side: Phia xuất hiện của trực thăng bên phải hoặc trái
        :param screen_width: độ rộng màn hình
        """
        
        if side == 'right':
            x = screen_width + 50
            self.speed = - 3
            self.flip = True
        else:
            x = -50
            self.speed = 3
            self.flip = False
        Animation.__init__(self, animation, 100, self.flip)
        self.rect = self.image.get_rect(topleft=(x, 100))
        self.width = screen_width

    def update(self):
        """
        Cập nhạt trạng thái của trực thăng
        :return:
        """
        self.update_animation()

        
        self.rect.x += self.speed
        
        if self.rect.right < - self.rect.width or self.rect.left > self.width + self.rect.width:
            self.kill()
