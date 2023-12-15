import os
import time

import pygame, sys
from player import Player, Helicopter

from zombie import Zombie
from random import choice, randint
from button import Button
from explosion import Explosion
from heath import HP, MP
from box_item import ItemBox, Bomb, Coin
from gameload import GameLoad, Info, Guide
import map

'''
module main có class Game và vòng lặp  game
class game xây dựng các logic xử lí sự kiện game
Vòng lặp game dùng để hiển thị game liên tục ko bị ngắt
------------------------------------------------------------
Khởi tạo một sô đối tượng cơ bản game như các module của pygame, screen , caption game ,icon game và clock(tạo fps game)
'''
pygame.init()
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Zombie Shooter')
pygame.display.set_icon(pygame.image.load('../Character Sprites/attack/gun/Shot_000.png').convert_alpha())
clock = pygame.time.Clock()

# khởi tạo font chũ và 1 số hình ảnh để hiển thị như bom , coin , zombie
font = pygame.font.Font('../font/gamecuben.ttf', 20)
bomb = pygame.image.load('../graphics/bom.png')
bomb = pygame.transform.scale(bomb, (bomb.get_width() // 5, bomb.get_height() // 5))
coin = pygame.transform.scale(pygame.image.load('../Elements/Coin/Coin_0000000.png').convert_alpha(), (50, 50))
zombie = pygame.transform.scale(pygame.image.load('../Elements/zombie_head.png').convert_alpha(), (50, 50))

# Đọc hình ảnh của các loại đạn và lưu trong list bullet_icon
bullet_icon = []
for i in os.listdir('../Elements/bullet'):
    for j in os.listdir(f'../Elements/bullet/{i}'):
        image = pygame.image.load(f"../Elements/bullet/{i}/{j}")
        image = pygame.transform.scale(image, (image.get_width() // 5, image.get_height() // 5))
        bullet_icon.append(image)
        break


def draw_text(text, text_col, x, y):
    """
    hiển thị text lên màn hình
    :param text: chuỗi kí tự cần hiển thị
    :param text_col: màu chứ
    :param x: toạ độ x
    :param y: toạ độ y
    :return:
    """
    img = font.render(text, False, text_col)
    screen.blit(img, (x, y))


class Game:
    def __init__(self):

        # backgrond cho menu tạo hiệu ứng chạy cho màn hình
        self.kill_zombie = 0
        self.image_bg = pygame.image.load('../graphics/background.jpg').convert_alpha()
        self.image_bg1 = pygame.transform.scale(self.image_bg, (screen_width, screen_height))
        self.image_bg2 = pygame.transform.scale(self.image_bg, (screen_width, screen_height))

        # cai dat map game
        self.map = map.Map()
        self.image_bg, self.bg_street = self.map.get_map('map1')
        self.rect_bg = pygame.Rect(0, 0, screen_width, screen_height)
        self.rect_street = self.bg_street.get_rect()
        self.rect_street.midbottom = screen.get_rect().midbottom

        # cài đặt nhân vật
        self.player_sprite = Player(self.rect_street.midtop, screen_width, 5)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.screen_rect = screen.get_rect()

        #  hp va mp cua nhan vat
        self.hp = HP(10, 10, 100, 150, 20)
        self.mp = MP()

        # khởi tạo các nút bấm trong game
        self.play_button = Button((screen_width - Button.width) / 2, screen_height / 2 - 150, 'Play')
        self.exit_button = Button((screen_width - Button.width) / 2, screen_height / 2 + 150, 'Exit')
        self.info_button = Button((screen_width - Button.width) / 2, screen_height / 2 - 50, 'Info')
        self.guide_button = Button((screen_width - Button.width) / 2, screen_height / 2 + 50, 'Guide')
        self.menu_button = Button((screen_width - Button.width) / 2 + 30, screen_height / 2 + 50, 'Menu')

        # group chứa các đối tượng explosion
        self.explosion_group = pygame.sprite.Group()

        # cài đặt zombie group để chưa zombie
        self.zombies = pygame.sprite.Group()

        # cài đặt group để chưa đối tg items và helicopter
        self.helicopter = pygame.sprite.GroupSingle()
        self.drop_time = randint(40, 80)
        self.items = pygame.sprite.Group()
        self.checkItem = False  
        self.posItem = [0, 100]  

        # âm thanh game
        music = pygame.mixer.Sound('../audio/bensound-epic.mp3')
        music.set_volume(0.03)
        music.play(loops=-1)
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(0.1)

        #  cai dat hieu ung load game, hiển thị các thông tin như info và guide
        self.gameload = GameLoad()
        self.info = Info(screen)
        self.guide = Guide(screen)

        # Các thuộc tính về zombie cần tiêu diệt ,xuất hiện trong 1 màn
        self.kill_zombie 
        self.zombie_die = 0
        self.zombie_time = 0
        self.zombie_active = 0
        self.cool_down = 0

        # Các thuộc tính chuyển màn
        self.update_map = False
        self.map_code = 1
        self.max_zombie = map.number_zombie[f'map{self.map_code}']

        # Các thuộc tính để và điều kiện cần để thả bom
        self.drop = False
        self.salary_bom = 8
        self.cool_down_bom = 0  
        self.price_bom = 80
        self.pos = [(70, 0), (170, 0), (270, 0), (370, 0), (470, 0), (570, 0), (670, 0), (770, 0),
                    (870, 0)] 
        self.boms = pygame.sprite.Group()

        #  cac thuoc tinh về việc vận hành game
        self.pause = True
        self.gamover = False
        self.game_active = False
        self.delay_game = 200
        self.win = False

        # coin trong game
        self.coin = 0
        self.coin_group = pygame.sprite.Group()

    def empty_grouup(self):
        """
         Xoá tát cả đối tượng khỏi các group bên dưới phục vụ cho việc chuyển màn và chơi lại
        :return:
        """
        self.items.empty()
        self.coin_group.empty()
        self.zombies.empty()
        self.helicopter.empty()
        self.boms.empty()
        self.explosion_group.empty()
        self.player_sprite.bullets.empty()
        self.player_sprite.rocket.empty()

    def reset(self):
        """
         reset lai 1 số thuộc tính để chuẩn bị cho việc chơi lại từ map 1
        :return:
        """
        self.empty_grouup()
        self.checkItem = False
        self.kill_zombie = 0
        self.zombie_die = 0
        self.zombie_time = 0
        self.zombie_active = 0
        self.cool_down = 0
        self.update_map = False
        self.map_code = 1
        self.max_zombie = map.number_zombie[f'map{self.map_code}']
        self.image_bg, self.bg_street = self.map.get_map(f'map{self.map_code}')
        self.rect_street = self.bg_street.get_rect()
        self.rect_street.midbottom = screen.get_rect().midbottom
        self.drop = False
        self.salary_bom = 8
        self.coin = 0
        self.pause = True
        self.gamover = False
        self.game_active = False
        self.player_sprite = Player(self.rect_street.midtop, screen_width, 5)
        self.player.add(self.player_sprite)

    def zombie_setup(self):
        """
        Cài đặt , khởi tạo zombie cho mỗi map
        nếu số zombie xuất hiện nhỏ hơn max_zombie thì tiếp tực tạo zombie
        nếu tiêu diệt zombie của 1 map thì sẽ chuyển nếu map <6 (giới hạn hiện tại của game sẽ phát triên thêm trong tương lai)
        nếu vợt qua tát cả map người chơi sẽ win
        :return:
        """
        if self.zombie_active < self.max_zombie:
            # tạo zombie sau 1 khoang tg
            if pygame.time.get_ticks() - self.zombie_time > 1500:
                zombie = Zombie(choice([1, 2, 3, 4, 5]), screen_width - 50, self.rect_street.top)
                self.zombie_active += 1
                self.zombies.add(zombie)
                self.zombie_time = pygame.time.get_ticks()
            # Kiểm tra cho việc updatemap
        elif self.zombie_die == self.max_zombie:
            if len(self.zombies) == 0 and self.map_code < 6:
                self.update_map = True
                self.map_code += 1
            # kiểm tra việc win
            elif len(self.zombies) == 0:
                self.win = True

    def change_map(self):
        """
        phương thức thay đổi map cập nhật lại 1 số thuộc tính mới (chỉ đổi map khi map< 6)

        :return:
        """
        if self.map_code <= 6:
            self.update_map = False

            # khởi tạo lại map và vị trí của nhân vật
            self.image_bg, self.bg_street = self.map.get_map(f'map{self.map_code}')
            self.rect_street = self.bg_street.get_rect()
            self.rect_street.midbottom = screen.get_rect().midbottom
            self.player_sprite.rect.midbottom = self.rect_street.midtop
            self.player_sprite.rect_y = self.rect_street.top

            # khởi tạo lại các thuộc tính tiêu diệt zombie
            self.zombie_time = pygame.time.get_ticks()
            self.zombie_die = 0
            self.zombie_active = 0
            self.max_zombie = map.number_zombie[f'map{self.map_code}']

            # khởi tạo lại các thuộc tính bom
            self.salary_bom = 8
            self.drop = False

            # reset lại nhan vật và emty các group
            self.empty_grouup()
            self.player_sprite.set_active()

    def drop_bom(self):
        """
        Phương thức dùng để tạo hiệu ứng bom rơi
        Bom sẽ đc thả khi đủ coin và nhấn r khi rơi sẽ tạo hiệu ứng nổ và tiêu diệt zombie nếu va chạm
        :return:
        """
        if self.drop:
            # thả bom sau 1 khoảng tg = cool_down_bom tối đa 8 quả
            if self.cool_down_bom <= 0:
                pos = choice(self.pos)
                bom = Bomb(pos, self.rect_street.top)
                self.boms.add(bom)
                self.cool_down_bom = 100
                self.salary_bom -= 1
            else:
                self.cool_down_bom -= 1
        # reset drop khi thả hết
        if self.salary_bom <= 0:
            self.salary_bom = 8
            self.drop = False
        # khởi tạo hiệu ứng nổ khi va chạm mặt đất
        if self.boms:
            for bom in self.boms.sprites():
                if bom.explosion_bomb():
                    self.explosion_group.add(Explosion(bom.rect.midbottom, 'bom'))
                    bom.kill()
                    self.explosion_sound.play()

    # cai dat item chinh sua thoi gian:00h18 11/10/2021
    def drop_item(self):
        """
        Phương thức dùng để tạo hiệu ứng item rơi
        Sau 1 khoảng tg drop_time trực thăng sẽ bay qua và thả item
        :return:
        """
        self.drop_time -= 1
        if self.drop_time <= 0 and len(self.helicopter) == 0:
            self.posItem[0] = randint(20, screen_width // 2)
            self.helicopter.add(Helicopter(choice(['right', 'left']), screen_width))
            self.drop_time = randint(900, 1500)
            self.checkItem = True
        
        if self.helicopter.sprite and self.helicopter.sprite.rect.collidepoint(self.posItem) and self.checkItem:
            item = ItemBox(self.helicopter.sprite.rect.midbottom, self.rect_street.top)
            self.items.add(item)
            self.checkItem = False

    def collision_checks(self):
        """
        xử lí va chạm của zombie vs đạn
        Xử lí coin tạo ra
        Xử lí zombie đã chết
        :return:
        """
        if self.player.sprite.bullets:
            for bullet in self.player.sprite.bullets:
                # danh sách zombie chúng đạn
                zombie_hit = pygame.sprite.spritecollide(bullet, self.zombies, False)
                if zombie_hit:
                    

                    for zombie in zombie_hit:
                        if zombie.hp > 0:
                            zombie.hp -= bullet.dame
                            bullet.kill()
                            self.explosion_sound.play()
                            explosion = Explosion(zombie.rect.center, 'bullet')
                            self.explosion_group.add(explosion)

        elif len(self.player_sprite.rocket) > 0 and self.player_sprite.bullet_gun == 3:
            # danh sách zombie chúng đạn trong th đạn là rocket
            zombie_hit = pygame.sprite.spritecollide(self.player_sprite.rocket.sprite, self.zombies, False)
            if zombie_hit:
                for zombie in zombie_hit:
                    if zombie.hp > 0:
                        explosion = Explosion(zombie.rect.center, 'rocket')
                        
                        explosion_zombie = pygame.sprite.spritecollide(explosion, self.zombies, False)
                        self.explosion_sound.play()
                        self.explosion_group.add(explosion)
                        dame = self.player_sprite.rocket.sprite.dame
                        
                        self.player_sprite.rocket.empty()
                        
                        for zombie in explosion_zombie:
                            zombie.hp -= dame
                        break
        # xử lí di chuỷen của nhân vật khi va chạm
        if not pygame.sprite.groupcollide(self.player, self.zombies, False, False):
            self.player_sprite.moving_collision = True

        if self.zombies:
            # tính số zombie die và khởi tạo coin
            for zombie in self.zombies:
                if zombie.hp <= 0 and zombie.alive:
                    self.zombie_die += 1
                    self.kill_zombie += 1
                    zombie.alive = False
                    self.coin_group.add(Coin(zombie.rect.center, zombie.coin))

        if self.coin_group:
            
            for coin in self.coin_group.sprites():
                if coin.fly:
                    self.coin += coin.coin
                    coin.fly = False

    def victory_message(self):
        """
        Hiển thị thông victory message lên màn hình
        :return:
        """
        font = pygame.font.Font('../font/gamecuben.ttf', 50)
        victory_surf = font.render('You Win', True, 'red')
        victory_rect = victory_surf.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(victory_surf, victory_rect)

    def draw_backgroundmenu(self):
        """
        Tạo hiểu ứng chuyển động của background menu
        :return:
        """
        screen.blit(self.image_bg1, self.rect_bg)
        screen.blit(self.image_bg2, (self.rect_bg.x + screen_width, 0))
        self.rect_bg.x -= 1
        if self.rect_bg.x < -screen_width:
            self.rect_bg.x = 0

    def run(self):
        """
        Xử lí 1 vòng lặp game
        :return:
        """
        
        self.zombies.draw(screen)
        self.player_sprite.bullets.draw(screen)
        self.helicopter.draw(screen)
        self.coin_group.draw(screen)
        self.items.draw(screen)
        self.boms.draw(screen)
        self.player_sprite.rocket.draw(screen)
        self.player.draw(screen)
        self.explosion_group.draw(screen)
        self.hp.draw(screen, self.player_sprite.hp)
        self.mp.draw(screen, self.player_sprite.mp)
        self.player_sprite.weapon_icon.draw(screen)
        if self.pause and self.gamover == False and self.win == False:
            # Update các đối tượng
            self.helicopter.update()
            self.explosion_group.update()
            self.zombies.update(screen, self.player)
            self.player.update(screen)
            self.boms.update(screen, self.zombies)
            self.items.update(self.player_sprite)
            self.player_sprite.rocket.update()
            self.coin_group.update()
            # hàm xử lí 1 số logic sự kiện
            self.collision_checks()
            self.zombie_setup()
            self.drop_bom()
            self.drop_item()

            # Xư lí gameover
            if self.player_sprite.alive == False and self.delay_game < 0:
                self.gamover = True
                self.delay_game = 200
            elif not self.player_sprite.alive:
                self.delay_game -= 1
        elif not self.pause:  
            draw_text('Press enter to continue...', (123, 90, 123), 400, screen_height // 2)

        # xử lí game over
        if self.gamover:
            draw_text('Game Over', 'red', 450, 200)
            draw_text('Coin : ' + str(self.coin), 'red', 450, 250)
            draw_text('Zombies : ' + str(self.kill_zombie), 'red', 450, 300)
            if self.menu_button.draw_button(screen):
                self.game_active = False
                self.reset()
                self.gameload.draw(screen)
        # xử lí game wim
        if self.win:
            if self.delay_game > 0:
                self.victory_message()
                self.delay_game -= 1
            elif self.delay_game == 0:
                self.delay_game = 200
                self.game_active = False
                self.gameload.draw(screen)
                self.reset()

    def game_event(self):
        """
         Xự kiên trong game
        :return:
        """
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game_active:
                # sự kiện nhấn
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:  
                        self.player_sprite.attack = False
                        self.player_sprite.moving_left = True
                    elif event.key == pygame.K_d:  
                        self.player_sprite.attack = False
                        self.player_sprite.moving_right = True
                    elif event.key == pygame.K_SPACE and self.pause: 
                        if self.player_sprite.bullet_gun != 3 or len(self.player_sprite.rocket) == 0:
                            self.player_sprite.attack = True
                            self.player_sprite.shooting = True

                            self.player_sprite.moving_left = False
                            self.player_sprite.moving_right = False
                    elif event.key == pygame.K_r and self.coin >= self.price_bom and self.pause:  
                        self.drop = True
                        self.coin -= self.price_bom
                    elif event.key == pygame.K_f and self.pause:  
                        self.player_sprite.shooting = False
                        self.player_sprite.change_weapon()
                    elif event.key == pygame.K_ESCAPE:  
                        self.pause = False
                    elif event.key == pygame.K_RETURN:  
                        self.pause = True
                    elif event.key == pygame.K_q and self.pause: 
                        self.player_sprite.change_bullet_gun()
                # sự kiện thả nút
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:  
                        self.player_sprite.moving_left = False
                    elif event.key == pygame.K_d:  
                        self.player_sprite.moving_right = False
                    elif event.key == pygame.K_SPACE:  
                        self.player_sprite.shooting = False

    def update_screen(self):
        """
        Cập nhật 1 số hình ảnh khác trên màn hình
        :return:
        """
        # backgruond game
        screen.blit(self.image_bg, (0, 0))
        screen.blit(self.bg_street, self.rect_street)

        # hiển thị bom va giá
        pygame.draw.rect(screen, 'black', (450, 35, 80, 30), 0, 4)
        screen.blit(bomb, (400, 0))
        draw_text(str(self.price_bom), (255, 255, 255), 470, 35)
        screen.blit(pygame.transform.scale(coin, (25, 25)), (507, 34))

        # hiên thị vũ khhis
        if self.player_sprite.weapon == 'sword':
            screen.blit(bullet_icon[3], (300, 10))
        else:
            screen.blit(bullet_icon[self.player_sprite.bullet_gun - 1], (300, 10))

        # hien thi coin icon
        pygame.draw.rect(screen, 'black', (600, 15, 100, 30), 0, 4)
        screen.blit(coin, (590, 5))
        draw_text(str(self.coin), (255, 255, 255), 650, 17)

        # hien thi zombie da tieu diet
        pygame.draw.rect(screen, 'black', (750, 15, 100, 30), 0, 4)
        screen.blit(zombie, (738, 10))
        draw_text(str(self.kill_zombie), (255, 255, 255), 800, 17)
        draw_text('Map: ' + str(self.map_code), 'red', 10, 60)


game = Game()

while True:
    game.game_event()
    if game.game_active:
        if not game.update_map:
            game.update_screen()
            game.run()
        else:
            time.sleep(0.5)
            game.gameload.draw(screen)
            game.change_map()

    else:
        game.draw_backgroundmenu()
        if game.play_button.draw_button(screen):
            game.win = False
            game.game_active = True
            game.gameload.draw(screen)
        if game.info_button.draw_button(screen):
            game.info.draw()
        if game.guide_button.draw_button(screen):
            game.guide.draw()
        if game.exit_button.draw_button(screen):
            sys.exit()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
