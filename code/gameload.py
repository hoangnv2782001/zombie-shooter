import pygame
import sys
from button import Button1

'''
module gameload gồm 3 class 
GameLoad tạo hiệu ứng load trong game
Info hiển thị thông tin về game
Guide hiển thị các hướng dẫn chơi game
'''


class GameLoad:
    def __init__(self):
        self.x = 400
        self.y = 200
        self.load = 0
        self.load_max = 200
        self.time = pygame.time.get_ticks()

    def draw(self, screen):
        """
        Hiển thị hiệu ứng load trong game
        :param screen: đối tượng màn hình
        :return:
        """
        self.time = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.fill((123, 122, 111))

            # hiển thị thanh load game
            tmp = self.load / self.load_max
            pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, 204, 24))
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 200 * tmp, 20))

            # cập nhật trạng thái thanh load game
            if pygame.time.get_ticks() - self.time > 100:
                self.load += 10
                self.time = pygame.time.get_ticks()
            if self.load == self.load_max + 10:
                break
            pygame.display.flip()
        self.load = 0


def draw_text(screen, font, text, text_col, x, y):
    """
     Tương tự hàm dra_text cuả class Info
        :param screen: đối tượng màn hình để hiển thị text
        :param font: ffont chữ
        :param text: chuỗi cần viết lên
        :param text_col: màu chữ
        :param x: toạ đô x
        :param y: toạ độ y
        :return:
    """
    img = font.render(text, False, text_col)
    screen.blit(img, (x, y))


class Info:
    def __init__(self, screen):
        self.font = pygame.font.Font('../font/gamecuben.ttf', 30)
        self.font1 = pygame.font.Font('../font/gamecuben.ttf', 20)
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.background = pygame.image.load('../Elements/maps_table.jpg')
        self.button = Button1(450, 530, pygame.image.load('../Elements/Button_exit.png'), 1)

    def draw(self):
        while True:
            """
            Hiển thị các thông tin 1 số thông tin về game lên màn hình
            :return: 
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # Vẽ thông tin lên màn hình
            self.screen.blit(self.background, (0, 0))
            draw_text(self.screen,self.font, 'ZOMBIES SHOOTER', 'red', 300, 20)
            draw_text(self.screen,self.font1, 'Idependent Video Game created and designed by Group 13:', 'red', 30, 100)
            draw_text(self.screen,self.font, 'Nguyen Quy Duong', 'red', 300, 160)
            draw_text(self.screen,self.font, 'Nguyen Phu Luong', 'red', 300, 240)
            draw_text(self.screen,self.font, 'Nguyen Van Hoang', 'red', 300, 320)
            draw_text(self.screen,self.font, 'Nghe Minh Tan', 'red', 300, 400)
            draw_text(self.screen,self.font, 'Khong Duy Tuan', 'red', 300, 480)
            if self.button.draw(self.screen):
                break
            pygame.display.flip()



class Guide:
    def __init__(self, screen):
        self.font = pygame.font.Font('../font/gamecuben.ttf', 30)
        self.font1 = pygame.font.Font('../font/gamecuben.ttf', 20)
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.button = Button1(450, 530, pygame.image.load('../Elements/Button_exit.png'), 1)


    def draw(self):
        """
          Hiển thị các thông tin hướng dẫn chơi game
        :return:
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill((12, 78, 90))
            draw_text(self.screen,self.font, 'INSTRUCTIONS', 'red', 300, 20)
            draw_text(self.screen,self.font, 'Pause Game : Esc', 'red', 200, 80)
            draw_text(self.screen,self.font, 'Acttack : Space', 'red', 200, 160)
            draw_text(self.screen,self.font, 'Move : A or D', 'red', 200, 240)
            draw_text(self.screen,self.font, 'Change Weapon : F', 'red', 200, 320)
            draw_text(self.screen,self.font, 'Change Bullet : Q', 'red', 200, 400)
            draw_text(self.screen,self.font, 'Drop Bomb : R', 'red', 200, 480)

            if self.button.draw(self.screen):
                break
            pygame.display.flip()
